from django.http import HttpResponse
from django.template import loader
from apps.utilities.helper.ui_data_helper import UIDataHelper

'''
    Function  : Index
    Method    : Get
'''
def index(request):
    data = UIDataHelper(request).getData(page="is_notifications")
    template = loader.get_template("notify_homepage.html")
    return HttpResponse(template.render(data, request))
