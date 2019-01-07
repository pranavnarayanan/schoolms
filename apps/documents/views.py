import os
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.utilities.helper.ui_data_helper import UIDataHelper
from apps.documents.forms import FORM_Document
from apps.documents.models import EN_Documents
from properties.session_properties import SessionProperties

def index(request):
    template = loader.get_template("doc_list_my_documenst.html")
    data = UIDataHelper(request).getData(page="is_list_my_documents")
    data.__setitem__("form", FORM_Document(request.POST) if request.method == "POST" else FORM_Document() )
    folder_id = request.session["USED_DOCUMENT_FOLDER_ID"] if "USED_DOCUMENT_FOLDER_ID" in request.session else "ROOT"
    data.__setitem__("folder",folder_id)
    return HttpResponse(template.render(data, request))



def uploadDocument(request):
 if request.method=='POST':
    try:
        doc = EN_Documents()
        doc.data_file = request.FILES['file']
        doc.type = os.path.splitext(doc.data_file.name)[1]
        doc.name  = doc.data_file.name
        doc.uploaded_by_id = request.session[SessionProperties.USER_ID_KEY]
        doc.save()
        messages.success(request,"File uploaded successfully")
        request.method = "GET"
    except Exception as e:
        messages.warning(request,e.__str__())
    return index(request)
 else:
     messages.warning(request, "Direct access restricted")
     return HttpResponseRedirect("../Home")


@csrf_exempt
def loadFolderData(request):
    if request.is_ajax():
        id = request.POST.get("folder_id")
        if id == "ROOT":
            docs = EN_Documents.objects.filter(parent_folder=None)
        else:
            docs = EN_Documents.objects.filter(parent_folder=int(id))

        request.session["USED_DOCUMENT_FOLDER_ID"] = id
        return HttpResponse("Response Meow : ID is {}".format(id))
    else:
        messages.warning(request, "Direct access restricted")
        return HttpResponseRedirect("../Home")
