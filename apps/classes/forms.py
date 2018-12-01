from django import forms

from displaykey.display_key import DisplayKey
from apps.organization.helper.choice_helper import Choice

class FORM_ClassDetails(forms.Form) :

    TIMEPATTERN = [('lkg', 'SRS LKG Pattern'),
                   ('1to4','SRS 1 to 4 Pattern'),
                   ('5to7','SRS 5 to 7 Pattern'),
                   ('8to10','SRS 8 to 10 Pattern'),
                   ('11and12','SRS 11 and 12 Pattern')]

    class_name = forms.CharField (
        max_length=30,
        min_length=1,
        required=True
    )

    class_nickname = forms.CharField(
        max_length=30
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



    def clean(self):
        data = self.cleaned_data
        classStart = data["class_start_date"]
        classEnd = data["class_end_date"]
        if(classStart > classEnd):
            self.add_error("class_start_date", DisplayKey.get("class_end_date_prior_to_start_date_error"))
        return data