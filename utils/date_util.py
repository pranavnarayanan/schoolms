import datetime

class DateUtil():

    def makePyDateInstance(self, dateString, delimitor = '-', format='dmy'):
        format = format.lower()
        dateArray = dateString.split(delimitor)
        if format == 'dmy':
            return datetime.date(self.formatYear(int(dateArray[2])),int(dateArray[1]), int(dateArray[0]))
        elif format == 'dym':
            return datetime.date(self.formatYear(int(dateArray[1])), int(dateArray[2]), int(dateArray[0]))
        elif format == 'mdy':
            return datetime.date(self.formatYear(int(dateArray[2])), int(dateArray[0]), int(dateArray[1]))
        elif format == 'myd':
            return datetime.date(self.formatYear(int(dateArray[1])), int(dateArray[0]), int(dateArray[2]))
        elif format == 'ymd':
            return datetime.date(self.formatYear(int(dateArray[0])), int(dateArray[1]), int(dateArray[2]))
        elif format == 'ydm':
            return datetime.date(self.formatYear(int(dateArray[0])), int(dateArray[2]), int(dateArray[0]))
        elif format == 'dym':
            return datetime.date(self.formatYear(int(dateArray[1])), int(dateArray[2]), int(dateArray[1]))
        else:
            raise Exception("Invalid date Format [Format should be one amongst -> dmy,dym, mdy, myd, ymd, ydm, dym]")

    def formatYear(self, year):
        if(year < 1800):
            raise Exception("Invalid year | Year should be in YYYY format")
        else:
            return year

