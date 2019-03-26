import json
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.books.models import EN_Books
from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from apps.subjects.forms import FORM_SubjectDetails, FORM_ClassNamesForSubject
from apps.subjects.models import EN_ClassSubjects, EN_SubjectTeachers
from apps.users.models import EN_Users
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties


def index(request):
    data = UIDataHelper(request).getData(page="is_list_all_subjects")
    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True)
    if user_role.exists():
        user_role = user_role.first()
        classes = EN_Classes.objects.filter(organization=user_role.related_organization)
        teachers = EN_UserRoles.objects.filter(related_organization=user_role.related_organization, role__code=Roles.TEACHER, approved=True)
        if not teachers.exists():
            messages.warning(request, "No Teachers added to this Organization.")
            teacherList = None
        else:
            teacherList = [{
                "id": teacher.id, #setting role_id, not user_id
                "name": teacher.user.name + " [" + teacher.user.product_id + "]"
            } for teacher in teachers]
        data.__setitem__("teachersList", teacherList)

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
                if not classes.exists():
                    messages.error(request, "No subject exists for given combination of class and division")

        dataList = None
        for classData in classes:
            subjects = EN_ClassSubjects.objects.filter(class_fk=classData)
            dataList = [{
                "id": subject.id,
                "name": subject.subject_name,
                "duration": subject.duration,
                "assigned_to_class": subject.class_fk.class_name+"-"+subject.class_fk.class_division
            } for subject in subjects ]
        data.__setitem__("subjects", dataList)

        fd_classes = FORM_ClassNamesForSubject(request.POST, request=request) if request.method == "POST" else FORM_ClassNamesForSubject(request=request)
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
    if request.is_ajax():
        if request.method == 'POST':
            subject_name = request.POST.get("subject_name")
            subject_duration = request.POST.get("subject_duration")
            classes_assigned = request.POST.get("classes_assigned")
            selected_books_id = request.POST.get("selected_books_id")

            userRole = EN_UserRoles.objects.filter(is_selected_role=True,role__code=Roles.SCHOOL_ADMIN)
            if(userRole.exists()):
                userRole = userRole.first()
                #TODO : -----------------
            else:
                status = False
                message = "Selected Roles does not have permission to perform this action"


            return HttpResponse("{}\n{}\n{}\n{}".format(subject_name,subject_duration,classes_assigned,selected_books_id))
            '''
            subjectObj = EN_ClassSubjects()
            subjectObj.subject_name = subjectName
            subjectObj.duration = subjectDuration
            subjectObj.organization = user_role.related_organization
            subjectObj.class_fk = classObj
            subjectObj.save()
            '''
        else:
            messages.warning(request, DisplayKey.get("error_not_a_post_request"))
            return HttpResponseRedirect("../Home")
    else:
        messages.warning(request, DisplayKey.get("error_not_ajax_request"))
        return HttpResponseRedirect("../Home")

@csrf_exempt
def getTeacherList(request) :
    if request.is_ajax():
        subject_id = request.POST["subject_id"]
        mainReturnList = {
            "teacherData" : []
        }
        returnList = []
        teacherList = EN_SubjectTeachers.objects.filter(subject_id=subject_id)
        for teacher in teacherList:
            rowDict = {
                "id": teacher.teacher.id,
                "name": teacher.teacher.name+"["+teacher.teacher.product_id+"]",
                "note": teacher.note
            }
            returnList.append(rowDict)
        mainReturnList.__setitem__('teacherData', returnList)
        jsonResponse = json.dumps(mainReturnList)
        return HttpResponse(jsonResponse)
    else:
        return HttpResponseRedirect("../Page404/")

@csrf_exempt
def saveNewTeacher(request) :
    if request.is_ajax():
        mainReturnList = {
            "status": False,
            "message": None
        }
        try:
            subject_id = int(request.POST.get("selected_subject_id"))
        except:
            mainReturnList["message"] = "No Subject Selected"
            return HttpResponse(json.dumps(mainReturnList))
        teacher_role_id = int(request.POST.get("selected_teacher_role_id"))
        note = request.POST["note"]
        my_current_role = EN_UserRoles.objects.get(is_selected_role=True,user_id=request.session[SessionProperties.USER_ID_KEY])
        user_role = EN_UserRoles.objects.get(approved=True, id = teacher_role_id, role__code=Roles.TEACHER, related_organization=my_current_role.related_organization)

        try:
            subjectTeacher = EN_SubjectTeachers()
            subjectTeacher.teacher = user_role.user
            subjectTeacher.subject_id = subject_id
            subjectTeacher.note = note
            subjectTeacher.organization = my_current_role.related_organization
            subjectTeacher.teacher_role = user_role
            subjectTeacher.save()
            mainReturnList["status"] = True
            mainReturnList["message"] = "Successfully added teacher to selected subject"
        except Exception as e:
            mainReturnList["message"] = e.__str__()
            mainReturnList["status"] = False
        jsonResponse = json.dumps(mainReturnList)
        return HttpResponse(jsonResponse)
    else:
        messages.warning(request,"Direct access denied")
        return HttpResponseRedirect("../Home")


def searchBooks(request):
    if request.is_ajax():
        if request.method == "POST":
            status = True
            message = ""
            search_key = request.POST.get("search_key")
            books = []
            if search_key == None or search_key=="":
                status = False
                message = "Search key should not be empty"
            else:
                books = EN_Books.objects.filter(Q(name__contains=search_key) | Q(book_code__contains=search_key))
                totalCount = books.count()
                if totalCount > 30:
                    status = False
                    message = "Filter using bookid. Result exceeds threshold {}"
            jsonRetData = {
                "status" : status,
                "message": message,
                "booksData" : [{
                    "id": book.id,
                    "name": book.name,
                    "volume": book.volume,
                    "book_code": book.book_code,
                    "author": book.author,
                    "publisher": book.publisher,
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
