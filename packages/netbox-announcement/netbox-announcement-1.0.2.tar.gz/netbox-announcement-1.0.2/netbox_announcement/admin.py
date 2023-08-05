from django.contrib import admin
from .models import AnnouncementStatus, AnnouncementEmailPreConfig


@admin.register(AnnouncementStatus)
class AnnouncementStatusAdmin(admin.ModelAdmin):
    """
    Define Announcement Status
    """
    list_display=('status', 'status_label')


@admin.register(AnnouncementEmailPreConfig)
class AnnouncementEmailPreConfigAdmin(admin.ModelAdmin):
    """
    Define Announcement Email Pre config
    """
    list_display=('name', 'header', 'footer')
