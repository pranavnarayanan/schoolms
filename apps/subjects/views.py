from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.classes.models import EN_Classes
from apps.subjects.forms import FORM_SubjectDetails
from apps.subjects.models import EN_ClassSubjects
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey


def index(request):
    data = UIDataHelper(request).getData(page="is_subjects")
    data.__setitem__("is_list_subjects", "active")
    template = loader.get_template("sub_list_all_subjects.html")
    return HttpResponse(template.render(data, request))


def addSubject(request):
    data = UIDataHelper(request).getData(page="is_add_subjects")
    data.__setitem__("form", FORM_SubjectDetails(request.POST, request=request) if request.method == "POST" else FORM_SubjectDetails(request=request))
    template = loader.get_template("sub_add_new_subject.html")
    return HttpResponse(template.render(data, request))


def saveSubject(request):
    if request.method == 'POST':
        form_data = FORM_SubjectDetails(request.POST, request=request)
        if (form_data.is_valid()):
            subjectName = form_data.cleaned_data.get("subject_name")
            subjectDuration = form_data.cleaned_data.get("subject_duration")
            classId = form_data.cleaned_data.get("assign_to_class")
            for id in classId :
                classObj = EN_Classes.objects.get(id = id)
                subjectObj = EN_ClassSubjects()
                subjectObj.subject_name = subjectName
                subjectObj.duration = subjectDuration
                subjectObj.class_fk = classObj
                subjectObj.save()
            messages.success(request, DisplayKey.get("success_added_subject"))
            return HttpResponseRedirect("../Subjects")
        else:
            return index(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")
