from django.http import HttpResponse
from django.template import loader
from apps.utilities.helper.ui_data_helper import UIDataHelper

def index(request):
    template = loader.get_template("home_homepage.html")
    data = UIDataHelper(request).getData(page="is_home")
    return HttpResponse(template.render(data, request))

