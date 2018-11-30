from datetime import datetime

class SchoolTimingsHelper():

    def convert12To24Format(self,str_time):
        time_format = "%H:%M %p"
        time = datetime.strptime(str_time, time_format).time()

        if "PM" in str_time.upper():
            hour = 12 + time.hour if time.hour != 12 else 12
        else:
            hour = 0 if time.hour == 12 else time.hour

        return time.replace(hour=hour)


    def timeToMin(self, time):
        return ((time.hour * 60) + time.minute)