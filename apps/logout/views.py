from django.contrib import messages
from django.http import HttpResponseRedirect
from properties.session_properties import SessionProperties

def index(request):
    if SessionProperties.USER_ID_KEY in request.session:
        del(request.session[SessionProperties.USER_ID_KEY])
    if SessionProperties.USER_NAME_KEY in request.session:
        del(request.session[SessionProperties.USER_NAME_KEY])
    if SessionProperties.USER_GENDER_KEY in request.session:
        del(request.session[SessionProperties.USER_GENDER_KEY])
    if SessionProperties.USER_DP_KEY in request.session:
        del(request.session[SessionProperties.USER_DP_KEY])
    if SessionProperties.USER_PRODUCT_ID_KEY in request.session:
        del(request.session[SessionProperties.USER_PRODUCT_ID_KEY])
    if SessionProperties.USER_ONLINE_KEY in request.session:
        del(request.session[SessionProperties.USER_ONLINE_KEY])
    messages.success(request,"Successfully Signed Out")
    return HttpResponseRedirect("../Login")