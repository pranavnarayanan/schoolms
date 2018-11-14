from django.urls import path
from apps.messaging import views

urlpatterns = [
    path(r'',views.index, name="Renders Messaging Page"),
    path(r'SendMessage',views.sendMessage, name="Sends the Message"),
    path(r'GetContactList',views.getContactList, name="Retrieves The Chat List"),
    path(r'LoadUserChat',views.loadUserChat, name="Loads User Chat"),
    path(r'GetLiveChatUpdate',views.getLiveChatUpdate, name="Get Live Chat Update"),
    path(r'GetUnreadMsgsCount',views.getUnreadMsgsCount, name="Get Unread Msgs Count"),
]