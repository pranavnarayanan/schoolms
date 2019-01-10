from django.http import HttpResponse
from django.template import loader
from apps.utilities.helper.ui_data_helper import UIDataHelper

def index(request):
    template = loader.get_template("announcements_home.html")
    data = UIDataHelper(request).getData(page="is_announcements_home")
    return HttpResponse(template.render(data, request))

def create(request):
    template = loader.get_template("announcements_create.html")
    data = UIDataHelper(request).getData(page="is_create_announcement")
    return HttpResponse(template.render(data, request))