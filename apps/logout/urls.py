from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Clears the session and redirects to login page"),
]