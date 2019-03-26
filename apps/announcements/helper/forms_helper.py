import json

from apps.announcements.constants import AnnouncementConstants
from apps.announcements.helper.app_helper import AppHelper
from apps.organization.models import EN_OrganizationGroup
from apps.roles.models import EN_UserRoles, TL_Roles
from properties.session_properties import SessionProperties

class FormsHelper:

    def __init__(self,request):
        self.request = request
        self.user_id = request.session[SessionProperties.USER_ID_KEY]

    def getRolesList(self):
        user_role = AppHelper.getCurrentRole(user_id=self.user_id)
        roles = TL_Roles.objects.filter(code__in=AnnouncementConstants.PERMISSION_DICTIONARY.__getitem__(user_role.role.code))
        retArray = []
        for role in roles:
            array = []
            array.append(role.code)
            array.append(role.name)
            retArray.append(tuple(array))
        return tuple(retArray)

    def getOrganizationGroup(self):
        try:
            user_role = EN_UserRoles.objects.get(user_id=self.user_id, approved=True, is_selected_role=True)
            retArray = []
            orgGroup = EN_OrganizationGroup.objects.filter(id = user_role.related_organization.organization_group_id)
            for grp in orgGroup :
                array = []
                array.append(grp.id)
                array.append(grp.group_name)
                retArray.append(tuple(array))
            return tuple(set(retArray))
        except:
            return None, "No Permission"