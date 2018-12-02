from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="List School Subjects Page"),
    path(r'AddSubject',views.addSubject, name="Add New School Subject"),
    path(r'SaveSubject',views.saveSubject, name="Save New Subject"),
]

