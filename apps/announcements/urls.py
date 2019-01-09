from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Announcements Home Page"),
    path(r'Create',views.create, name="Create New Announcement"),
]