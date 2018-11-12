from apps.users.models import EN_Users
from properties.session_properties import SessionProperties

class UIDataHelper:

    def __init__(self, request):
        self.request = request

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
                "user_roles" : self.__rolesOnName(),
                "current_role" : {
                    "role"       : "school_admin",
                    "address"    : "Some Address",
                    "image"      : None,
                    "name"       : "Gafoor KA",
                    "product_id" : "MY1202344",
                    "type"       : "user"
                },
                page : "active"
            }
        }

    '''
    # Returns the list of active role of user
    '''
    def __rolesOnName(self):
        retList = []
        retDict = {
            "role_id": 1,
            "name"        : "School Admin",
            "code"        : "school_admin",
            "type"        : "organization",
            "description" : "School Admin",
            "product_id"  : "MY123443",
            "image"       : None,
            "place"       : None
        }
        retList.append(retDict)
        return retList


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

















