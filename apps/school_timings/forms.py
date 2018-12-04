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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_SchoolTiming, self).__init__(*args, **kwargs)
        page1_data = json.loads(self.request.session["PAGE_1_DATA"])
        self.fields['timing_name'].school_timing_id = page1_data["school_timing_id"]
        if int(page1_data["school_timing_id"]) != 0:
            st = EN_SchoolTimings.objects.get(id=page1_data["school_timing_id"])
            self.fields['timing_name'].initial = st.timing_name
            self.fields['school_start_time'].initial = st.school_starting_time
            self.fields['school_closing_time'].initial = st.school_closing_time
            self.fields['school_off_days'].initial = {'category':tuple(st.off_days.split(","))}
            self.fields['total_periods'].initial = st.no_of_periods
            self.fields['assembly_on_days'].initial = {'category':tuple(st.assembly_on_days.split(","))}
            self.fields['assembly_duration'].initial = st.assembly_duration
        else:
            self.fields['timing_name'].initial = page1_data["school_timing_name"]

    timing_id           = forms.IntegerField(widget=forms.HiddenInput())
    timing_name         = forms.CharField(max_length=50, required=True)
    school_start_time   = forms.TimeField( required=True, widget=forms.TimeInput(attrs={"type":"time"}))
    school_closing_time = forms.TimeField( required=True, widget=forms.TimeInput(attrs={"type":"time"}))
    school_off_days     = forms.MultipleChoiceField(choices = DaysChoiceList, required = False)
    total_periods       = forms.IntegerField(required=True)
    assembly_on_days    = forms.MultipleChoiceField(choices=DaysChoiceList,required=False)
    assembly_duration   = forms.IntegerField(required=False)


    class_on_sunday = forms.BooleanField()
    class_on_monday = forms.BooleanField()
    class_on_tuesday = forms.BooleanField()
    class_on_wednesday = forms.BooleanField()
    class_on_thursday = forms.BooleanField()
    class_on_friday = forms.BooleanField()
    class_on_saturday = forms.BooleanField()
    assembly_on_sunday = forms.BooleanField()
    assembly_on_monday = forms.BooleanField()
    assembly_on_tuesday = forms.BooleanField()
    assembly_on_wednesday = forms.BooleanField()
    assembly_on_thursday = forms.BooleanField()
    assembly_on_friday = forms.BooleanField()
    assembly_on_saturday = forms.BooleanField()


    def clean(self):
        data = self.cleaned_data
        return data
