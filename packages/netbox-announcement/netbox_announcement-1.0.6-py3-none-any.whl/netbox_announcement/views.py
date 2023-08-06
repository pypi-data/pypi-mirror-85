from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views.generic import View
from django.utils.html import escape
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django_tables2 import RequestConfig

import logging
import time
from utilities.forms import TableConfigForm, restrict_form_fields
from utilities.paginator import EnhancedPaginator, get_paginate_count
from utilities.utils import normalize_querydict, prepare_cloned_fields
from utilities.views import (
    GetReturnURLMixin, ObjectView, ObjectEditView, ObjectDeleteView, ObjectListView,
)
from .models import Announcement, AnnouncementUpdate, AnnouncementStatus
from .choices import *
from . import tables, filters, forms

# 
# Announcement
# 

class AnnouncementListView(ObjectListView):
    """
    Present announcement
    """
    queryset = Announcement.objects.prefetch_related(
        'user')
    filterset = filters.AnnouncementFilterSet
    filterset_form = forms.AnnouncementFilterForm
    table = tables.AnnouncementTable
    template_name = 'netbox_announcement/announcement_list.html'
    
    def get(self, request, **kwargs):
        logger = logging.getLogger('netbox_announcement.views.AnnouncementListView')

        self.queryset = Announcement.objects.restrict(request.user, 'view').prefetch_related('user')
        
        if self.filterset:
            self.queryset = self.filterset(request.GET, self.queryset).qs
            
        # Construct the table based on the user`s permissions
        if request.user.is_authenticated:
            columns = request.user.config.get(
                f"tables.{self.table.__name__}.columns")
        else:
            columns = None
            
        table = self.table(
            self.queryset,
            orderable=True,
            columns=columns
        )
        
        # Apply the request context
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        
        RequestConfig(request, paginate).configure(table)
        context = {
            'table': table,
            'table_config_form': TableConfigForm(table=table),
            'filter_form': self.filterset_form(request.GET, label_suffix='') if self.filterset_form else None,
        }
        return render(request, self.template_name, context)


class AnnouncementView(ObjectView):
    queryset = Announcement.objects.prefetch_related('user')
    
    def get(self, request, pk):
        announcement = get_object_or_404(self.queryset, pk=pk)
        announcement_updates = AnnouncementUpdate.objects.filter(
            announcement=announcement).prefetch_related('user')
        announcement_status = AnnouncementStatus.objects.all()

        return render(request, 'netbox_announcement/announcement_detail.html', {
            'announcement': announcement,
            'announcement_status': announcement_status,
            'announcement_updates': announcement_updates,
        })
        
    def post(self, request, pk):
        announcement = get_object_or_404(self.queryset, pk=pk)
        data = request.POST
        
        # status update
        status_id = data['status_update'] if 'status_update' in data else None
        status_queryset = AnnouncementStatus.objects.all()
        status = get_object_or_404(status_queryset, pk=status_id)
        announcement.status=status
        announcement.save()
        
        return JsonResponse({
            'result': 'Announcement status updated successfully'
        })

class AnnouncementUpdateView(ObjectView):
    queryset = Announcement.objects.prefetch_related('user')
    
    def post(self, request, pk):
        announcement = get_object_or_404(self.queryset, pk=pk)
        data = request.POST
        
        # save announcement update
        status_id = data['update_status'] if 'update_status' in data else None
        status_queryset = AnnouncementStatus.objects.all()
        status = get_object_or_404(status_queryset, pk=status_id)
        
        content = data['update_content'] if 'update_content' in data else None
        announcement.status=status
        announcement.save()    
        au = AnnouncementUpdate(announcement=announcement,
                           user=request.user, content=content)
            
        au.save()
        
        return JsonResponse({
            'result': 'announcement update created successfully'
        })
        
        
    

class AnnouncementTemplateView(ObjectEditView):
    
    def get_return_url(self, request, obj=None):
        # First, see if `return_url` was specified as a query parameter or form data. Use this URL only if it's
        # considered safe.
        query_param = request.GET.get(
            'return_url') or request.POST.get('return_url')
        if query_param and is_safe_url(url=query_param, allowed_hosts=request.get_host()):
            return query_param

        # Next, check if the object being modified (if any) has an absolute URL.
        if obj is not None and obj.pk and hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()

        # Attempt to dynamically resolve the list view for the object
        if hasattr(self, 'queryset'):
            model_opts = self.queryset.model._meta
            try:
                return reverse(f'plugins:{model_opts.app_label}:{model_opts.model_name}_list')
            except NoReverseMatch:
                pass

        # If all else fails, return home. Ideally this should never happen.
        return reverse('home')
        
    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(
            'netbox_announcement.views.AnnouncementTemplateView')
        print("POST params:", request.POST)
        # check separate param
        exist_separate = True if 'separate' in request.POST else False
        
        is_separate = True
        if exist_separate:
            if request.POST['separate']:
                is_separate = True
            else:
                is_separate = False
        else:
            is_separate = False
        
        if not is_separate: # create one announcement per multiple selections
            obj = self.alter_obj(self.get_object(kwargs), request, args, kwargs)
            form = self.model_form(
                data=request.POST,
                files=request.FILES,
                instance=obj
            )
            restrict_form_fields(form, request.user)

            if form.is_valid():
                logger.debug("Form validation was successful")

                try:
                    with transaction.atomic():
                        object_created = form.instance.pk is None
                        obj = form.save()

                        # Check that the new object conforms with any assigned object-level permissions
                        self.queryset.get(pk=obj.pk)

                    msg = '{} {}'.format(
                        'Created' if object_created else 'Modified',
                        self.queryset.model._meta.verbose_name
                    )
                    logger.info(f"{msg} {obj} (PK: {obj.pk})")
                    if hasattr(obj, 'get_absolute_url'):
                        msg = '{} <a href="{}">{}</a>'.format(
                            msg, obj.get_absolute_url(), escape(obj))
                    else:
                        msg = '{} {}'.format(msg, escape(obj))
                    messages.success(request, mark_safe(msg))

                    if '_addanother' in request.POST:

                        # If the object has clone_fields, pre-populate a new instance of the form
                        if hasattr(obj, 'clone_fields'):
                            url = '{}?{}'.format(
                                request.path, prepare_cloned_fields(obj))
                            return redirect(url)

                        return redirect(request.get_full_path())

                    return_url = form.cleaned_data.get('return_url')
                    if return_url is not None and is_safe_url(url=return_url, allowed_hosts=request.get_host()):
                        return redirect(return_url)
                    else:
                        return redirect(self.get_return_url(request, obj))

                except ObjectDoesNotExist:
                    msg = "Object save failed due to object-level permissions violation"
                    logger.debug(msg)
                    form.add_error(None, msg)

            else:
                logger.debug("Form validation failed")

            return render(request, self.template_name, {
                'obj': obj,
                'obj_type': self.queryset.model._meta.verbose_name,
                'form': form,
                'return_url': self.get_return_url(request, obj),
            })
        else: # create one announcement per each selection
            model = self.queryset.model
            # form = self.form(request.POST)
            model_form = self.model_form(request.POST)

            if model_form.is_valid():
                logger.debug("Form validation was successful")
                
                objects = []
                related_target = None
                # site
                if "related_site" in model_form.cleaned_data:
                    objects = model_form.cleaned_data['related_site']
                    related_target = "related_site"
                
                # device
                elif "related_device" in model_form.cleaned_data:
                    objects = model_form.cleaned_data['related_device']
                    related_target = "related_device"
                
                # vm
                elif "related_vm" in model_form.cleaned_data:
                    objects = model_form.cleaned_data['related_vm']
                    related_target = "related_vm"
                
                else:
                    pass
                
                new_objs = []

                try:
                    with transaction.atomic():

                        # Create objects from the expanded. Abort the transaction on the first validation error.
                        for value in objects:

                            # Reinstantiate the model form each time to avoid overwriting the same instance. Use a mutable
                            # copy of the POST QueryDict so that we can update the target field value.
                            model_form = self.model_form(request.POST.copy())
                            model_form.data[related_target] = value

                            # Validate each new object independently.
                            if model_form.is_valid():
                                obj = model_form.save()
                                logger.debug(f"Created {obj} (PK: {obj.pk})")
                                new_objs.append(obj)
                            else:
                                # Copy any errors on the pattern target field to the pattern form.
                                errors = model_form.errors.as_data()
                                if errors.get(related_target):
                                    form.add_error(
                                        'separate', errors[related_target])
                                # Raise an IntegrityError to break the for loop and abort the transaction.
                                raise IntegrityError()

                        # Enforce object-level permissions
                        if self.queryset.filter(pk__in=[obj.pk for obj in new_objs]).count() != len(new_objs):
                            raise ObjectDoesNotExist

                        # If we make it to this point, validation has succeeded on all new objects.
                        msg = "Added {} {}".format(
                            len(new_objs), model._meta.verbose_name_plural)
                        logger.info(msg)
                        messages.success(request, msg)

                        if '_addanother' in request.POST:
                            return redirect(request.path)
                        return redirect(self.get_return_url(request, None))

                except IntegrityError:
                    pass

                except ObjectDoesNotExist:
                    msg = "Object creation failed due to object-level permissions violation"
                    logger.debug(msg)
                    form.add_error(None, msg)

            else:
                logger.debug("Form validation failed")

            return render(request, self.template_name, {
                'form': model_form,
                'obj': None,
                'obj_type': self.queryset.model._meta.verbose_name,
                'return_url': self.get_return_url(request, None),
            })
        
class AnnouncementEditView(AnnouncementTemplateView):
    queryset = Announcement.objects.all()
    model_form = forms.AnnouncementEditForm
    template_name = 'netbox_announcement/announcement_edit.html'
   
    

class AnnouncementNetworkEditView(AnnouncementTemplateView):
    queryset = Announcement.objects.all()
    model_form = forms.AnnouncementNetworkEditForm
    template_name = 'netbox_announcement/announcement_edit_network.html'
    
    
class AnnouncementDeviceEditView(AnnouncementTemplateView):
    queryset = Announcement.objects.all()
    model_form = forms.AnnouncementDeviceEditForm
    template_name = 'netbox_announcement/announcement_edit_device.html'
    

class AnnouncementVMEditView(AnnouncementTemplateView):
    queryset = Announcement.objects.all()
    model_form = forms.AnnouncementVMEditForm
    template_name = 'netbox_announcement/announcement_edit_vm.html'

    
class AnnouncementDeleteView(ObjectDeleteView):
    queryset = Announcement.objects.all()
