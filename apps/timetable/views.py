from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from apps.roles.models import EN_UserRoles
from apps.school_timings.models import EN_SchoolTimings
from apps.utilities.helper.ui_data_helper import UIDataHelper
from properties.app_roles import Roles
from properties.session_properties import SessionProperties


def index(request):
    return HttpResponse("Index page")


def timetable(request):
    data = UIDataHelper(request).getData(page="is_add_timetable")
    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True, role__code=Roles.SCHOOL_ADMIN)
    if(user_role.exists()):
        user_role = user_role.first()
        timings = [{
            "id" : timing.id,
            "name" : timing.timing_name,
        }for timing in EN_SchoolTimings.objects.filter(organization=user_role.related_organization)]
        data.__setitem__("timings",timings)
        template = loader.get_template("tt_add_modify_timetable.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.warning(request,"You don't have privilage to perform this action")
        return HttpResponseRedirect("../Home")

