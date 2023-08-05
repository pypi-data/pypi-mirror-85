from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from utilities.querysets import RestrictedQuerySet
from .choices import *

class AnnouncementStatus(models.Model):
    """
    Announcement Status model
    """
    STATUS_LABEL_CHOICES = (
        ('success', 'Green'),
        ('primary', 'Blue'),
        ('info', 'Cyan'),
        ('warning', 'Orange'),
        ('danger', 'Red')
    )
    status = models.CharField(
        max_length=50
    )
    status_label = models.CharField(
        max_length=10, 
        choices=STATUS_LABEL_CHOICES
    )
    
    class Meta:
        managed=True
        verbose_name='Announcement Status'
        verbose_name_plural = 'Announcement Statuses'
        
    def __str__(self):
        return self.status
    
class AnnouncementEmailPreConfig(models.Model):
    """
    Annoucement email preconfig header and footer model
    """
    name=models.CharField(
        max_length=255
    )
    header=models.TextField(
        blank=True, 
        null=True
    )
    footer=models.TextField(
        blank=True,
        null=True
    )
    
    class Meta:
        managed=True
        verbose_name = 'Announcement Email Preconfig'
        verbose_name_plural = 'Announcement Email Preconfigs'
    
    def __str__(self):
        return self.name
        
        
class Announcement(models.Model):
    """
    Announcement Model
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='announcement',
        blank=True,
        null=True
    )
    subject = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    content = models.TextField(
        blank=True,
        null=True,
    )
    mailed = models.BooleanField(
        default=False,
        verbose_name='Has mailed',
        help_text='Indicate whether mailer script has mailed this announcement'
    )
    type = models.CharField(
        max_length=50,
        choices=AnnouncementTypeChoices,
        default=AnnouncementTypeChoices.TYPE_COMPANY
    )
    server_type = models.CharField(
        max_length=10,
        choices=AnnouncementServerTypeChoices,
        blank=True,
        null=True
    )
    related_site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name='announcements',
        blank=True,
        null=True
    )
    related_device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.PROTECT,
        related_name='announcements',
        blank=True,
        null=True
    )
    related_vm = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.PROTECT,
        related_name='announcements',
        blank=True,
        null=True
    )
    # status = models.CharField(
    #     max_length=50,
    #     choices=AnnouncementStatusChoices,
    #     default=AnnouncementStatusChoices.STATUS_IN_PROGRESS
    # )
    status=models.ForeignKey(
        to=AnnouncementStatus,
        on_delete=models.PROTECT,
    )
    content_preset = models.ForeignKey(
        to=AnnouncementEmailPreConfig,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        editable=True,
        db_index=True
    )
    slug = models.SlugField(
        unique=True
    )

    TYPE_CLASS_MAP = {
        AnnouncementTypeChoices.TYPE_COMPANY: 'info',
        AnnouncementTypeChoices.TYPE_NETWORK: 'primary',
        AnnouncementTypeChoices.TYPE_SERVER: 'success'
    }
    objects = RestrictedQuerySet.as_manager()
    
    class Meta:
        ordering=["-created_at"]
    
    def __str__(self):
        return self.subject
    
    def get_absolute_url(self):
        return reverse("plugins:netbox_announcement:announcement", kwargs={"pk": self.pk})
    
    def get_type_class(self):
        return self.TYPE_CLASS_MAP.get(self.type)

class AnnouncementUpdate(models.Model):
    """
    Announcement Updates model
    """
    announcement = models.ForeignKey(
        to=Announcement,
        on_delete=models.SET_NULL,
        related_name='announcement_update',
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='announcement_update',
        blank=True,
        null=True
    )
    content = models.TextField(
        blank=True,
        null=True,
    )
    mailed = models.BooleanField(
        default=False,
        verbose_name='Has mailed',
        help_text='Indicate whether mailer script has mailed this announcement update'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        db_index=True
    )
    # slug = models.SlugField(
    #     unique=True
    # )
    
    objects = RestrictedQuerySet.as_manager()
    
    class Meta:
        ordering = ["-created_at"]
        
