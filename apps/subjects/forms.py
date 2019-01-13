import json

from django import forms
from apps.subjects.forms_helper import SubjectFormsHelper
from properties.session_properties import SessionProperties

class FORM_ClassNamesForSubject(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_ClassNamesForSubject, self).__init__(*args, **kwargs)
        fh = SubjectFormsHelper(self.request)
        self.fields['class_names'].choices = fh.getClassesForFilter()
        self.fields['class_div'].choices = fh.getDivisionForFilter()

    class_names = forms.ChoiceField(choices=[], required=False, initial=None)
    class_div = forms.ChoiceField(choices=[], required=False, initial=None)


class FORM_SubjectDetails(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_SubjectDetails, self).__init__(*args, **kwargs)
        roleData = json.loads(self.request.session[SessionProperties.USER_SELECTED_ROLE_KEY])
        self.fields['assign_to_class'].choices = SubjectFormsHelper(self.request).getClasses(roleData)


    subject_name = forms.CharField(
        required=True
    )

    subject_duration = forms.IntegerField(
        required=True
    )

    assign_to_class = forms.MultipleChoiceField(required=True, choices=[])


def clean(self):
    data = self.cleaned_data
    return data