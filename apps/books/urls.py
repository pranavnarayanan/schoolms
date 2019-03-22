from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Search Book"),
    path(r'LoadSubCategories',views.loadSubCategories, name="Load Sub Categories from category selected"),
    path(r'AddBook',views.addBook, name="Add Book"),
    path(r'SaveBookDetails',views.saveBookDetails, name="Save Book Details"),
    path(r'SearchBooks',views.searchBooks, name="Search Book"),
]