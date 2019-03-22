import json
from math import floor, ceil
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from apps.books.forms import FORM_BookDetails
from apps.books.models import EN_Books, TL_BooksCategory, TL_BooksSubCategory
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey


def index(request):
    data = UIDataHelper(request).getData(page="is_books")
    data.__setitem__("is_add_new_book", "active")
    data.__setitem__("categories",[{
        "code" : category.code,
        "name" : category.name,
    }for category in TL_BooksCategory.objects.all()])
    template = loader.get_template("books_search_book.html")
    return HttpResponse(template.render(data, request))

def loadSubCategories(request):
    if request.is_ajax():
        data = [{
            "code": sub_category.code,
            "name": sub_category.name,
        } for sub_category in TL_BooksSubCategory.objects.filter(category__code=request.POST["category"])]
        return HttpResponse(json.dumps(data))
    else:
        messages.warning(request,"Direct Access Deneed")
        return HttpResponseRedirect("../Home")

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
            if request.POST.get("book_sub_category") != "" and request.POST.get("book_sub_category") != None:
                bookObj.sub_category = TL_BooksSubCategory.objects.get(code=request.POST.get("book_sub_category"))
            bookObj.save()
            messages.success(request, DisplayKey.get("book_added_successfully"))
            return HttpResponseRedirect("../Books")
        else:
            return addBook(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")

def searchBooks(request):
    if request.is_ajax():
        if request.method == "POST":
            status = True
            message = ""
            book_id_or_name = request.POST.get("book_id_or_name")
            book_author = request.POST.get("book_author")
            book_pubilisher = request.POST.get("book_pubilisher")
            book_published_year = request.POST.get("book_published_year")
            book_category = request.POST.get("book_category")
            book_sub_category = request.POST.get("book_sub_category")
            try:
                page = int(request.POST.get("page_no"))
            except:
                page = 1
                status=False
                message = "Invalid Page number"
            books = EN_Books.objects
            filter = False
            if book_id_or_name != "":
                books = books.filter(Q(name__contains=book_id_or_name) | Q(book_code__contains=book_id_or_name))
                filter = True
            if book_author != "":
                books = books.filter(author__contains=book_author)
                filter = True
            if book_pubilisher != "":
                books = books.filter(publisher__contains=book_pubilisher)
                filter = True
            if book_published_year != "":
                try:
                    book_published_year = int(book_published_year)
                    books = books.filter(published_year=book_published_year)
                    filter = True
                except:
                    status =  False
                    message = "Published year should be a number"
            if book_category != "None":
                books = books.filter(category__code__exact=book_category)
                filter = True
            if book_sub_category != "None" and book_sub_category != "all":
                books = books.filter(sub_category__code__exact=book_sub_category)
                filter = True

            if not filter:
                books = books.all()

            totalCount = books.count()
            perPageDataLimit = 2
            if page > int(ceil(totalCount/perPageDataLimit)):
                page = 1
            books = books[((page*perPageDataLimit)-perPageDataLimit):(page*perPageDataLimit)]

            jsonRetData = {
                "status" : status,
                "message": message,
                "page_count": ceil(totalCount/perPageDataLimit),
                "current_page": page,
                "booksData" : [{
                    "id": book.id,
                    "name": book.name,
                    "code": book.book_code,
                    "volume": book.volume,
                    "book_code": book.book_code,
                    "author": book.author,
                    "publisher": book.publisher,
                    "published_year": book.published_year,
                    "category": book.category.name,
                    "sub_category": None if book.sub_category == None else book.sub_category.name,
                } for book in books]
            }
            return HttpResponse(json.dumps(jsonRetData))
        else:
            messages.warning(request,DisplayKey.get("error_not_a_post_request"))
    else:
        messages.warning(request, DisplayKey.get("error_not_ajax_request"))
    return HttpResponseRedirect("../Home")
