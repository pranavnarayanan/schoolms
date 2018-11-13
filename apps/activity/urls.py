from django.urls import path
from apps.activity import views

urlpatterns = [
    path(r'',views.index, name="Loads Notification Page"),
    path(r'GetMyNotifications', views.getMyNotifications,name="Get Notifications | AJAX For table"),

    path(r'LiveNotify', views.liveNotificationUpdate, name="Gets all unread messages and notifications | AJAX"),
]