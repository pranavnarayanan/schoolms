from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.login.forms import FORM_ResetPassword, FORM_LoginDetails
from apps.login.helper import LoginHelper
from apps.roles.helper.user_roles_helper import UserRolesHelper
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties

''''
    Function  : Loads the Login Page
    Method    : GET / POST
'''

def index(request):
    template = loader.get_template("login_loginpage.html")
    data = {
        "form": FORM_LoginDetails(request.POST) if request.method == "POST" else FORM_LoginDetails()
    }
    return HttpResponse(template.render(data, request))


''''
    Function  : Validates the login Page
    Method    : POST
'''
def validateLogin(request):
    if request.method == 'POST':
        form_data = FORM_LoginDetails(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data.get("username")
            password = form_data.cleaned_data.get("password")
            lh = LoginHelper(request)
            userId = lh.getUserIdAfterAuthentication(username, password)
            if(userId == None):
                messages.error(request,DisplayKey.get("invalid_credentials"))
                return index(request)
            else:
                request.session[SessionProperties.USER_ID_KEY] = userId
                lh.updateOnlineStatusAndLoggedInTime()
                lh.setStaticUIData()
                lh.setActiveRole()
                UserRolesHelper(request).updateRolesOnSession()
                return HttpResponseRedirect("../../Home")
        else:
            return index(request)
    else:
        messages.error(request,DisplayKey.get("direct_access_denied"))
        return HttpResponseRedirect("Login")


''''
    Function  : Validates the reset password page
    Method    : POST
'''
def resetPasswordValidate(request):
    if request.method == 'POST':
        form_data = FORM_ResetPassword(request.POST)
        if(form_data.is_valid()) :
            return HttpResponse("<b>Call the action to send reset link to the user to reset password</b>")
        else:
            return resetPassword(request)
    else:
        return HttpResponseRedirect("Login?message=direct_access_denied")


''''
    Function  : Loads reset password page
    Method    : GET / POST 
'''
def resetPassword(request):
    template = loader.get_template("login_password_reset.html")
    data = {
        "form": FORM_ResetPassword() if request.method == "GET" else FORM_ResetPassword(request.POST)
    }
    return HttpResponse(template.render(data, request))
