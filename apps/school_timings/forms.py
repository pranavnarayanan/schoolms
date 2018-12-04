import json
from django import forms
from apps.roles.models import EN_UserRoles
from apps.school_timings.helper.school_timing_helper import SchoolTimingsHelper
from apps.school_timings.models import EN_SchoolTimings
from properties.calendar import DaysChoiceList
from properties.session_properties import SessionProperties


class FORM_AddModifySchoolTiming_Page1(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_AddModifySchoolTiming_Page1, self).__init__(*args, **kwargs)
        active_role = json.loads(self.request.session[SessionProperties.USER_SELECTED_ROLE_KEY])
        active_role = EN_UserRoles.objects.get(id=active_role["role_id"])
        schoolTimings = EN_SchoolTimings.objects.filter(organization=active_role.related_organization)
        choiceList = []
        for st in schoolTimings:
            ch = (st.id,"{} - {} to {} ".format(st.timing_name,st.school_starting_time,st.school_closing_time))
            choiceList.append(ch)
        self.fields['available_timings'].choices = tuple(choiceList)

    timing_name       = forms.CharField( max_length=50, required=False )
    available_timings = forms.ChoiceField(required=False, choices=[])


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
