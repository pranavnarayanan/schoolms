from django import forms

from apps.subjects.forms_helper import SubjectFormsHelper


class FORM_SubjectDetails(forms.Form) :

    subject_name = forms.CharField(
        required=True
    )

    subject_duration = forms.IntegerField(
        required=True
    )

    assign_to_class = forms.MultipleChoiceField(
        choices = SubjectFormsHelper().getClasses(),
        required=True
    )

def clean(self):
    data = self.cleaned_data
    return data