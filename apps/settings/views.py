import json
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.login.models import EN_LoginCredentials
from apps.users.models import EN_Users
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties


def index(request):
    data = UIDataHelper(request).getData(page="is_settings")
    data.__setitem__("is_settings","active")
    template = loader.get_template("settings_home.html")
    return HttpResponse(template.render(data, request))

@csrf_exempt
def changeUsername(request):
    if request.is_ajax() :
        username = request.POST['username']
        user = EN_Users.objects.get(id=request.session[SessionProperties.USER_ID_KEY])
        if(user.en_logincredentials.username == username):
            retDict={
                "status":False,
                "message":DisplayKey.get("same_username")
            }
            return HttpResponse(json.dumps(retDict))
        else:
            usernameExists = EN_LoginCredentials.objects.exclude(user=user).filter(username=username)
            if(not usernameExists.exists()):
                loginData = EN_LoginCredentials.objects.get(user=user)
                loginData.username = username
                loginData.last_logged_in_time = datetime.datetime.now()
                loginData.save()
                retDict = {
                    "status": True,
                    "message": DisplayKey.get("successful_username_reset")
                }
                return HttpResponse(json.dumps(retDict))
            else:
                retDict = {
                    "status": True,
                    "message": DisplayKey.get("username_exists_otheruser")
                }
                return HttpResponse(json.dumps(retDict))
    else:
        return HttpResponseRedirect("../Page404/")


@csrf_exempt
def changePassword(request):
    if request.is_ajax() :
        password = request.POST['password']
        user = EN_Users.objects.get(id=request.session[SessionProperties.USER_ID_KEY])

        existingPass = user.en_logincredentials.password

        if(existingPass == password):
            retDict = {
                "status":False,
                "message":DisplayKey.get("same_password")
            }
            return HttpResponse(json.dumps(retDict))
        else:
            credentials = user.en_logincredentials
            if credentials.password_history is None or credentials.password_history != password:
                credentials.password_history = existingPass
                credentials.password = password
                credentials.last_logged_in_time = datetime.datetime.now()
                credentials.save()
                retDict = {
                    "status":True,
                    "message":DisplayKey.get("successful_pass_reset")
                }
                return HttpResponse(json.dumps(retDict))
            else:
                retDict = {
                    "status":False,
                    "message":DisplayKey.get("last_two_pass_error")
                }
                return HttpResponse(json.dumps(retDict))
    else:
        return HttpResponseRedirect("../Page404/")
