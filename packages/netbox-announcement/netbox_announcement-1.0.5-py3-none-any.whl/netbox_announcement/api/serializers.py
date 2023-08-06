from rest_framework.serializers import ModelSerializer
from netbox_announcement.models import Announcement, AnnouncementStatus

class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('id', 'user', 'subject', 'content', 'mailed', 'type', 'server_type',
                  'related_site', 'related_device', 'related_vm', 'status', 'slug')

class AnnouncementStatusSerializer(ModelSerializer):
    class Meta:
        model = AnnouncementStatus
        fields = ('id', 'status', 'status_label')