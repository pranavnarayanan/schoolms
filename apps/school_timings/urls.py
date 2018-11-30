from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="School Timings Home Page"),
    path(r'AddTiming',views.addSchoolTimings, name="Add New School Timing"),
    path(r'SubmitSchoolTimings',views.submitSchoolDetails, name="New School Timing Submit Page"),
]

