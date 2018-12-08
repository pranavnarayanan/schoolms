from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.books.forms import FORM_BookDetails
from apps.books.models import EN_Books, TL_BooksCategory, TL_BooksSubCategory
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey


def index(request):
    data = UIDataHelper(request).getData(page="is_books")
    data.__setitem__("is_add_new_book", "active")
    template = loader.get_template("books_search_book.html")
    return HttpResponse(template.render(data, request))


def addBook(request):
    data = UIDataHelper(request).getData(page="is_books")
    data.__setitem__("is_add_new_book", "active")
    data.__setitem__("form", FORM_BookDetails(request.POST) if request.method == "POST" else FORM_BookDetails())
    template = loader.get_template("books_add_new_book.html")
    return HttpResponse(template.render(data, request))

def saveBookDetails(request):
    if request.method == 'POST':
        form_data = FORM_BookDetails(request.POST)
        if (form_data.is_valid()):
            bookObj = EN_Books()
            bookObj.name = form_data.cleaned_data.get("book_name")
            bookObj.book_code = form_data.cleaned_data.get("book_code")
            bookObj.published_year = form_data.cleaned_data.get("book_year")
            bookObj.volume = form_data.cleaned_data.get("book_volume")
            bookObj.author = form_data.cleaned_data.get("book_author")
            bookObj.publisher = form_data.cleaned_data.get("book_publisher")
            bookObj.category = TL_BooksCategory.objects.get(code=form_data.cleaned_data.get("book_category"))
            bookObj.sub_category = TL_BooksSubCategory.objects.get(code=form_data.cleaned_data.get("book_sub_category"))
            bookObj.save()
            messages.success(request, DisplayKey.get("book_added_successfully"))
            return HttpResponseRedirect("../Books")
        else:
            return addBook(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")

