from django.http import HttpResponse
from django.template import loader
from apps.notifications.models import EN_Notifications
from apps.utilities.helper.ui_data_helper import UIDataHelper
from properties.session_properties import SessionProperties

'''
    Function : Index
    Method   : Get
'''
def index(request):
    data = UIDataHelper(request).getData(page="is_notifications")
    template = loader.get_template("notify_homepage.html")
    return HttpResponse(template.render(data, request))


def getLiveNotifications(request):
    user_id = request.session[SessionProperties.USER_ID_KEY]
    EN_Notifications.objects.filter(created_to__id=user_id)

    retData = {
        "name":"aravind"
    }
    return HttpResponse(retData)