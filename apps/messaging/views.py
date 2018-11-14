from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from apps.messaging.helper import MessagesHelper
from apps.messaging.models import EN_Message
from apps.users.models import EN_Users
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from django.db.models import Q
import json

from properties.session_properties import SessionProperties

'''
    Function  : Index
    Method    : Get
'''
def index(request):
    data = UIDataHelper(request).getData(page="is_messaging")
    data.__setitem__("is_messages","active")
    template = loader.get_template("msg_homepage.html")
    return HttpResponse(template.render(data, request))

@csrf_exempt
def sendMessage(request) :
    if request.is_ajax():
        user_id = request.session[SessionProperties.USER_ID_KEY]
        retDict = {
            "status":False,
            "message":None
        }
        messageObj = EN_Message()
        #Saving the message
        try :
            messageData = request.POST["message"].strip()
            if(messageData != None and messageData != ""):
                messageObj.message = messageData
            else:
                retDict["message"] = DisplayKey.get("no_message_body")
        except :
            retDict["message"] = DisplayKey.get("no_message_body")

        #Getting the user to whom the message is sent
        try:
            if request.POST["send_to"].strip() != None:
                try:
                    assigned_to = int(request.POST["send_to"])
                    assigned_to = None if assigned_to == user_id else assigned_to
                    messageObj.send_to = EN_Users.objects.get(id=assigned_to)
                    messageObj.send_by = EN_Users.objects.get(id=user_id)
                except:
                    retDict["message"] = DisplayKey.get("invalid_user_id")
            else:
                retDict["message"] = DisplayKey.get("select_valid_user")
        except:
            retDict["message"] = DisplayKey.get("select_valid_user")

        if retDict["message"] == None:
            try:
                messageObj.save()
                retDict["status"] = True
            except:
                retDict["message"] = DisplayKey.get("no_message_body")
        return HttpResponse(json.dumps(retDict))
    else:
        return HttpResponseRedirect("../Page404/")


@csrf_exempt
def getContactList(request):
    if(request.is_ajax()):
        user_id = request.session[SessionProperties.USER_ID_KEY]
        type = request.POST["type"]
        mh = MessagesHelper()
        returnList = []
        if type == "search":
            keyword = request.POST["keyword"]
            returnList = mh.getContactsMatchingToSearchKeyword(keyword, user_id)
        elif type == "recent":
            returnList = mh.getRecentChatList(user_id)
        else:
            returnList = mh.getUnreadChatList(user_id)
        return HttpResponse(json.dumps(returnList))
    else :
        return HttpResponseRedirect("../Page404/")


@csrf_exempt
def getLiveChatUpdate(request):
    if request.is_ajax():
        try:
            other_user_id   = int(request.POST["other_user_id"])
            last_message_id = int(request.POST["last_message_id"])
            user_id = request.session[SessionProperties.USER_ID_KEY]

            messageResult = EN_Message.objects.filter(send_to_id=user_id, send_by_id=other_user_id, id__gt=last_message_id)

            mainReturnList = {
                "last_message_id": last_message_id,
                "messages": []
            }

            returnList = []
            for message in messageResult:
                message.read_status = True
                message.save()
                created_date = message.send_datetime
                date = "{} {} at {}:{} {}".format(created_date.strftime('%B')[:3], created_date.day, created_date.hour,
                                                  created_date.minute,created_date.strftime('%p'))
                rowDict = {
                    "message": message.message,
                    "time": date,
                    "read_status": message.read_status,
                    "sender": message.send_by.id
                }
                returnList.append(rowDict)
                mainReturnList.__setitem__('last_message_id', message.id)
            mainReturnList.__setitem__('messages', returnList)
            jsonResponse = json.dumps(mainReturnList)
            return HttpResponse(jsonResponse)
        except:
            return HttpResponse(0)
    else:
        return HttpResponseRedirect("../Page404/")


@csrf_exempt
def loadUserChat(request):
    if request.is_ajax():
        currentUser = EN_Users.objects.get(id=request.session[SessionProperties.USER_ID_KEY])
        sendToUser = EN_Users.objects.get(id=request.POST["chatting_with_user_id"])
        messageResult = EN_Message.objects.filter((Q(send_by=currentUser) & Q(send_to=sendToUser))
                                                  | (Q(send_by=sendToUser) & Q(send_to=currentUser))).order_by('send_datetime')[:200]
        mainReturnList = {
            "last_message_id":0,
            "other_user_name":sendToUser.name,
            "other_user_dp":sendToUser.display_picture,
            "other_user_id":sendToUser.id,
            "messages":[]
        }
        returnList = []
        for message in messageResult :
            message.read_status = True
            message.save()
            created_date = message.send_datetime
            date = "{} {} at {}:{} {}".format(created_date.strftime('%B')[:3], created_date.day, created_date.hour, created_date.minute,
                                              created_date.strftime('%p'))
            rowDict = {
                "message":message.message,
                "time":date,
                "read_status":message.read_status,
                "sender":message.send_by.id
            }
            returnList.append(rowDict)
            mainReturnList.__setitem__('last_message_id', message.id)
        mainReturnList.__setitem__('messages',returnList)
        jsonResponse = json.dumps(mainReturnList)
        return HttpResponse(jsonResponse)
    else:
        return HttpResponseRedirect("../Page404/")


@csrf_exempt
def getUnreadMsgsCount(request):
    user_id = request.session[SessionProperties.USER_ID_KEY]
    count = EN_Message.objects.filter(send_to_id=user_id, read_status=False).count()
    return HttpResponse(count)