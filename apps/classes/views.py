from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.classes.forms import FORM_ClassDetails, FORM_ClassNames
from apps.classes.models import EN_Classes
from apps.organization.models import TL_InstitutionLevels
from apps.roles.models import EN_UserRoles
from apps.school_timings.models import EN_SchoolTimings
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties


def index(request, is_add_new_class = False):
    data = UIDataHelper(request).getData(page="is_list_all_classes")
    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role = EN_UserRoles.objects.filter(Q(role__code=Roles.SCHOOL_ADMIN) | Q(role__code=Roles.PRINCIPAL),
                                            approved=True, user_id=user_id, is_selected_role=True)
    if user_role.exists():
        user_role = user_role.first()

        classes = EN_Classes.objects.filter(organization=user_role.related_organization)
        if request.method == "POST":
            if "class_names" in request.POST:
                filter_class = request.POST["class_names"]
                if filter_class != "all":
                    classes = classes.filter(class_name=filter_class)

        dataList = []
        for classData in classes:
            dataList.append({
                "name" : classData.class_name,
                "division":classData.class_division if(classData.class_division != None and classData.class_division != "") else "-",
                "nickname":classData.batch_nick_name if(classData.batch_nick_name != None and classData.batch_nick_name != "") else "-",
                "start_date":classData.academic_starting_year,
                "end_date":classData.academic_ending_year,
                "batch":classData.batch_name,
                "class_teacher":classData.class_teacher.name if(classData.class_teacher != None) else "-",
            })

        data.__setitem__("classes",dataList)
        data.__setitem__("is_add_new_class",is_add_new_class)

        if request.method == "POST":
            if "class_names" in request.POST:
                fd_cls_details = FORM_ClassDetails(request=request)
                fd_classes = FORM_ClassNames(request.POST,request=request)
            else:
                fd_cls_details = FORM_ClassDetails(request.POST,request=request)
                fd_classes = FORM_ClassNames(request.POST,request=request)
        else:
            fd_cls_details = FORM_ClassDetails(request=request)
            fd_classes = FORM_ClassNames(request=request)

        data.__setitem__("form",fd_cls_details)
        data.__setitem__("class_names",fd_classes)

        template = loader.get_template("classes_list_all_classes.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.warning(request, DisplayKey.get("current_role_cannot_perform_this_action"))
        return HttpResponseRedirect("../Home")


def saveClassDetails(request):
    if request.method == 'POST':
        form_data = FORM_ClassDetails(request.POST, request=request)
        if (form_data.is_valid()):
            user_id = request.session[SessionProperties.USER_ID_KEY]
            organization = EN_UserRoles.objects.filter(user_id=user_id, is_selected_role=True, approved=True)
            if(organization.exists()) :
                organization = organization.first()

                divisions = form_data.cleaned_data.get("class_division")
                timing = EN_SchoolTimings.objects.get(id=int(form_data.cleaned_data.get("class_time_pattern")))
                for div in divisions.split(","):
                    if not (div.strip() == "" or div.strip() == None):
                        classObj = EN_Classes()
                        classObj.class_name = form_data.cleaned_data.get("class_name")
                        classObj.class_division = div.strip().upper()
                        classObj.batch_nick_name = form_data.cleaned_data.get("class_nickname")
                        classObj.academic_starting_year = form_data.cleaned_data.get("class_start_date")
                        classObj.academic_ending_year = form_data.cleaned_data.get("class_end_date")
                        classObj.batch_name = classObj.academic_starting_year.year.__str__() + "-" +classObj.academic_ending_year.year.__str__()#form_data.cleaned_data.get("class_batch")
                        classObj.organization = organization.related_organization
                        classObj.organization_level = TL_InstitutionLevels.objects.get(code=form_data.cleaned_data.get("institution_levels"))
                        classObj.timing = timing
                        classObj.save()
                messages.success(request, DisplayKey.get("success_added_class"))
                return HttpResponseRedirect("../Classes")
            else:
                messages.error(request, DisplayKey.get("current_role_doesnot_have_permission_to_do_this_action"))
                return index(request)
        else:
            return index(request,True)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")
