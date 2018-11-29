from django.contrib import messages
from django.http import HttpResponseRedirect
from displaykey.display_key import DisplayKey
from properties.app_accessibility_dictionary import AppAccessibilityDictionary
from properties.session_properties import SessionProperties
from utils.logger import Logger

'''
    User Role Authentication Middleware
'''
class MW_RoleAccessiblityOnAppAuthentication():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            fullPath = request.get_full_path()
            if list(fullPath).__contains__("?"):
                fullPathList = list((fullPath.split("?")[0]).split("/"))
            else:
                fullPathList = list(fullPath.split("/"))

            for uri in fullPathList:
                if uri.strip() == "":
                    fullPathList.remove(uri)

            app = fullPathList[0]
            method = "Index" if fullPathList.__len__() == 1 else fullPathList[1]

            allow = False
            isURLInvalid = False

            if not AppAccessibilityDictionary.APPS_WITH_FULL_ACCESS_TO_ALL_USERS.__contains__(app):
                if AppAccessibilityDictionary.APPS_WITH_LIMITED_ACCESS_TO_USERS.keys().__contains__(app):
                    limitedAccessApp = AppAccessibilityDictionary.APPS_WITH_LIMITED_ACCESS_TO_USERS.get(app)
                    if limitedAccessApp.keys().__contains__(method):
                        currentRole = request.session[SessionProperties.USER_ACTIVE_ROLE_KEY]
                        allow = True if (limitedAccessApp.get(method).__contains__(currentRole) or limitedAccessApp.get(method).__contains__("all")) else False
                    else:
                        isURLInvalid = True
                else:
                    isURLInvalid = True
            else:
                allow = True

            if allow:
                return self.get_response(request)
            elif isURLInvalid:
                messages.error(request, DisplayKey.get("unregistered_url"))
                return HttpResponseRedirect('../Home')
            else:
                messages.error(request, DisplayKey.get("no_privelege_to_access_app"))
                return HttpResponseRedirect('../Home')
        except Exception as e:
            Logger.error("Error occured on middleware MW_RoleAccessiblityOnAppAuthentication \n : {}".format(e))
            messages.error(request, DisplayKey.get("unregistered_url"))
            return HttpResponseRedirect('../Home')
