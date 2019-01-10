import datetime
from apps.notifications.models import EN_Notifications

class NotificationHelper:

    @staticmethod
    def notify(recipient_id, type, requester_id=1, change_read_status_direclty=True):
        notifs = EN_Notifications()
        notifs.created_on = datetime.datetime.now()
        notifs.created_by_id = requester_id
        notifs.created_to_id = recipient_id
        notifs.notification_type = type
        notifs.read_status = False
        notifs.can_change_read_status_direclty = change_read_status_direclty
        notifs.save()