import datetime
import json
from apps.notifications.models import EN_Notifications
from properties.notification_properties import NotificationTypes
from properties.session_properties import SessionProperties

class NotificationHelper:

    def __init__(self,request):
        self.request = request
        self.user_id = self.request.session[SessionProperties.USER_ID_KEY]

    def notify(self,recipient_id, type, requester_id=1, change_read_status_direclty=True):
        notifs = EN_Notifications()
        notifs.created_on = datetime.datetime.now()
        notifs.created_by_id = requester_id
        notifs.created_to_id = recipient_id
        notifs.notification_type = type
        notifs.read_status = False
        notifs.can_change_read_status_direclty = change_read_status_direclty
        notifs.save()

    def getUnSeenNotificationCount(self):
        unread_notifs = EN_Notifications.objects.filter(created_to_id = self.user_id, read=False)
        unseen_notifs = unread_notifs.filter(seen=False)
        return (unread_notifs.count() - unseen_notifs.count())

    def getUnreadNotificationsAsJSON(self):
        return json.dumps([{
            "id" : notif.id,
            "created_on" : notif.created_on,
            "created_by" : notif.created_by.name,
            "notification_type" : notif.notification_type,
            "content":NotificationTypes.Message.get(notif.notification_type),
            "seen" : notif.seen,
            "read" : notif.read,
            "can_change_read_status_direclty" : notif.can_change_read_status_direclty,
        }for notif in EN_Notifications.objects.filter(created_to_id=self.user_id, read=False).order_by('-id')])