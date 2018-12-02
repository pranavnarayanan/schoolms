from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from apps.classes.forms import FORM_ClassDetails
from apps.classes.models import EN_Classes
from apps.organization.models import TL_InstitutionLevels
from apps.roles.models import EN_UserRoles
from apps.school_timings.models import EN_SchoolTimings
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties


def index(request):
    data = UIDataHelper(request).getData(page="is_classes")
    data.__setitem__("is_list_all_classes", "active")
    template = loader.get_template("classes_list_all_classes.html")
    return HttpResponse(template.render(data, request))

def addNewClass(request):
    data = UIDataHelper(request).getData(page="is_classes")
    data.__setitem__("is_add_new_class", "active")
    data.__setitem__("form", FORM_ClassDetails(request.POST) if request.method == "POST" else FORM_ClassDetails())
    template = loader.get_template("classes_add_new_class.html")
    return HttpResponse(template.render(data, request))

def saveClassDetails(request):
    if request.method == 'POST':
        form_data = FORM_ClassDetails(request.POST)
        if (form_data.is_valid()):
            user_id = request.session[SessionProperties.USER_ID_KEY]
            organization = EN_UserRoles.objects.filter(user_id=user_id, is_selected_role=True, approved=True)
            if(organization.exists()) :
                organization = organization.first()
                classObj = EN_Classes()
                classObj.class_name = form_data.cleaned_data.get("class_name")
                classObj.batch_nick_name = form_data.cleaned_data.get("class_nickname")
                classObj.academic_starting_year = form_data.cleaned_data.get("class_start_date")
                classObj.academic_ending_year = form_data.cleaned_data.get("class_end_date")
                classObj.batch_name = classObj.academic_starting_year.year.__str__() + "-" +classObj.academic_ending_year.year.__str__()#form_data.cleaned_data.get("class_batch")
                classObj.organization = organization.related_organization
                classObj.organization_level = TL_InstitutionLevels.objects.get(code=form_data.cleaned_data.get("institution_levels"))
                timePattern = form_data.cleaned_data.get("class_time_pattern")
                classObj.timing = EN_SchoolTimings.objects.get(id=1)
                classObj.save()
                messages.success(request, DisplayKey.get("success_added_class"))
                return HttpResponseRedirect("../Classes")
            else:
                messages.error(request, DisplayKey.get("current_role_doesnot_have_permission_to_do_this_action"))
                return index(request)
        else:
            return index(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")
