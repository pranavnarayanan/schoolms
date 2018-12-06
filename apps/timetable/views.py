from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.roles.models import EN_UserRoles
from apps.school_timings.models import EN_SchoolTimings
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties


def index(request):
    return HttpResponse("Index page")


def timetable(request):
    data = UIDataHelper(request).getData(page="is_add_school_timings")
    template = loader.get_template("tt_add_modify_timetable.html")
    return HttpResponse(template.render(data, request))
