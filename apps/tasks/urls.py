from django.urls import path
from apps.tasks import views

urlpatterns = [
    path(r'',views.index, name="List All Pending Notes"),
    path(r'SaveTask',views.SaveTask, name="Save New Task"),
]