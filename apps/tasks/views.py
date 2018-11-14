import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from apps.tasks.models import EN_Tasks
from apps.users.models import EN_Users
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties


def index(request):
    data = UIDataHelper(request).getData(page="is_tasks")
    data.__setitem__("is_tasks", "active")
    template = loader.get_template("tasks_list_tasks.html")
    return HttpResponse(template.render(data, request))

@csrf_exempt
def SaveTask(request):
    if request.is_ajax():
        retDict = {
            "status":False,
            "message":None
        }
        taskData = EN_Tasks()

        # --- Priority --- #
        try:
            priority = int(request.POST["priority"])
            taskData.priority = 5 if priority > 5 else 1 if priority < 1 else priority
        except:
            taskData.priority = 3

        # --- Date --- #
        try:
            input_date = datetime.strptime(request.POST["date"], "%Y-%m-%d").date()
            if input_date < datetime.now().date():
                retDict["message"] = DisplayKey.get("task_previous_date_error")
            else:
                taskData.to_be_done_on = input_date
        except:
            retDict["message"] = DisplayKey.get("invalid_date_entry")

        # --- Time --- #
        try:
            taskData.to_be_done_at = datetime.strptime(request.POST["time"], "%H:%M").time()
        except:
            taskData.to_be_done_at = datetime.strptime("00:00", "%H:%M").time()

        # --- Task --- #
        try:
            taskData.task = request.POST["taskname"].strip()
            if taskData.task == None:
                retDict["message"] = DisplayKey.get("task_name_is_empty")
        except:
            retDict["message"] = DisplayKey.get("task_name_is_empty")

        # --- Assigned by --- #
        taskData.assigned_by_id = request.session[SessionProperties.USER_ID_KEY]

        # --- Assigned To --- #
        try:
            if request.POST["assigned_to"].strip() != None:
                try:
                    assigned_to = int(request.POST["assigned_to"])
                    taskData.assigned_to = EN_Users.objects.get(id=assigned_to)
                except:
                    retDict["message"] = DisplayKey.get("invalid_user_id")
            else:
                taskData.assigned_to_id = request.session[SessionProperties.USER_ID_KEY]
        except:
            taskData.assigned_to_id = request.session[SessionProperties.USER_ID_KEY]

        if retDict["message"] == None:
            try:
                taskData.save()
                retDict["status"] = True
            except:
                retDict["message"] = DisplayKey.get("task_with_same_constraints_already_exist")

        return HttpResponse(json.dumps(retDict))
    else:
        return HttpResponseRedirect("SaveTask?message=direct_access_denied")

