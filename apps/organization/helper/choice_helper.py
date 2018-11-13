from apps.organization.models import TL_Affiliation, TL_InstitutionType
from apps.utilities.entities.country import EN_Country

class Choice:

    @staticmethod
    def AffiliationAsChoice():
        chMainList = []
        for row in TL_Affiliation.objects.all():
            chList = []
            chList.append(row.code)
            chList.append(row.name)
            chMainList.append(tuple(chList))
        return tuple(chMainList)


    @staticmethod
    def InstitutionTypeAsChoice():
        chMainList = []
        for row in TL_InstitutionType.objects.all():
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