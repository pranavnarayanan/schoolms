from apps.roles.models import EN_UserRoles
from properties.session_properties import SessionProperties

class AppHelper:

    @staticmethod
    def getCurrentRole(request = None,user_id=None):
        if(request ==  None and user_id == None):
            raise Exception("Either request or user id should be provided")
        else:
            if request != None:
                user_id = request.session[SessionProperties.USER_ID_KEY]
            roles = EN_UserRoles.objects.filter(user_id=user_id, is_selected_role=True)
            if not roles.exists():
                raise Exception("No active role found")
            else:
                return roles.first()

