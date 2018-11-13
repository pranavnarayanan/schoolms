from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Renders Roles Home Page - Lists all active roles of user"),
]