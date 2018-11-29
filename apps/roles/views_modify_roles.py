from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.roles.forms import FORM_ModifyUserRole
from apps.utilities.helper.ui_data_helper import UIDataHelper
from properties.app_roles import Roles
from properties.session_properties import SessionProperties

def modifyUserRoles(request):
    current_role = request.session[SessionProperties.USER_ACTIVE_ROLE_KEY]
    if not (current_role in [Roles.SITE_ADMIN, Roles.INSTITUTION_SUPER_USER, Roles.SCHOOL_ADMIN]):
       messages.warning(request,"Current role does not have privilege to perform this action")
       return HttpResponseRedirect("../Home")
    else:
       data = UIDataHelper(request).getData(page="is_modify_user_roles")
       data.__setitem__("form",FORM_ModifyUserRole(request.POST,request=request) if request.method == "POST" else FORM_ModifyUserRole(request=request))
       template = loader.get_template("roles_modify_user_roles.html")
       return HttpResponse(template.render(data, request))


def filterUser(request):
    form_data = FORM_ModifyUserRole(request.POST, request=request)
    if form_data.is_valid():

        form_data.cleaned_data.get("product_id")
        form_data.cleaned_data.get("name")
        form_data.cleaned_data.get("role")

        data = UIDataHelper(request).getData(page="is_modify_user_roles")
        data.__setitem__("form",form_data)
        template = loader.get_template("roles_modify_user_roles.html")
        return HttpResponse(template.render(data, request))
    else:
        return modifyUserRoles(request)