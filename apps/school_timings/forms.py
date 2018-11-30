from django import forms
from apps.school_timings.helper.school_timing_helper import SchoolTimingsHelper
from properties.calendar import DaysChoiceList

class FORM_SchoolTiming(forms.Form) :

    timing_name         = forms.CharField( max_length=50, required=True )
    school_start_time   = forms.TimeField( required=True, widget=forms.TimeInput(attrs={"type":"time"}))
    school_closing_time = forms.TimeField( required=True, widget=forms.TimeInput(attrs={"type":"time"}))
    school_off_days     = forms.MultipleChoiceField(choices = DaysChoiceList, required = False)
    total_periods       = forms.IntegerField(required=True)

    interval_1_starting_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_1_ending_time   = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_2_starting_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_2_ending_time   = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_3_starting_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_3_ending_time   = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_4_starting_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    interval_4_ending_time   = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))

    # --- FOOD BREAK DETAILS--------------------------------------------------#
    breakfast_break_starting_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    breakfast_break_ending_time   = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    lunch_break_starting_time     = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    lunch_break_ending_time       = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    dinner_break_starting_time    = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    dinner_break_ending_time      = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))

    #---ASSEMBLY DETAILS--------------------------------------------------#
    assembly_starting_time = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    assembly_ending_time   = forms.TimeField(required=False, widget=forms.TimeInput(attrs={"type": "time"}))
    assembly_on_days       = forms.MultipleChoiceField(choices=DaysChoiceList,required=False)
    #---------------------------------------------------------------------#

    def clean(self):
        data = self.cleaned_data
        sth = SchoolTimingsHelper()

        try:
            timing_name = data["timing_name"].trim()
        except Exception as e :
            self.add_error("timing_name", str(e))

        school_strt_time = None
        school_clsg_time = None

        try:
            school_start_time = sth.timeToMin(data["school_start_time"])
            school_strt_time = school_start_time
            try:
                school_closing_time = sth.timeToMin(data["school_closing_time"])
                school_clsg_time = school_closing_time
                if(school_closing_time - school_start_time < 60):
                    self.add_error("school_closing_time", "School closing time should be atleast 1hr after starting time")
                try:
                    if(int(data["total_periods"]) > 10):
                        self.add_error("total_periods", "Total Periods should be <= 10")
                    elif (int(data["total_periods"]) < 1):
                        self.add_error("total_periods", "Atleast 1 period should be present")
                except Exception as e:
                    self.add_error("school_closing_time", str(e))
            except Exception as e:
                self.add_error("school_closing_time", str(e))
        except Exception as e:
            self.add_error("school_start_time", str(e))

        if(school_strt_time != None and school_clsg_time != None):

            #First Interval Check
            interval_1_starting_time = data["interval_1_starting_time"]
            interval_1_ending_time = data["interval_1_ending_time"]
            if(interval_1_starting_time != None and interval_1_ending_time != None):
                if sth.timeToMin(interval_1_starting_time) - sth.timeToMin(data["school_start_time"]) < 20:
                    self.add_error("interval_1_ending_time","Interval should start atleast 20 mins after school start time")
                elif sth.timeToMin(data["school_closing_time"]) - sth.timeToMin(interval_1_ending_time) < 20:
                    self.add_error("interval_1_ending_time", "Interval should end 20 mins before school ending time")
                elif sth.timeToMin(interval_1_ending_time) - sth.timeToMin(interval_1_starting_time) >= 30:
                    self.add_error("interval_1_ending_time", "Interval Duration should be less than 30 mins")
                elif sth.timeToMin(interval_1_ending_time) - sth.timeToMin(interval_1_starting_time) <= 5:
                    self.add_error("interval_1_ending_time", "Interval Duration should be atleast 5 mins")
            elif(interval_1_starting_time != None and interval_1_ending_time == None):
                self.add_error("interval_1_ending_time", "Cannot be empty when interval starting time is not null")
            elif(interval_1_starting_time == None and interval_1_ending_time != None):
                self.add_error("interval_1_starting_time", "Cannot be empty when interval ending time is not null")

            #Second Interval Check
            interval_2_starting_time = data["interval_2_starting_time"]
            interval_2_ending_time = data["interval_2_ending_time"]
            if(interval_2_starting_time != None and interval_2_ending_time != None):
                if  sth.timeToMin(interval_2_starting_time) - sth.timeToMin(interval_1_ending_time) < 20:
                    self.add_error("interval_2_starting_time","Interval should start atleast 20 mins after the previous interval")
                elif sth.timeToMin(data["school_closing_time"]) - sth.timeToMin(interval_2_ending_time) < 20:
                    self.add_error("interval_2_ending_time", "Interval should end 20 mins before school ending time")
                elif sth.timeToMin(interval_2_ending_time) - sth.timeToMin(interval_2_starting_time) >= 30:
                    self.add_error("interval_2_ending_time", "Interval Duration should be less than 30 mins")
                elif sth.timeToMin(interval_2_ending_time) - sth.timeToMin(interval_2_starting_time) <= 5:
                    self.add_error("interval_2_ending_time", "Interval Duration should be atleast 5 mins")
            elif(interval_2_starting_time != None and interval_2_ending_time == None):
                self.add_error("interval_2_ending_time", "Cannot be empty when interval starting time is not null")
            elif(interval_2_starting_time == None and interval_2_ending_time != None):
                self.add_error("interval_2_starting_time", "Cannot be empty when interval ending time is not null")


            #Third Interval Check
            interval_3_starting_time = data["interval_3_starting_time"]
            interval_3_ending_time = data["interval_3_ending_time"]
            if(interval_3_starting_time != None and interval_3_ending_time != None):
                if  sth.timeToMin(interval_3_starting_time) - sth.timeToMin(interval_2_ending_time) < 20:
                    self.add_error("interval_3_starting_time","Interval should start atleast 20 mins after the previous interval")
                elif sth.timeToMin(data["school_closing_time"]) - sth.timeToMin(interval_3_ending_time) < 20:
                    self.add_error("interval_3_ending_time", "Interval should end 20 mins before school ending time")
                elif sth.timeToMin(interval_3_ending_time) - sth.timeToMin(interval_3_starting_time) >= 30:
                    self.add_error("interval_3_ending_time", "Interval Duration should be less than 30 mins")
                elif sth.timeToMin(interval_3_ending_time) - sth.timeToMin(interval_3_starting_time) <= 5:
                    self.add_error("interval_3_ending_time", "Interval Duration should be atleast 5 mins")
            elif(interval_3_starting_time != None and interval_3_ending_time == None):
                self.add_error("interval_3_ending_time", "Cannot be empty when interval starting time is not null")
            elif(interval_3_starting_time == None and interval_3_ending_time != None):
                self.add_error("interval_3_starting_time", "Cannot be empty when interval ending time is not null")


            #Fourth Interval Check
            interval_4_starting_time = data["interval_4_starting_time"]
            interval_4_ending_time = data["interval_4_ending_time"]
            if(interval_4_starting_time != None and interval_4_ending_time != None):
                if  sth.timeToMin(interval_4_starting_time) - sth.timeToMin(interval_3_ending_time) < 20:
                    self.add_error("interval_4_starting_time","Interval should start atleast 20 mins after the previous interval")
                elif sth.timeToMin(data["school_closing_time"]) - sth.timeToMin(interval_4_ending_time) < 20:
                    self.add_error("interval_4_ending_time", "Interval should end 20 mins before school ending time")
                elif sth.timeToMin(interval_4_ending_time) - sth.timeToMin(interval_4_starting_time) >= 30:
                    self.add_error("interval_4_ending_time", "Interval Duration should be less than 30 mins")
                elif sth.timeToMin(interval_4_ending_time) - sth.timeToMin(interval_4_starting_time) <= 5:
                    self.add_error("interval_4_ending_time", "Interval Duration should be atleast 5 mins")
            elif(interval_4_starting_time != None and interval_4_ending_time == None):
                self.add_error("interval_4_ending_time", "Cannot be empty when interval starting time is not null")
            elif(interval_4_starting_time == None and interval_4_ending_time != None):
                self.add_error("interval_4_starting_time", "Cannot be empty when interval ending time is not null")

            #Breakfast Timing Check
            breakfast_break_starting_time = data["breakfast_break_starting_time"]
            breakfast_break_ending_time = data["breakfast_break_ending_time"]
            if(breakfast_break_starting_time != None and breakfast_break_ending_time != None):
                if sth.timeToMin(breakfast_break_starting_time) - sth.timeToMin(school_strt_time) <= 0:
                    self.add_error("breakfast_break_starting_time", "Breakfast break should start on or after school start time")
                elif sth.timeToMin(school_clsg_time) - sth.timeToMin(breakfast_break_ending_time) > 0:
                    self.add_error("breakfast_break_ending_time", "Breakfast break should end before school closing time")
                elif sth.timeToMin(breakfast_break_ending_time) - sth.timeToMin(breakfast_break_starting_time) < 10:
                    self.add_error("breakfast_break_ending_time", "Breakfast break should be more than 10 Mins")
                elif sth.timeToMin(breakfast_break_ending_time) - sth.timeToMin(breakfast_break_starting_time) > 90:
                    self.add_error("breakfast_break_ending_time", "Breakfast break should not be more than 1.5 Hours")
            elif(breakfast_break_starting_time != None and breakfast_break_ending_time == None):
                self.add_error("breakfast_break_ending_time", "Cannot be empty when breakfast starting time is not null")
            elif(breakfast_break_starting_time == None and breakfast_break_ending_time != None):
                self.add_error("breakfast_break_starting_time", "Cannot be empty when breakfast ending time is not null")


            #Lunch Timing Check
            lunch_break_starting_time = data["lunch_break_starting_time"]
            lunch_break_ending_time = data["lunch_break_ending_time"]
            if(lunch_break_starting_time != None and lunch_break_ending_time != None):
                if sth.timeToMin(lunch_break_starting_time) - sth.timeToMin(school_strt_time) <= 0:
                    self.add_error("lunch_break_starting_time", "Lunch break should start on or after school start time")
                elif sth.timeToMin(school_clsg_time) - sth.timeToMin(lunch_break_ending_time) > 0:
                    self.add_error("lunch_break_ending_time", "Lunch break should end before school closing time")
                elif sth.timeToMin(lunch_break_ending_time) - sth.timeToMin(lunch_break_starting_time) < 10:
                    self.add_error("lunch_break_ending_time", "Lunch break should be more than 10 Mins")
                elif sth.timeToMin(lunch_break_ending_time) - sth.timeToMin(lunch_break_starting_time) > 90:
                    self.add_error("lunch_break_ending_time", "Lunch break should not be more than 1.5 Hours")
            elif(lunch_break_starting_time != None and lunch_break_ending_time == None):
                self.add_error("lunch_break_ending_time", "Cannot be empty when lunch starting time is not null")
            elif(lunch_break_starting_time == None and lunch_break_ending_time != None):
                self.add_error("lunch_break_starting_time", "Cannot be empty when lunch ending time is not null")


            #Dinner Timing Check
            dinner_break_starting_time = data["dinner_break_starting_time"]
            dinner_break_ending_time = data["dinner_break_ending_time"]
            if(dinner_break_starting_time != None and dinner_break_ending_time != None):
                if sth.timeToMin(dinner_break_starting_time) - sth.timeToMin(school_strt_time) <= 0:
                    self.add_error("dinner_break_starting_time", "Dinner break should start on or after school start time")
                elif sth.timeToMin(school_clsg_time) - sth.timeToMin(dinner_break_ending_time) > 0:
                    self.add_error("dinner_break_ending_time", "Dinner break should end before school closing time")
                elif sth.timeToMin(dinner_break_ending_time) - sth.timeToMin(dinner_break_starting_time) < 10:
                    self.add_error("dinner_break_ending_time", "Dinner break should be more than 10 Mins")
                elif sth.timeToMin(dinner_break_ending_time) - sth.timeToMin(dinner_break_starting_time) > 90:
                    self.add_error("dinner_break_ending_time", "dinner break should not be more than 1.5 Hours")
            elif(dinner_break_starting_time != None and dinner_break_ending_time == None):
                self.add_error("dinner_break_ending_time", "Cannot be empty when dinner starting time is not null")
            elif(dinner_break_starting_time == None and dinner_break_ending_time != None):
                self.add_error("dinner_break_starting_time", "Cannot be empty when dinner ending time is not null")


            #Assembly Timing Check
            assembly_starting_time = data["assembly_starting_time"]
            assembly_ending_time = data["assembly_ending_time"]
            if(assembly_starting_time != None and assembly_ending_time != None):
                assembly_on_days = data["assembly_on_days"]
                if(assembly_on_days == None):
                    self.add_error("assembly_on_days", "Assembly days are not specified")
                if sth.timeToMin(assembly_starting_time) - sth.timeToMin(school_strt_time) <= 0:
                    self.add_error("assembly_starting_time", "Assembly should start on or after school start time")
                elif sth.timeToMin(school_clsg_time) - sth.timeToMin(assembly_ending_time) > 0:
                    self.add_error("assembly_ending_time", "Assembly should end before school closing time")
                elif sth.timeToMin(assembly_ending_time) - sth.timeToMin(assembly_starting_time) < 5:
                    self.add_error("assembly_ending_time", "Assembly should be more than 5 Mins")
                elif sth.timeToMin(assembly_ending_time) - sth.timeToMin(assembly_starting_time) > 90:
                    self.add_error("assembly_ending_time", "Assembly should not be more than 1.5 Hours")
            elif(assembly_starting_time != None and assembly_ending_time == None):
                self.add_error("assembly_ending_time", "Cannot be empty when assembly starting time is not null")
            elif(assembly_starting_time == None and assembly_ending_time != None):
                self.add_error("assembly_starting_time", "Cannot be empty when assembly ending time is not null")

        else:
            pass



        return data
