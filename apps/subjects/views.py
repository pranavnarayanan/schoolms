from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from apps.subjects.forms import FORM_SubjectDetails, FORM_ClassNamesForSubject
from apps.subjects.models import EN_ClassSubjects
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties


def index(request):
    data = UIDataHelper(request).getData(page="is_list_all_subjects")
    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True)
    if user_role.exists():
        user_role = user_role.first()

        classes = EN_Classes.objects.filter(organization=user_role.related_organization)
        if request.method == "POST":
            if "class_names" in request.POST and "class_div" in request.POST:
                filter_class = request.POST["class_names"]
                filter_div = request.POST["class_div"]
                if filter_class != "all" and filter_div == "all":
                    classes = classes.filter(class_name=filter_class)
                elif filter_class == "all" and filter_div != "all" :
                    classes = classes.filter(class_division=filter_div)
                elif(filter_div != "all") :
                    classes = classes.filter(class_name=filter_class, class_division=filter_div)
                    if classes == None or not classes.exists() :
                        messages.error(request, "The given combination of class and division does not exist")

        dataList = []
        for classData in classes:
            subjects = EN_ClassSubjects.objects.filter(class_fk=classData)
            for subject in subjects :
                dataList.append({
                    "id": subject.id,
                    "name": subject.subject_name,
                    "duration": subject.duration,
                    "assigned_to_class": subject.class_fk.class_name+"-"+subject.class_fk.class_division
                })

        if dataList.__len__() == 0 :
            messages.error(request, "No subject exists for given combination of class and division")

        data.__setitem__("subjects", dataList)

        if request.method == "POST":
            fd_classes = FORM_ClassNamesForSubject(request.POST,request=request)
        else:
            fd_classes = FORM_ClassNamesForSubject(request=request)


        data.__setitem__("class_names",fd_classes)

        template = loader.get_template("sub_list_all_subjects.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.warning(request, DisplayKey.get("current_role_cannot_perform_this_action"))
        return HttpResponseRedirect("../Home")


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
