import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.announcements.forms import FORM_Announcements
from apps.organization.models import EN_Organization, EN_OrganizationGroup
from apps.utilities.helper.ui_data_helper import UIDataHelper

def index(request):
    template = loader.get_template("announcements_home.html")
    data = UIDataHelper(request).getData(page="is_announcements_home")
    return HttpResponse(template.render(data, request))

def create(request):
    template = loader.get_template("announcements_create.html")
    data = UIDataHelper(request).getData(page="is_create_announcement")
    data.__setitem__("form", FORM_Announcements(request.POST, request=request) if request.method == "POST" else FORM_Announcements(request=request))
    return HttpResponse(template.render(data, request))

def loadOrgList(request):
    if request.is_ajax():
        orgGrp = EN_OrganizationGroup.objects.get(id=request.POST["org_grp_id"])
        data = [{
            "id": org.id,
            "name": org.school_name,
        } for org in EN_Organization.objects.filter(organization_group=orgGrp)]
        return HttpResponse(json.dumps(data))
    else:
        messages.warning(request,"Direct Access Denied")
        return HttpResponseRedirect("../Home")
