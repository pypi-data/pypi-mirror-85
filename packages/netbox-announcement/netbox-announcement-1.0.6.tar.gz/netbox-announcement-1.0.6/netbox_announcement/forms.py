from django import forms
from django.contrib.auth.models import User

from utilities.forms import (
    BootstrapMixin, DateTimePicker, DynamicModelChoiceField, CommentField, DynamicModelMultipleChoiceField, SlugField,
    SmallTextarea, StaticSelect2, APISelectMultiple, StaticSelect2Multiple,
    BOOLEAN_WITH_BLANK_CHOICES
)
from dcim.models import (
    Site, Device
)
from virtualization.models import VirtualMachine

from .models import Announcement, AnnouncementStatus, AnnouncementEmailPreConfig
from .choices import *
# 
# Announcement Form and Edit Form
# 
class AnnouncementFilterForm(BootstrapMixin, forms.Form):
    """
    Announcement Form
    """
    model = Announcement
    q = forms.CharField(
        required=False,
        label='Search'
    )
    created_at_after = forms.DateTimeField(
        label='After',
        required=False,
        widget=DateTimePicker()
    )
    created_at_before = forms.DateTimeField(
        label='Before',
        required=False,
        widget=DateTimePicker()
    )
    type = forms.MultipleChoiceField(
        choices=AnnouncementTypeChoices,
        required=False,
        widget=StaticSelect2Multiple()
    )
    user = DynamicModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        display_field='username',
        label='Author',
        widget=APISelectMultiple(
            api_url='/api/users/users/',
        )
    )
    status = DynamicModelMultipleChoiceField(
        queryset=AnnouncementStatus.objects.all(),
        required=False,
        display_field='status',
        label='Status',
        widget=APISelectMultiple(
            api_url='/api/plugins/announcement/status/',
        )
    )


class AnnouncementEditForm(BootstrapMixin, forms.ModelForm):
    """
    Announcement Edit Form
    """
    slug = SlugField(
        slug_source='subject'
    )
    content = CommentField(
        widget=SmallTextarea,
        label='Content',
        required=False
    )

    class Meta:
        model = Announcement
        fields = [
            'subject', 'slug', 'user', 'status', 'content_preset', 'type', 'content'
        ]


class AnnouncementNetworkEditForm(BootstrapMixin, forms.ModelForm):
    """
    Network Announcement Edit Form
    """
    slug = SlugField(
        slug_source='subject'
    )
    content = CommentField(
        widget=SmallTextarea,
        label='Content',
        
    )
    related_site = DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(),
        required=False,
        display_field='name',
        label='Related Sites',
        widget=APISelectMultiple(
            api_url='/api/dcim/sites/',
        )
    )

    class Meta:
        model = Announcement
        fields = [
            'subject', 'slug', 'user', 'status', 'content_preset', 'content', 
            'type', 
            'related_site'
        ]


class AnnouncementDeviceEditForm(BootstrapMixin, forms.ModelForm):
    """
    Server Device Announcement Edit Form
    """
    slug = SlugField(
        slug_source='subject'
    )
    content = CommentField(
        widget=SmallTextarea,
        label='Content',
    )
    related_device = DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(),
        required=False,
        display_field='name',
        label='Related Device',
        widget=APISelectMultiple(
            api_url='/api/dcim/devices/',
        )
    )
    
    class Meta:
        model = Announcement
        fields = [
            'subject', 'slug', 'user', 'status', 'content_preset', 'content',
            'type', 'server_type', 
            'related_device'
        ]


class AnnouncementVMEditForm(BootstrapMixin, forms.ModelForm):
    """
    Server VM Announcement Edit Form
    """
    slug = SlugField(
        slug_source='subject'
    )
    content = CommentField(
        widget=SmallTextarea,
        label='Content',

    )
    related_vm = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        display_field='name',
        label='Related VMs',
        widget=APISelectMultiple(
            api_url='/api/virtualization/virtual-machines/',
        )
    )

    class Meta:
        model = Announcement
        fields = [
            'subject', 'slug', 'user', 'status', 'content_preset', 'content',
            'type', 'server_type', 
            'related_vm'
        ]
