from apps.roles.models import EN_UserRoles, TL_Roles
from apps.users.models import EN_Users
from properties.app_roles import Roles

class RolesViewHelper:

    def __init__(self, user):
        self.user = EN_Users.objects.get(id=user) if type(user) == int else user

    ''''
    # Returns the list of all roles [approved and pending] to display on UI
    '''
    def getRolesToDisplayOnRolesScreen(self):
        roles = []
        for role in EN_UserRoles.objects.filter(user_id=self.user.id):
            roleDict = {}
            roleDict.__setitem__("name", role.role.name)
            roleDict.__setitem__("code", role.role.code)
            roleDict.__setitem__("role_requested_by",
                                 role.request_raised_by.name + " - [" + role.request_raised_by.product_id + "]")
            roleDict.__setitem__("role_requested_on", role.request_raised_on)
            try:
                roleDict.__setitem__("role_approved_by",
                                     role.request_approved_by.name + " - [" + role.request_approved_by.product_id + "]")
                roleDict.__setitem__("role_approved_on", role.request_approved_on)
            except:
                roleDict.__setitem__("role_approved_by", None)
                roleDict.__setitem__("role_approved_on", None)
            roleDict.__setitem__("role_approved_on", role.request_approved_on)
            roleDict.__setitem__("approval_status", role.approved)

            if role.role_id == 1 and role.related_organization == None and role.related_organization_group == None and role.related_user == None:
                image = "myshishya.png"
                role_on = "Wokidz"
                product_id = ""
                id = self.user.id
            elif role.related_user != None:
                image = role.related_user.display_picture
                role_on = role.related_user.name
                product_id = role.related_user.product_id
                id = role.related_user.id
            elif role.related_organization != None:
                image = role.related_organization.display_picture
                role_on = role.related_organization.school_name
                product_id = role.related_organization.product_id
                id = role.related_organization.id
            elif role.related_organization_group != None:
                image = role.related_organization_group.logo
                role_on = role.related_organization_group.group_name
                product_id = role.related_organization_group.product_id
                id = role.related_organization_group.id
            else:
                return None

            roleDict.__setitem__("image", image)
            roleDict.__setitem__("role_on", role_on)
            roleDict.__setitem__("product_id", product_id)
            roleDict.__setitem__("id", id)
            roles.append(roleDict)
        return roles


    '''
    #Returns the list of system roles available
    '''
    def getSystemRolesAsList(self):
        retList = []
        for role in TL_Roles.objects.all():
            if role.code != Roles.SITE_ADMIN:
                innerDict = {
                    "code": role.code,
                    "name":role.name
                }
                retList.append(innerDict)
        return retList
