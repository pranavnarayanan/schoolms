from django import forms
from apps.school_timings.helper.school_timing_helper import SchoolTimingsHelper
from properties.calendar import DaysChoiceList

class FORM_SchoolTiming(forms.Form) :

    timing_name         = forms.CharField( max_length=50, required=True )
    school_start_time   = forms.TimeField( required=True, widget=forms.TimeInput(attrs={"type":"time"}))
    school_closing_time = forms.TimeField( required=True, widget=forms.TimeInput(attrs={"type":"time"}))
    school_off_days     = forms.MultipleChoiceField(choices = DaysChoiceList, required = False)
    total_periods       = forms.IntegerField(required=True)
    assembly_on_days    = forms.MultipleChoiceField(choices=DaysChoiceList,required=False)
    assembly_duration   = forms.IntegerField(required=False)

    def clean(self):
        data = self.cleaned_data
        sth = SchoolTimingsHelper()
        return data
