from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="User Home Page"),
    path(r'ChangeUsername',views.changeUsername, name="Change Username"),
    path(r'ChangePassword',views.changePassword, name="Change Password"),
]

