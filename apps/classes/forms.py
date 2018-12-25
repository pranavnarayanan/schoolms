import json

from django import forms

from apps.classes.forms_helper import ClassFormsHelper
from displaykey.display_key import DisplayKey
from apps.organization.helper.choice_helper import Choice
from properties.session_properties import SessionProperties


class FORM_ClassDetails(forms.Form) :
    TIMEPATTERN = [('lkg', 'SRS LKG Pattern'),
                   ('1to4', 'SRS 1 to 4 Pattern'),
                   ('5to7', 'SRS 5 to 7 Pattern'),
                   ('8to10', 'SRS 8 to 10 Pattern'),
                   ('11and12', 'SRS 11 and 12 Pattern')]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_ClassDetails, self).__init__(*args, **kwargs)
        roleData = json.loads(self.request.session[SessionProperties.USER_SELECTED_ROLE_KEY])
        self.fields['class_teacher'].choices = ClassFormsHelper().getTeachers(roleData)

    class_name = forms.CharField (
        max_length=30,
        min_length=1,
        required=True
    )

    class_division = forms.CharField(
        max_length=30,
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
            attrs={
                'type': 'date'
            }
        ),
        required=True
    )

    class_end_date = forms.DateField(
        widget=forms.widgets.DateInput(
            format="%Y-%m-%d",
            attrs={
                'type': 'date'
            }
        ),
        required=True
    )

    class_time_pattern = forms.CharField(
        widget=forms.Select(choices=TIMEPATTERN)
    )

    institution_levels = forms.ChoiceField(
        choices=Choice.InstitutionLevelAsChoice(),
        required=True
    )

    class_teacher = forms.ChoiceField(choices=[],required=False,initial=None)



    def clean(self):
        data = self.cleaned_data
        classStart = data["class_start_date"]
        classEnd = data["class_end_date"]
        if(classStart > classEnd):
            self.add_error("class_start_date", DisplayKey.get("class_end_date_prior_to_start_date_error"))
        return data