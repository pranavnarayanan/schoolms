import json
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from math import ceil
from apps.activity.models import EN_Activity
from apps.utilities.helper.ui_data_helper import UIDataHelper
from properties.session_properties import SessionProperties

'''
    Function  : Index
    Method    : Get
'''
def index(request):
    data = UIDataHelper(request).getData(page="is_notifications")
    template = loader.get_template("notify_homepage.html")
    return HttpResponse(template.render(data, request))


'''
    Function  : Get Notifications
    Method    : AJAX  | POST 
'''
@csrf_exempt
def liveNotificationUpdate(request):
    if request.is_ajax():
        retDict = {
            "have_change":0,
            "notifications":[],
            "notification_count_from_db" : 0,
            "last_notification_id_from_db" : 0
        }
        try:
            notification_count_from_ui   = int(request.POST["notification_count_from_ui"])
            last_notification_id_from_ui = int(request.POST["last_notification_id_from_ui"])
            user_id = request.session[SessionProperties.USER_ID_KEY]
            notifs = EN_Activity.objects.filter(read_status=False, created_to_id=user_id)
            if notifs.exists():
                notification_count_from_db = notifs.count()
                last_notification_id_from_db = notifs.last().id
                if notification_count_from_db != notification_count_from_db or last_notification_id_from_ui != last_notification_id_from_db:
                    retDict["have_change"] = 1
                    retDict["notification_count_from_db"] = notification_count_from_db
                    retDict["last_notification_id_from_db"] = last_notification_id_from_db
                    notifications = []
                    for notify in notifs:
                        notificationsDict = {}
                        notificationsDict.__setitem__("activity_id", notify.id)
                        notificationsDict.__setitem__("pattern", notify.pattern.pattern_name)
                        notificationsDict.__setitem__("subject", notify.pattern.subject)
                        notificationsDict.__setitem__("priority", notify.pattern.priority)
                        notificationsDict.__setitem__("is_escalated", (notify.escalated_from != None))
                        notificationsDict.__setitem__("can_change_status_directly",
                                                      notify.can_change_read_status_direclty)
                        on = notify.created_on
                        date = "{} {} at {}:{} {}".format(on.strftime('%B')[:3], on.day, on.hour, on.minute,
                                                          on.strftime('%p'))
                        notificationsDict.__setitem__("created_on", date)
                        if notify.created_by != None:
                            notificationsDict.__setitem__("created_by_name", notify.created_by.name)
                            notificationsDict.__setitem__("product_id", notify.created_by.product_id)
                            notificationsDict.__setitem__("created_by_image", notify.created_by.display_picture)
                        else:
                            notificationsDict.__setitem__("created_by_image", None)
                        notifications.append(notificationsDict)
                    retDict.__setitem__("notifications", notifications)
                else:
                    retDict["notification_count_from_db"] = notification_count_from_ui
                    retDict["last_notification_id_from_db"] = last_notification_id_from_ui
            elif notification_count_from_ui != 0 or last_notification_id_from_ui != 0:
                retDict["have_change"] = 1
            else:
                pass
        except:
            pass #Swallow errors - Errors occur due to quite frequent calling of same function
        return HttpResponse(json.dumps(retDict))
    else:
        return HttpResponseRedirect("../Page404")


'''
    Function  : Get Notifications For Table
    Method    : AJAX  | POST 
'''
@csrf_exempt
def getMyNotifications(request):
    if request.is_ajax():
        page = int(request.POST.get('page'))
        page = 1 if page < 1 else page
        pageRowCount = int(request.POST.get('page_row_count'))
        search_keyword = request.POST.get('search_keyword').strip()
        search_keyword = None if search_keyword == "" else search_keyword
        startingIndex = (page - 1) * pageRowCount
        endingIndex = page * pageRowCount
        user_id = request.session[SessionProperties.USER_ID_KEY]
        records = EN_Activity.objects.filter(created_to=user_id).order_by('-id')
        if search_keyword != None:
            records = records.filter(Q(role__code__contains=search_keyword))
        total_records_count = records.all().count()
        records = records.all()[startingIndex:endingIndex]
        retList = []
        for record in records:
            returnDict = {
                "activity_id": record.id,
                "act_creator_name": record.created_by.name,
                "act_creator_prd_id": record.created_by.product_id,
                "act_created_on": record.created_on.__str__(),
                "read_status": record.read_status,
                "pattern" : record.pattern.pattern_name,
                "subject" : record.pattern.subject,
                "description" : record.pattern.description,
            }
            retList.append(returnDict)
        ret = {
            "total_pages": ceil(total_records_count / pageRowCount),
            "total_records": total_records_count,
            "data": retList
        }

        jsonResponse = json.dumps(ret)
        return HttpResponse(jsonResponse)
    else:
        return HttpResponseRedirect("../Redirects/ErrorPage?page=403")

