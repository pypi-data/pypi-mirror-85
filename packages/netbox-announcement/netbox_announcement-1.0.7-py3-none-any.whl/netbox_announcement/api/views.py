from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import APIRootView
from rest_framework.response import Response
from netbox_announcement.models import Announcement, AnnouncementStatus, AnnouncementUpdate
from .serializers import AnnouncementSerializer, AnnouncementStatusSerializer, AnnouncementUpdateSerializer
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


class AnnouncementUpdateViewSet(ModelViewSet):
    queryset = AnnouncementUpdate.objects.all()
    serializer_class = AnnouncementUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.data
        exist_status_field = True if "status" in data else False
        
        status = None
        if exist_status_field:
            request_data = data.copy()
            status = request_data.pop('status')[0]

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            if not status is None:
                announcement = Announcement.objects.get(id=data['announcement'])
                status_obj = AnnouncementStatus.objects.get(id=status)
                announcement.status = status_obj
                announcement.save()

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
        
