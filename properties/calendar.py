from enum import Enum

class Days(Enum):
    MONDAY     = "Monday"
    TUESDAY    = "Tuesday"
    WEDNESDAY  = "Wednesday"
    THURSDAY   = "Thursday"
    FRIDAY     = "Friday"
    SATURDAY   = "Saturday"
    SUNDAY     = "Sunday"

    DaysList = [MONDAY, TUESDAY, WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY]

class IntegerDays(Enum):
    MONDAY     = 1
    TUESDAY    = 2
    WEDNESDAY  = 3
    THURSDAY   = 4
    FRIDAY     = 5
    SATURDAY   = 6
    SUNDAY     = 7


class Months(Enum):
    JANUARY   = "January"
    FEBRUARY  = "February"
    MARCH     = "March"
    APRIL     = "April"
    MAY       = "May"
    JUNE      = "June"
    JULY      = "July"
    AUGUST    = "August"
    SEPTEMBER = "September"
    OCTOBER   = "October"
    NOVEMBER  = "November"
    DECEMBER  = "December"

    MonthsList = [JANUARY,FEBRUARY,MARCH,APRIL,MAY,JUNE,JULY,AUGUST,SEPTEMBER,OCTOBER,NOVEMBER,DECEMBER]

class IntegerMonths(Enum):
    JANUARY   = 1
    FEBRUARY  = 2
    MARCH     = 3
    APRIL     = 4
    MAY       = 5
    JUNE      = 6
    JULY      = 7
    AUGUST    = 8
    SEPTEMBER = 9
    OCTOBER   = 10
    NOVEMBER  = 11
    DECEMBER  = 12

DaysChoiceList = (
    (Days.SUNDAY.value,Days.SUNDAY.value),
    (Days.MONDAY.value,Days.MONDAY.value),
    (Days.TUESDAY.value,Days.TUESDAY.value),
    (Days.WEDNESDAY.value,Days.WEDNESDAY.value),
    (Days.THURSDAY.value,Days.THURSDAY.value),
    (Days.FRIDAY.value,Days.FRIDAY.value),
    (Days.SATURDAY.value,Days.SATURDAY.value)
)
