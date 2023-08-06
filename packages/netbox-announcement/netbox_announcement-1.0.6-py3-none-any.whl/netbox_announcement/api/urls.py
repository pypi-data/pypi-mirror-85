from rest_framework import routers
from .views import AnnouncementsRootView, AnnouncementViewSet, AnnouncementStatusViewSet


router = routers.DefaultRouter()
router.APIRootView = AnnouncementsRootView

router.register('announcments', AnnouncementViewSet)
router.register('status', AnnouncementStatusViewSet)

app_name = 'netbox_announcement-api'
urlpatterns = router.urls
