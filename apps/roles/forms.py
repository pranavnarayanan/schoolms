import re
from django import forms
from apps.roles.helper.role_approval_hierarchy import RoleApprovalHierarchy
from apps.roles.models import TL_Roles
from apps.users.models import EN_Users
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties

'''
    Form for assigning user roles
'''
class FORM_UserRoleAssignment(forms.Form):

    product_ids = forms.CharField(widget=forms.Textarea,required=True )

    def clean(self):
        data = self.cleaned_data
        prdIdListString = (data["product_ids"].replace(" ", "")).strip()
        if (re.match('^[MY0-9,]+$',prdIdListString) == None):
            self.add_error("product_ids", DisplayKey.get("invalid_characters_in_product_id_list"))
        return data



'''
    Form for filtering user -- To modify user roles
'''
class FORM_ModifyUserRole(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_ModifyUserRole, self).__init__(*args, **kwargs)
        self.fields['roles'].choices = self.getRoles()

    def getRoles(self):
        current_role = self.request.session[SessionProperties.USER_ACTIVE_ROLE_KEY]
        roles = []
        if current_role == Roles.SITE_ADMIN:
            roles = TL_Roles.objects.all()
        elif current_role == Roles.INSTITUTION_SUPER_USER:
            roles = TL_Roles.objects.filter(code__in=RoleApprovalHierarchy.INSTITUTION_SU_APPROVAL_LIST)
        elif current_role == Roles.SCHOOL_ADMIN:
            roles = TL_Roles.objects.filter(code__in=RoleApprovalHierarchy.SCHOOL_ADMIN_APPROVAL_LIST)

        retChoice = []
        retChoice.append(("0","Select Roles"))
        for role in roles:
            retChoice.append((role.code,role.name))
        return tuple(retChoice)

    product_id = forms.CharField(required=False, min_length=9, max_length=12)
    name = forms.CharField(min_length=2, required=False)
    roles = forms.ChoiceField(required=False, choices=[])

    def clean(self):
        data = self.cleaned_data
        prd_id = data["product_id"]
        if prd_id != None:
            if not EN_Users.objects.filter(product_id=prd_id).exists():
                self.add_error("product_id", "Invalid Product ID")
        return data