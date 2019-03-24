import json

from apps.organization.models import EN_OrganizationGroup
from apps.roles.models import EN_UserRoles, TL_Roles
from properties.session_properties import SessionProperties

class FormsHelper:

    def __init__(self,request):
        self.request = request
        self.user_id = request.session[SessionProperties.USER_ID_KEY]

    def getRolesList(self):
        try:
            roles = TL_Roles.objects.all()
            retArray = []
            for role in roles:
                array = []
                array.append(role.id)
                array.append(role.name)
                retArray.append(tuple(array))
            return tuple(retArray)
        except:
            return ((None,"No Permission"))

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