from django.contrib import messages
from django.http import HttpResponseRedirect

from utils.app_util import AppUtil
from utils.logger import Logger
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties

'''
    Authentication Middleware
'''
class MW_Authentication():

    excluded_apps = [
        "SignUp",
        "Login",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        appName = AppUtil.getAppName(request)
        if appName not in self.excluded_apps:
            user_id = request.session[SessionProperties.USER_ID_KEY] if SessionProperties.USER_ID_KEY in request.session else None
            if user_id == None:
                Logger.error("Middleware Authentication Denied User ID {} To Access App {} ".format(user_id,appName))
                messages.warning(request,DisplayKey.get("error_session_time_out"))
                return HttpResponseRedirect('../Login')
            response = self.get_response(request)
            return response
        else:
            return self.get_response(request)

