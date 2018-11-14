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
            book_name = form_data.cleaned_data.get("book_name")
            book_code = form_data.cleaned_data.get("book_code")
            book_volume = form_data.cleaned_data.get("book_volume")
            book_author = form_data.cleaned_data.get("book_author")
            book_publisher = form_data.cleaned_data.get("book_publisher")
            book_category = form_data.cleaned_data.get("book_category")
            book_sub_category = form_data.cleaned_data.get("book_sub_category")
            book_year = form_data.cleaned_data.get("book_year")
            bookObj = EN_Books()
            bookObj.name = book_name
            bookObj.book_code = book_code
            bookObj.published_year = book_year
            bookObj.volume = book_volume
            bookObj.author = book_author
            bookObj.publisher = book_publisher
            bookObj.category = TL_BooksCategory.objects.get(code=book_category)
            bookObj.sub_category = TL_BooksSubCategory.objects.get(code=book_sub_category)
            bookObj.save()
            messages.success(request, DisplayKey.get("book_added_successfully"))
            return HttpResponseRedirect("../Books")
        else:
            return addBook(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")

