from datetime import date
from apps.activity.models import EN_ActivityPattern, EN_Activity
from apps.roles.models import EN_UserRoles
from apps.users.models import EN_Users
from displaykey.display_key import DisplayKey

'''
    Activity Helper Class
'''
class ActivityHelper:

    def __init__(self,user_id = None):
        self.CreatedBy = user_id

    # Desc :
    # Creates an activity based on pattern
    #
    def createActivity(self, pattern, created_to, table, can_change_status_directly = True):
        act_pattern = EN_ActivityPattern.objects.filter(pattern_name=pattern)
        if not act_pattern.exists():
            raise Exception(DisplayKey.get("invalid_activity_pattern"))

        act = EN_Activity()
        act.created_on = date.today()
        act.created_to = created_to
        act.pattern = act_pattern.first()
        act.can_change_read_status_direclty = can_change_status_directly
        act.created_by = EN_Users.objects.get(id=self.CreatedBy)

        table_type = type(table).__name__
        if table_type == EN_UserRoles.__name__:
            act.en_user_role = table
        else:
            raise Exception(DisplayKey.get("invalid_table_for_activity_creation"))

        act.table_name = table_type

        act.save()
        return act