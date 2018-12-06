from django.urls import path
from apps.timetable import views

urlpatterns = [
    path(r'',views.index, name="List All Timetables"),
    path(r'Add',views.timetable, name="Save New Task"),
]