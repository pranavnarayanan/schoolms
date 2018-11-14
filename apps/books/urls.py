from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Search Book"),
    path(r'AddBook',views.addBook, name="Add Book"),
    path(r'SaveBookDetails',views.saveBookDetails, name="Save Book Details"),
]