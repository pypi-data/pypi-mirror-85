from django.urls import path
from . import views

urlpatterns = [
    path('announcements/', views.AnnouncementListView.as_view(),
         name='announcement_list'),
    path('announcements/add/', views.AnnouncementEditView.as_view(),
         name='announcement_add'),
    path('announcements/net_ann_add/', views.AnnouncementNetworkEditView.as_view(),
         name='announcement_network_add'),
    path('announcements/dev_ann_add/', views.AnnouncementDeviceEditView.as_view(),
         name='announcement_device_add'),
    path('announcements/vm_ann_add/', views.AnnouncementVMEditView.as_view(),
         name='announcement_vm_add'),
    path('announcements/<int:pk>/',
         views.AnnouncementView.as_view(), name='announcement'),
    path('announcements/<int:pk>/edit/',
         views.AnnouncementEditView.as_view(), name='announcement_edit'),
    path('announcements/<int:pk>/net_ann_edit/',
         views.AnnouncementNetworkEditView.as_view(), name='announcement_edit_network'),
    path('announcements/<int:pk>/dev_ann_edit/',
         views.AnnouncementDeviceEditView.as_view(), name='announcement_edit_device'),
    path('announcements/<int:pk>/vm_ann_edit/',
         views.AnnouncementVMEditView.as_view(), name='announcement_edit_vm'),
    path('announcements/<int:pk>/delete/',
         views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('announcements/<int:pk>/ann_update',
         views.AnnouncementUpdateView.as_view(), name='announcement_update'),
]
