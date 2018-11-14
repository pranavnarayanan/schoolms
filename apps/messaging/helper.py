from django.db.models import Q
from apps.messaging.models import EN_Message
from apps.users.models import EN_Users


class MessagesHelper():

    def getRecentChatList(self, user_id):
        userObj = EN_Users.objects.get(id=user_id)
        send_message_list = EN_Message.objects.filter(send_by=userObj).values('send_to').distinct()[:100]
        recvd_message_list = EN_Message.objects.filter(send_to=userObj).values('send_by').distinct()[:100]
        sendList = []
        recdList = []
        returnList = []
        for row in send_message_list:
            sendList.append(row['send_to'])
        for row in recvd_message_list:
            recdList.append(row['send_by'])
        commonList = set(sendList).union(recdList)
        for row in commonList:
            user = EN_Users.objects.get(id=row)
            rowDict = {
                "id": user.id,
                "name": user.name,
                "disp_pic": user.display_picture,
                "unread_msg_count": 0
            }
            returnList.append(rowDict)

        return returnList


    def getUnreadChatList(self, user_id):
        recvd_message_query = EN_Message.objects.filter(send_to_id=user_id, read_status=False)
        #total_unread_messages = recvd_message_query.count()
        usersList = list(recvd_message_query.values('send_by').distinct()[:100])
        returnList = []
        for user in usersList:
            user = EN_Users.objects.get(id=user['send_by'])
            rowDict = {
                "id": user.id,
                "name": user.name,
                "disp_pic": user.display_picture,
                "unread_msg_count": EN_Message.objects.filter(send_to_id=user_id, read_status=False, send_by_id=user.id).count()
            }
            returnList.append(rowDict)
        return returnList

    def getContactsMatchingToSearchKeyword(self, keyword, user_id):
        usersList = EN_Users.objects.filter(((Q(name__contains=keyword) | Q(product_id__contains=keyword)) & (~Q(id= user_id))))[:100]
        returnList = []
        for user in usersList:
            rowDict = {
                "id": user.id,
                "name": user.name,
                "disp_pic": user.display_picture,
                "unread_msg_count": 0
            }
            returnList.append(rowDict)
        return returnList
