from django.urls import path
from apps.classes import views

urlpatterns = [
    path(r'',views.index, name="Lists Classes Of An Organization"),
    path(r'AddNewClass',views.addNewClass, name="Add New Class"),
    path(r'SaveClass',views.saveClassDetails, name="Save Class Details"),
]