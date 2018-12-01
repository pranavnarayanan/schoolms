from django.http import HttpResponse
from django.template import loader
from apps.utilities.helper.ui_data_helper import UIDataHelper
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from apps.documents.forms import documentform
from apps.documents.models import EN_Documents

def index(request):
    template = loader.get_template("doc_list_my_documenst.html")
    data = UIDataHelper(request).getData(page="is_list_my_documents")
    return HttpResponse(template.render(data, request))

def uploadNewFile(request):
    return HttpResponse("Page to upload new document")
def upload(request):
    template = loader.get_template("doc_list_my_documenst.html")
    data = {
        "form": documentform()
    }
    return HttpResponse(template.render(data, request))
def uploaddocument(request):
 if request.method=='POST':

    newdo = EN_Documents(file_name=request.FILES['file'],type='uddddddddddl',unique_name='kul',uploaded_by_id=2)
    newdo.save()
    return HttpResponse("sussessful")
