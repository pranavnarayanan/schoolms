import re
from django import forms

from apps.announcements.helper.forms_helper import FormsHelper
from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties

class FORM_Announcements(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_Announcements, self).__init__(*args, **kwargs)
        fh = FormsHelper(self.request)
        self.fields['org_group'].choices = fh.getOrganizationGroup()
        self.fields['roles_list'].choices = fh.getRolesList()

    org_group = forms.ChoiceField(choices=[], required=False, initial=None)

    roles_list = forms.MultipleChoiceField(
        choices = [],
        widget  = forms.CheckboxSelectMultiple,
    )

    announcement_content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Input your announcement here'}))

    sms_content = forms.CharField(widget=forms.TextInput)