import json
from django import forms
from apps.roles.models import EN_UserRoles
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
            ch = (st.id,st.timing_name)
            choiceList.append(ch)
        self.fields['available_timings'].choices = tuple(choiceList)

        if "PAGE_1_DATA" in self.request.session:
            page1Data = json.loads(self.request.session["PAGE_1_DATA"])
            if page1Data["school_timing_id"] == 0:
                self.fields['school_timing_name'].initial = page1Data["school_timing_name"]
            else:
                self.fields['available_timings'].initial = page1Data["school_timing_id"]
                self.fields['school_timing_name'].initial = ""

    school_timing_name = forms.CharField( max_length=50, required=False )
    available_timings  = forms.ChoiceField(required=False, choices=[])

    def clean(self):
        data = self.cleaned_data
        if self.request.POST["type"] == "new" and data["school_timing_name"] == "":
            self.add_error("school_timing_name","School timing name is mandatory")
        else:
            if data["available_timings"] == "" or data["available_timings"] == None:
                self.add_error("available_timings", "Modification can be done only after selecting a timing")
        return data



class FORM_SchoolTiming(forms.Form) :

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FORM_SchoolTiming, self).__init__(*args, **kwargs)
        page1_data = json.loads(self.request.session["PAGE_1_DATA"])
        self.fields['school_timing_id'].initial = page1_data["school_timing_id"]
        if int(page1_data["school_timing_id"]) != 0:
            st = EN_SchoolTimings.objects.get(id=page1_data["school_timing_id"])
            self.fields['school_timing_name'].initial = st.timing_name
            self.fields['school_start_time'].initial = st.school_starting_time
            self.fields['school_closing_time'].initial = st.school_closing_time
            self.fields['total_periods'].initial = st.no_of_periods
            self.fields['assembly_duration'].initial = st.assembly_duration

            self.fields['class_on_sunday'].initial = st.class_on_sunday
            self.fields['class_on_monday'].initial = st.class_on_monday
            self.fields['class_on_tuesday'].initial = st.class_on_tuesday
            self.fields['class_on_wednesday'].initial = st.class_on_wednesday
            self.fields['class_on_thursday'].initial = st.class_on_thursday
            self.fields['class_on_friday'].initial = st.class_on_friday
            self.fields['class_on_saturday'].initial = st.class_on_saturday

            self.fields['assembly_on_sunday'].initial = st.assembly_on_sunday
            self.fields['assembly_on_monday'].initial = st.assembly_on_monday
            self.fields['assembly_on_tuesday'].initial = st.assembly_on_tuesday
            self.fields['assembly_on_wednesday'].initial = st.assembly_on_wednesday
            self.fields['assembly_on_thursday'].initial = st.assembly_on_thursday
            self.fields['assembly_on_friday'].initial = st.assembly_on_friday
            self.fields['assembly_on_saturday'].initial = st.assembly_on_saturday

        else:
            self.fields['school_timing_name'].initial = page1_data["school_timing_name"]

    school_timing_id    = forms.IntegerField(widget=forms.HiddenInput())
    school_timing_name  = forms.CharField(max_length=50, required=False)
    school_start_time   = forms.TimeField( required=False, widget=forms.TimeInput(attrs={"type":"time"}))
    school_closing_time = forms.TimeField( required=False, widget=forms.TimeInput(attrs={"type":"time"}))
    school_off_days     = forms.MultipleChoiceField(choices = DaysChoiceList, required = False)
    total_periods       = forms.IntegerField(required=False)
    assembly_on_days    = forms.MultipleChoiceField(choices=DaysChoiceList,required=False)
    assembly_duration   = forms.IntegerField(required=False)

    class_on_sunday = forms.BooleanField(required=False)
    class_on_monday = forms.BooleanField(required=False)
    class_on_tuesday = forms.BooleanField(required=False)
    class_on_wednesday = forms.BooleanField(required=False)
    class_on_thursday = forms.BooleanField(required=False)
    class_on_friday = forms.BooleanField(required=False)
    class_on_saturday = forms.BooleanField(required=False)

    assembly_on_sunday = forms.BooleanField(required=False)
    assembly_on_monday = forms.BooleanField(required=False)
    assembly_on_tuesday = forms.BooleanField(required=False)
    assembly_on_wednesday = forms.BooleanField(required=False)
    assembly_on_thursday = forms.BooleanField(required=False)
    assembly_on_friday = forms.BooleanField(required=False)
    assembly_on_saturday = forms.BooleanField(required=False)

    assembly_error_field = forms.IntegerField(required=False)

    def clean(self):
        data = self.cleaned_data
        if data["school_start_time"] == None or data["school_start_time"] == "":
            self.add_error("school_start_time","School starting time is mandatory")
        if data["school_closing_time"] == None or data["school_closing_time"] == "":
            self.add_error("school_closing_time","School closing time is mandatory")

        if data["total_periods"] != None:
            try:
                if int(data["total_periods"]) < 1:
                    self.add_error("total_periods","Atleast one period should be there.")
                elif int(data["total_periods"]) > 12:
                    self.add_error("total_periods","Max 12 periods are permitted")
            except:
                self.add_error("total_periods", "Expecting a number value")
        else:
            self.add_error("total_periods", "Expecting a value between 1 and 12")


        if data["assembly_duration"] != None:
            try:
                if int(data["assembly_duration"]) < 15:
                    self.add_error("assembly_duration","Assembly should be atleast for 15 mins.")
                elif int(data["assembly_duration"]) > 60:
                    self.add_error("assembly_duration","Assembly should not exceed 60 mins")
            except:
                self.add_error("assembly_duration", "Expecting a number value")
        else:
            if data["assembly_on_sunday"] or data["assembly_on_monday"] or data["assembly_on_tuesday"] or data[
                "assembly_on_wednesday"] or data["assembly_on_thursday"] or data["assembly_on_friday"] or data[
                "assembly_on_saturday"]:
                self.add_error("assembly_duration", "Expecting a value when assembly dates are specified")


        if data["assembly_on_sunday"] and not data["class_on_sunday"]:
            self.add_error("assembly_error_field", "Sunday is a holiday")
        if data["assembly_on_monday"] and not data["class_on_monday"]:
            self.add_error("assembly_error_field", "Monday is a holiday")
        if data["assembly_on_tuesday"] and not data["class_on_tuesday"]:
            self.add_error("assembly_error_field", "Tuesday is a holiday")
        if data["assembly_on_wednesday"] and not data["class_on_wednesday"]:
            self.add_error("assembly_error_field", "Wednesday is a holiday")
        if data["assembly_on_thursday"] and not data["class_on_thursday"]:
            self.add_error("assembly_error_field", "Thursday is a holiday")
        if data["assembly_on_friday"] and not data["class_on_friday"]:
            self.add_error("assembly_error_field", "Friday is a holiday")
        if data["assembly_on_saturday"] and not data["class_on_saturday"]:
            self.add_error("assembly_error_field", "Saturday is a holiday")

        if (not data["assembly_on_sunday"] and not data["assembly_on_monday"] and not data["assembly_on_tuesday"] and not data[
            "assembly_on_wednesday"] and not data["assembly_on_thursday"] and not data["assembly_on_friday"] and not data[
            "assembly_on_saturday"]):
            if data["assembly_duration"] != None:
                self.add_error("assembly_error_field", "Expecting assembly days when duration is specified")



        return data
