import json
from apps.roles.models import EN_UserRoles
from properties.app_roles import RoleType
from properties.image_properties import ImageType
from properties.session_properties import SessionProperties
from utils.image_helper import ImageHelper


class UserRolesHelper:

    def __init__(self, request):
        self.request = request

    def getApprovedUserRoles(self):
        if SessionProperties.USER_APPROVED_ROLES_KEY in self.request.session:
            rolesJSON = self.request.session[SessionProperties.USER_APPROVED_ROLES_KEY]
            data = json.loads(rolesJSON)
            print(data)
        else:
            roles = self.__setUserRolesToSession()
            rolesJSON = json.dumps(roles)
            self.request.session[SessionProperties.USER_APPROVED_ROLES_KEY] = rolesJSON
            
    def __setUserRolesToSession(self):
        retList = []
        user_id = self.request.session[SessionProperties.USER_ID_KEY]
        user_roles = EN_UserRoles.objects.filter(approved=True, user_id=user_id)

        for role in user_roles:
            if role.related_organization_group != None:
                type = RoleType.ORGANIZATION_GROUP
                organization_details = role.related_organization_group.group_name
                place = "[ Group ]"
                product_id = role.related_organization_group.product_id
                image = role.related_organization_group.logo
                img_type = ImageType.ORGANIZATION_GROUP
            elif role.related_user != None:
                type = RoleType.PARENT
                organization_details = " "
                place = " "
                product_id = role.related_user.product_id
                image = role.related_user.display_picture
                img_type = ImageType.ORGANIZATION
            else:
                type = RoleType.ORGANIZATION
                organization_details = role.related_organization.school_name
                place = "[ " + role.related_organization.street + " ]"
                product_id = role.related_organization.product_id
                image = role.related_organization.display_picture
                img_type = ImageType.USER
            retDict = {
                "role_id": role.id,
                "name": role.role.name,
                "code": role.role.code,
                "type": type,
                "description": organization_details,
                "product_id": product_id,
                "image": ImageHelper(img_type).getFullPath(image),
                "place": place
            }
            retList.append(retDict)
        return retList
