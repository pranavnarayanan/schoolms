import json
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from apps.books.models import EN_Books
from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from apps.subjects.forms import FORM_SubjectDetails, FORM_ClassNamesForSubject
from apps.subjects.models import EN_Subjects, EN_SubjectTeachers, EN_SubjectBooks, EN_ClassSubjects
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
                elif filter_class != "all" and filter_div != "all":
                    classes = classes.filter(class_name=filter_class, class_division=filter_div)
                if not classes.exists():
                    messages.error(request, "The given combination of class and division does not exist")

        dataList = None

        dataList = [{
            "id": cs.subject.id,
            "name": cs.subject.subject_name,
            "duration": cs.subject.duration,
            "assigned_to_class": cs.class_fk.class_name + "-" + cs.class_fk.class_division
        }for cs in EN_ClassSubjects.objects.filter(class_fk__in=list(classes))]
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
            tag = request.POST.get("subject_tag")
            classes_assigned = request.POST.get("classes_assigned")
            selected_books_id = request.POST.get("selected_books_id")

            status = True
            message = ""

            userRole = EN_UserRoles.objects.filter(approved=True, is_selected_role=True,role__code=Roles.SCHOOL_ADMIN)
            if(userRole.exists()):
                userRole = userRole.first()
                organization = userRole.related_organization

                #Validating Classes
                for cls in classes_assigned.split(","):
                    try:
                        cls = EN_Classes.objects.filter(id=int(cls))
                        if not cls.exists():
                            raise Exception("Class {}-{} doesnot exist".format(cls.first().class_name, cls.first().class_division))
                        elif cls.first().organization.id != organization.id:
                            raise Exception("Class {}-{} doesnot belong to the organization where your current role is set to".format(cls.first().class_name,cls.first().class_division))
                    except Exception as e:
                        status = False
                        message = e.__str__()
                        break

                #Validating Books
                for book in selected_books_id.split(","):
                    try:
                        EN_Books.objects.get(id=int(book))
                    except Exception as e:
                        status = False
                        message = e.__str__()
                        break

                if status:
                    subjectObj = EN_Subjects()
                    subjectObj.subject_name = subject_name
                    subjectObj.tag = tag
                    try:
                        subjectObj.duration = int(subject_duration) if subject_duration != None or subject_duration != "" else None
                    except:
                        subjectObj.duration = None
                    subjectObj.organization = organization
                    subjectObj.save()

                    for cls in classes_assigned.split(","):
                        cs = EN_ClassSubjects()
                        cs.subject = subjectObj
                        cs.class_fk_id = int(cls)
                        cs.organization = organization
                        cs.save()

                    for book_id in selected_books_id.split(","):
                        sb = EN_SubjectBooks()
                        sb.book_id = int(book_id)
                        sb.organization = organization
                        sb.subject = subjectObj
                        sb.save()

                    message = "Subjects Saved Successfully"
            else:
                status = False
                message = "Selected Roles does not have permission to perform this action"
            return HttpResponse(json.dumps({"status" : status,"message" : message}))
        else:
            messages.warning(request, DisplayKey.get("error_not_a_post_request"))
            return HttpResponseRedirect("../Home")
    else:
        messages.warning(request, DisplayKey.get("error_not_ajax_request"))
        return HttpResponseRedirect("../Home")


def getTeacherList(request) :
    if request.is_ajax():
        subject_id = request.POST["subject_id"]
        mainReturnList = {
            "teacherData" : []
        }
        returnList = []
        teacherList = EN_SubjectTeachers.objects.filter(id=int(subject_id))
        for teacher in teacherList:
            rowDict = {
                "id": teacher.teacher.id,
                "name": teacher.teacher.name+" &nbsp;&nbsp; ["+teacher.teacher.product_id+"]",
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
        my_current_role = EN_UserRoles.objects.get(approved=True, is_selected_role=True,user_id=request.session[SessionProperties.USER_ID_KEY])
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
