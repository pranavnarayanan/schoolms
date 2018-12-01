from django.urls import path
from . import views

urlpatterns = [

    path(r'',views.index, name="List all files uploaded by user "),
    path(r'upload', views.upload, name="Upload New Document"),
    path(r'uploaddocument',views.uploaddocument, name="ddd")

]