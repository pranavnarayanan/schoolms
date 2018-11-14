from apps.users.models import EN_Users
from apps.roles.helper.user_roles_helper import UserRolesHelper
from properties.session_properties import SessionProperties

'''
Class Fetch All User Related UI Static Data From Session
'''
class UIDataHelper:

    def __init__(self, request):
        self.request = request
        self.userRoleHelper = UserRolesHelper(self.request)

    '''
    # Function returns the dict of user data which needs to be displayed on the UI
    '''
    def getData(self, page="home"):

        return {
            "ui_data" : {
                "header": {
                    "name"       : self.__getDataFromSession(SessionProperties.USER_NAME_KEY),
                    "gender"     : self.__getDataFromSession(SessionProperties.USER_GENDER_KEY),
                    "image"      : self.__getDataFromSession(SessionProperties.USER_DP_KEY),
                    "product_id" : self.__getDataFromSession(SessionProperties.USER_PRODUCT_ID_KEY)
                },
                "sidebar": {
                    "role" : self.__getDataFromSession(SessionProperties.USER_ACTIVE_ROLE_KEY)
                },
                "is_online"  : self.__getDataFromSession(SessionProperties.USER_ONLINE_KEY),
                "user_roles": self.userRoleHelper.getAllApprovedRolesOfUserFromSession(),
                "current_role": self.userRoleHelper.getSelectedRolesOfUserFromSession()
            },
            page : "active"
        }

    '''
    # Retrieving the user session data saved while logged in
    '''
    def __getDataFromSession(self, session_key):
        if SessionProperties.USER_ID_KEY not in self.request.session:
            raise Exception("User Auth Session Expired")

        if not session_key in self.request.session:
            user = EN_Users.objects.get(id=self.request.session[SessionProperties.USER_ID_KEY])
            if session_key == SessionProperties.USER_NAME_KEY:
                self.request.session[SessionProperties.USER_NAME_KEY] = user.name
            elif session_key == SessionProperties.USER_GENDER_KEY:
                self.request.session[SessionProperties.USER_GENDER_KEY] = user.gender.code
            elif session_key == SessionProperties.USER_DP_KEY:
                self.request.session[SessionProperties.USER_DP_KEY] = user.display_picture
            elif session_key == SessionProperties.USER_PRODUCT_ID_KEY:
                self.request.session[SessionProperties.USER_PRODUCT_ID_KEY] = user.product_id
            elif session_key == SessionProperties.USER_ONLINE_KEY:
                self.request.session[SessionProperties.USER_ONLINE_KEY] = user.en_logincredentials.is_online
            elif session_key == SessionProperties.USER_ACTIVE_ROLE_KEY:
                self.request.session[SessionProperties.USER_ACTIVE_ROLE_KEY] = None
            else:
                raise Exception("Invalid Session Key Passed | Class: UIDataHelper, Function: getDataFromSession")

        return self.request.session[session_key]
