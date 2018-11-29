from django.urls import path
from . import views

urlpatterns = [

    path(r'',views.index, name="List all files uploaded by user "),
    path(r'Upload', views.uploadNewFile, name="Upload New Document"),

]