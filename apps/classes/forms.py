import re
from django import forms
from apps.classes.helper.forms_helper import FormsHelper
from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from displaykey.display_key import DisplayKey
from apps.organization.helper.choice_helper import Choice
from properties.app_roles import Roles
from properties.session_properties import SessionProperties

class FORM_ClassNames(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_ClassNames, self).__init__(*args, **kwargs)
        fh = FormsHelper(self.request)
        self.fields['class_names'].choices = fh.getClasses()

    class_names = forms.ChoiceField(choices=[], required=False, initial=None)


class FORM_ClassDetails(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_ClassDetails, self).__init__(*args, **kwargs)
        fh = FormsHelper(self.request)
        self.fields['class_teacher'].choices = fh.getTeachers()
        self.fields['class_time_pattern'].choices = fh.getPatterns()


    class_name = forms.CharField (
        max_length=30,
        min_length=1,
        required=True
    )

    does_have_division = forms.BooleanField(required=False)

    class_division = forms.CharField(
        max_length=15,
        min_length=1,
        required=False
    )

    class_nickname = forms.CharField(
        max_length=30,
        required=False
    )

    class_start_date = forms.DateField(
        widget=forms.widgets.DateInput(
            format="%Y-%m-%d",
            attrs = { 'type': 'date' }
        ),
        required=True
    )

    class_end_date = forms.DateField(
        widget=forms.widgets.DateInput(
            format="%Y-%m-%d",
            attrs = { 'type' : 'date'}
        ),
        required=True
    )

    institution_levels = forms.ChoiceField(
        choices=Choice.InstitutionLevelAsChoice(),
        required=True
    )

    class_time_pattern = forms.ChoiceField(choices=[],required=True,initial=None)
    class_teacher = forms.ChoiceField(choices=[],required=False,initial=None)



    def clean(self):
        data = self.cleaned_data
        classStart = data["class_start_date"]
        classEnd = data["class_end_date"]
        if(classStart > classEnd):
            self.add_error("class_end_date", DisplayKey.get("class_end_date_prior_to_start_date_error"))
        if(data["class_division"] != None):
            division = data["class_division"]
            if re.match("^[a-z,A-Z]*$", division) is not None:
                divArray = division.split(",")
                divList = [d.upper() for d in divArray]
                for div in division.split(","):
                    if not(div.strip() == "" or div.strip() == None):
                        div = div.upper()
                        if len(div) > 1:
                            self.add_error("class_division", "Division '{}' should be single characters".format(div))
                        elif divList.count(div) > 1:
                            divList.remove(div)
                            self.add_error("class_division", "Division '{}' occurs multiple times".format(div))
                        elif EN_Classes.objects.filter(class_division=div, class_name=data["class_name"]):
                            user_id = self.request.session[SessionProperties.USER_ID_KEY]
                            try:
                                role = EN_UserRoles.objects.get(approved=True,is_selected_role=True, user_id=user_id, role__code=Roles.SCHOOL_ADMIN)
                                existing_divs = [clas.class_division for clas in
                                                 EN_Classes.objects.filter(class_name=data["class_name"], organization=role.related_organization)]
                                if div in existing_divs:
                                    self.add_error("class_division", "Division '{}' already exists for class {} ".format(div, data["class_name"]))
                            except Exception as e:
                                self.add_error("class_division", "No permmission for current role")
            else:
                self.add_error("class_division", "Invalid chars found. Single alphabets seperated by comma are only allowed")
        return data