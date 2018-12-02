from datetime import date
from apps.activity.models import EN_ActivityPattern, EN_Activity
from apps.roles.models import EN_UserRoles
from apps.users.models import EN_Users
from displaykey.display_key import DisplayKey
from properties.session_properties import SessionProperties

'''
    Activity Helper Class
'''
class ActivityHelper:

    def __init__(self,request, user_id=None):
        if SessionProperties.USER_ID_KEY in request.session:
            self.CreatedBy = request.session[SessionProperties.USER_ID_KEY]
        elif user_id != None:
            if EN_Users.objects.filter(id=user_id).exists():
                self.CreatedBy = user_id
            raise Exception("Invalid User id provided for activity creation")
        else:
            raise Exception("User Id not available for activity creation")


    # Desc :
    # Creates an activity based on pattern
    #
    def createActivity(self, pattern, created_to=None, table=None, can_change_status_directly = True):
        act_pattern = EN_ActivityPattern.objects.filter(pattern_name=pattern)
        if not act_pattern.exists():
            raise Exception(DisplayKey.get("invalid_activity_pattern"))

        act = EN_Activity()
        act.created_on = date.today()
        act.created_to_id = self.CreatedBy if created_to == None else created_to
        act.pattern = act_pattern.first()
        act.can_change_read_status_direclty = can_change_status_directly
        act.created_by_id = self.CreatedBy

        if table != None:
            table_type = type(table).__name__
            if table_type == EN_UserRoles.__name__:
                act.en_user_role = table
            else:
                raise Exception(DisplayKey.get("invalid_table_for_activity_creation"))
        else:
            table_type = None
        act.table_name = table_type

        act.save()
        return act