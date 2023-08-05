from django.contrib.auth.context_processors import PermWrapper

from extras.plugins import PluginTemplateExtension
from .models import Announcement

class DeviceAnnouncements(PluginTemplateExtension):
    """
    Display announcements on individual device page
    """
    model='dcim.device'
    
    def buttons(self):
        context = {
            'perms': PermWrapper(self.context['request'].user),
        }
        return self.render('netbox_announcement/device/announcementlist_btn.html', context)
    
    def left_page(self):
        # get latest 5 announcements
        announcements = Announcement.objects.filter(
            type='server', server_type='device', related_device=self.context['object'].id
        ).order_by('-updated_at')[:5]
        
        return self.render('netbox_announcement/device/latest_announcements.html', extra_context={'announcements': announcements})

class VMAnnouncements(PluginTemplateExtension):
    """
    Display announcements on individual virtual machine page
    """
    model = 'virtualization.virtualmachine'
    
    def buttons(self):
        context = {
            'perms': PermWrapper(self.context['request'].user),
        }
        return self.render('netbox_announcement/vm/announcementlist_btn.html', context)
    
    def left_page(self):
        # get latest 5 announcements
        announcements = Announcement.objects.filter(
            type='server', server_type='vm', related_vm=self.context['object'].id
        ).order_by('-updated_at')[:5]
        
        return self.render('netbox_announcement/vm/latest_announcements.html', extra_context={'announcements': announcements})

# PluginTemplateExtension subclasses must be package into an iterable named
# template_extensions to be imported by NetBox.
template_extensions = [DeviceAnnouncements, VMAnnouncements]
