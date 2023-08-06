from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import APIRootView
from rest_framework.response import Response
from netbox_announcement.models import Announcement, AnnouncementStatus
from .serializers import AnnouncementSerializer, AnnouncementStatusSerializer
from netbox_announcement import filters


class AnnouncementsRootView(APIRootView):
    """
    Announcement API root view
    """

    def get_view_name(self):
        return 'Announcement'


class AnnouncementViewSet(ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class AnnouncementStatusViewSet(ModelViewSet):
    queryset = AnnouncementStatus.objects.all()
    serializer_class = AnnouncementStatusSerializer
