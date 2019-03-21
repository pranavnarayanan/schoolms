from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Class Calendar"),
]