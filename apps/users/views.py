from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.login.models import EN_LoginCredentials
from properties.session_properties import SessionProperties

def index(request):
    pass

@csrf_exempt
def changeOnlineStatus(request):
    lc = EN_LoginCredentials.objects.get(user_id=request.session[SessionProperties.USER_ID_KEY])
    lc.is_online = not (lc.is_online)
    lc.save()
    request.session[SessionProperties.USER_ONLINE_KEY] = lc.is_online
    if request.is_ajax():
        return HttpResponse(lc.is_online)
    else:
        messages.info(request,"You are now {}".format("offline" if lc.is_online else "online"))
        return HttpResponseRedirect("../Home")