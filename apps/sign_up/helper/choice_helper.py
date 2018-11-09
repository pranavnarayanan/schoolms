from apps.users.models import TL_Gender
from apps.utilities.entities.country import EN_Country

class Choice:

    @staticmethod
    def genderAsChoice():
        chMailList = []
        for row in TL_Gender.objects.all():
            chList = []
            chList.append(row.code)
            chList.append(row.name)
            chMailList.append(tuple(chList))
        return tuple(chMailList)


    @staticmethod
    def countryMobileCodes():
        chMailList = []
        for row in EN_Country.objects.all():
            chList = []
            chList.append(row.id)
            chList.append(row.mobile_code + " : " + row.name)
            chMailList.append(tuple(chList))
        return tuple(chMailList)
