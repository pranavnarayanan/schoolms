import json
from apps.roles.models import EN_UserRoles
from properties.app_roles import RoleType
from properties.image_properties import ImageType
from properties.session_properties import SessionProperties
from utils.image_helper import ImageHelper

'''
This class is called to set the roles in Session
'''
class UserRolesHelper:

    def __init__(self, request):
        self.request = request
        self.user_id = request.session[SessionProperties.USER_ID_KEY]

    '''
    # Update Both Sessions of Roles 
    # This is used mainly in login app
    '''
    def updateRolesOnSession(self):
        self.request.session[SessionProperties.USER_APPROVED_ROLES_KEY] = json.dumps(self.__getAllApprovedRolesOfUser())
        self.request.session[SessionProperties.USER_SELECTED_ROLE_KEY] = json.dumps(self.__getSelectedRolesOfUser())

    '''
    # Returns the Approved Roles List From Session
    # If data not found in session, session update will be done 
    '''
    def getAllApprovedRolesOfUserFromSession(self):
        if not SessionProperties.USER_APPROVED_ROLES_KEY in self.request.session:
            self.updateRolesOnSession()
        rolesJSON = self.request.session[SessionProperties.USER_APPROVED_ROLES_KEY]
        return json.loads(rolesJSON)


    '''
    # Returns the Selected Role From Session
    # If data not found in session, session update will be done 
    '''
    def getSelectedRolesOfUserFromSession(self):
        if not SessionProperties.USER_SELECTED_ROLE_KEY in self.request.session:
            self.updateRolesOnSession()
        rolesJSON = self.request.session[SessionProperties.USER_SELECTED_ROLE_KEY]
        return json.loads(rolesJSON)



    '''
    # Returns the Approved Roles List From Database
    # For this class purpose only
    '''
    def __getAllApprovedRolesOfUser(self):
        retList = []
        user_roles = EN_UserRoles.objects.filter(approved=True, user_id=self.user_id)

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
            elif role.related_organization != None:
                type = RoleType.ORGANIZATION
                organization_details = role.related_organization.school_name
                place = "[ " + role.related_organization.street + " ]"
                product_id = role.related_organization.product_id
                image = role.related_organization.display_picture
                img_type = ImageType.USER
            else: # Myshisya User
                type = RoleType.MYSHISHYA_USER
                organization_details = "Site Admin"
                place = " "
                product_id = " "
                image = " "
                img_type = " "
            retDict = {
                "role_id": role.id,
                "name": role.role.name,
                "code": role.role.code,
                "type": type,
                "description": organization_details,
                "product_id": product_id,
                "image": ImageHelper(img_type).getFullPath(image),
                "place": place,
                "is_selected_role": role.is_selected_role
            }
            retList.append(retDict)
        return retList


    '''
    # Returns the Selected Role From Database
    # For this class purpose only
    '''
    def __getSelectedRolesOfUser(self):
        selected_role = EN_UserRoles.objects.filter(approved=True, user_id=self.user_id, is_selected_role=True)
        if selected_role.exists():
            role = selected_role.first()
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
        else:
            role = None
            type = RoleType.HOME
            organization_details = " "
            place = " "
            product_id = " "
            image = " "
            img_type = " "

        return {
            "role_id": role.id if role != None else " ",
            "role": role.role.name if role != None else "Home",
            "name": role.role.name if role != None else "Home",
            "code": role.role.code if role != None else "home",
            "type": type,
            "address": organization_details,
            "product_id": product_id,
            "image": ImageHelper(img_type).getFullPath(image) if role != None else " ",
            "place": place
        }