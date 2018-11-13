from apps.users.models import TL_Gender
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.zipcode import EN_Zipcode


class Choice:

    @staticmethod
    def genderAsChoice():
        chMainList = []
        for row in TL_Gender.objects.all():
            chList = []
            chList.append(row.code)
            chList.append(row.name)
            chMainList.append(tuple(chList))
        return tuple(chMainList)


    @staticmethod
    def countryMobileCodes():
        chMainList = []
        for row in EN_Country.objects.all():
            chList = []
            chList.append(row.id)
            chList.append(row.mobile_code + " : " + row.name)
            chMainList.append(tuple(chList))
        return tuple(chMainList)


    @staticmethod
    def getZipcodeAreas(pincode = 000000):
        chMainList = []
        for row in EN_Zipcode.objects.filter(pincode=pincode):
            chList = []
            chList.append(row.id)
            chList.append(row.city + ", " + row.name)
            chMainList.append(tuple(chList))
        return tuple(chMainList)
