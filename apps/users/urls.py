from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="User Profile"),
    path(r'ChangeOnlineStatus',views.changeOnlineStatus, name="Change Online Status"),
]