from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="List all notifications"),
    path(r'LiveNotify',views.getLiveNotifications, name="Get Live Notifications"),
]