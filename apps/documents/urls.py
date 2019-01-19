from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="List all files uploaded by user "),
    path(r'Upload', views.uploadDocument, name="Validate and Upload Document"),

    path(r'LoadFolderData', views.loadFolderData, name="Load Folder Data | Ajax"),
    path(r'Createfolder',views.createfolder,name="createfolder - Ajax")
]