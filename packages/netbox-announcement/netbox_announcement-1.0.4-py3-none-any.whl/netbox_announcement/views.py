from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import transaction
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
