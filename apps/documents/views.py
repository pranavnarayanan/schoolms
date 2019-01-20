import os
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from apps.utilities.entities.sequenceutil import EN_SequenceUtil
from apps.utilities.helper.ui_data_helper import UIDataHelper
from apps.documents.forms import FORM_Document
from apps.documents.models import EN_Documents
from properties.session_properties import SessionProperties
from apps.documents.helper import DocumentHelper

def index(request):
    template = loader.get_template("doc_list_my_documenst.html")
    data = UIDataHelper(request).getData(page="is_list_my_documents")
    data.__setitem__("form", FORM_Document(request.POST) if request.method == "POST" else FORM_Document() )
    folder_id = request.session["USED_DOCUMENT_FOLDER_ID"] if "USED_DOCUMENT_FOLDER_ID" in request.session else "ROOT"
    data.__setitem__("folder",folder_id)
    user_id=request.session[SessionProperties.USER_ID_KEY]

    if not EN_Documents.objects.filter(owner=user_id, name="ROOT", is_root = True).exists():
        DocumentHelper().createRootEntry(user_id)

    return HttpResponse(template.render(data, request))



def uploadDocument(request):
 if request.method=='POST':
    try:
        doc = EN_Documents()
        doc.data_file = request.FILES['file']
        doc.type = os.path.splitext(doc.data_file.name)[1]
        doc.name  = doc.data_file.name
        doc.is_file=True
        doc.is_folder=False
        if "ROOT" == request.session["USED_DOCUMENT_FOLDER_ID"]:
            doc.parent_folder = EN_Documents.objects.get(is_folder=True, is_file=False, name="ROOT",owner=request.session[SessionProperties.USER_ID_KEY])
        else:
            doc.parent_folder_id = int(request.session["USED_DOCUMENT_FOLDER_ID"])
        doc.unique_name = "file_{}{}".format(EN_SequenceUtil.next("UNIQUE_FILE_NAME"),doc.type)
        doc.owner_id = request.session[SessionProperties.USER_ID_KEY]
        doc.save()
        messages.success(request,"File uploaded successfully")
        request.method = "GET"
    except Exception as e:
        messages.warning(request,e.__str__()),
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


@csrf_exempt
def createfolder(request):
    if request.is_ajax():
        try:
            doc=EN_Documents()
            if "ROOT" == request.session["USED_DOCUMENT_FOLDER_ID"]:
                doc.parent_folder = EN_Documents.objects.get(is_folder=True,is_file=False, name="ROOT", owner=request.session[SessionProperties.USER_ID_KEY])
            else:
                doc.parent_folder_id = int(request.session["USED_DOCUMENT_FOLDER_ID"])
            doc.is_file = False
            doc.is_folder = True
            doc.type = "folder"
            doc.unique_name = "folder_{}".format(EN_SequenceUtil.next("UNIQUE_FILE_NAME"))
            doc.name = request.POST.get("folder_name")
            doc.owner_id = request.session[SessionProperties.USER_ID_KEY]
            doc.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(e.__str__())
    else:
        messages.warning(request,"Direct Access Denied")
        return HttpResponseRedirect("../Home")