from django.http import HttpResponse
from django.template import loader
from apps.utilities.helper.ui_data_helper import UIDataHelper

def index(request):
    template = loader.get_template("doc_list_my_documenst.html")
    data = UIDataHelper(request).getData(page="is_list_my_documents")
    return HttpResponse(template.render(data, request))

def uploadNewFile(request):
    return HttpResponse("Page to upload new document")
