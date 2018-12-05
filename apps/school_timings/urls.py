from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="School Timings Home Page"),

    path(r'AddModifyTiming',views.addSchoolTimings_Page1, name="Add/Modify School Timing "),
    path(r'AddModifyTimingSubmit',views.addSchoolTimings_Page1_Submit, name="New School Timing Submit Page"),

    path(r'TimingDetails',views.addSchoolTimings_Page2, name="Add New School Timing Details"),
    path(r'TimingDetailsSubmit',views.addSchoolTimings_Page2_Submit, name="Add New School Timing Details"),

    path(r'TimingBreakup', views.addSchoolTimings_Page3, name="Timing Breakup Page"),
    path(r'LoadBreakUpData', views.addSchoolTimings_loadBreakUpData, name="AJAX | Load Break UpData based on timing selected"),


]

