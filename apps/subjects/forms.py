from django import forms
from apps.subjects.forms_helper import SubjectFormsHelper

class FORM_SubjectDetails(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_SubjectDetails, self).__init__(*args, **kwargs)
        self.fields['assign_to_class'].choices = SubjectFormsHelper().getClasses()


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