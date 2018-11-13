from apps.roles.models import EN_UserRoles
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
                "current_role" : self.__getActiveRoleData()
            },
            page : "active"
        }

    '''
    # Returns the list of active role of user
    '''
    def __rolesOnName(self):
        retList = []
        user_id = self.request.session[SessionProperties.USER_ID_KEY]
        user_roles = EN_UserRoles.objects.filter(approved=True,user_id=user_id)

        for role in user_roles:
            type = "organization_group" if role.related_organization_group != None else "parent" if role.related_user != None else "organization"

            if type == "organization":
                organization_details = role.related_organization.school_name
                place = "[ "+role.related_organization.street+" ]"
                product_id = role.related_organization.product_id
            elif type == "organization_group":
                organization_details = role.related_organization_group.group_name
                place = "[ Group ]"
                product_id = role.related_organization_group.product_id
            else:
                organization_details = " "
                place = " "
                product_id = role.related_user.product_id
            retDict = {
                "role_id": role.id,
                "name"        : role.role.name,
                "code"        : role.role.code,
                "type"        : type,
                "description" : organization_details,
                "product_id"  : product_id,
                "image"       : role.related_user.display_picture if type=="parent" else "#",
                "place"       : place
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


    '''
    # Returns active role of user
    '''
    def __getActiveRoleData(self):
        user_id = self.request.session[SessionProperties.USER_ID_KEY]
        active_roles = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True)
        active_role = None
        if active_roles.exists():
            if active_roles.__len__() > 1:
                for role in EN_UserRoles.objects.filter(user_id=user_id):
                    role.approved = False
                    role.save()
            else:
                active_role = active_roles.first()

        type = "Home" if active_role == None else "organization_group" if active_role.related_organization_group != None else "parent" if active_role.related_user != None else "organization"
        if type == "organization":
            organization_details = active_role.related_organization.school_name
            place = active_role.related_organization.street
            product_id = active_role.related_organization.product_id
        elif type == "organization_group":
            organization_details = active_role.related_organization_group.group_name
            place = " "
            product_id = active_role.related_organization_group.product_id
        elif type == "parent":
            organization_details = " "
            place = " "
            product_id = active_role.related_user.product_id
        else:
            organization_details = " "
            place = " "
            product_id = " "

        return {
            "role": active_role.role.name if active_role != None else "Home",
            "address": (organization_details+", "+place) if type == "organization" else organization_details,
            "image": None,
            "name": active_role.role.name if active_role != None else "Home",
            "product_id": product_id,
            "type": type
        }