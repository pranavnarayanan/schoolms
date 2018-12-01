from django.db import models

from apps.organization.models import EN_Organization, TL_InstitutionLevels
from apps.school_timings.models import EN_SchoolTimings

'''
    Table   : Classes
'''
class EN_Classes(models.Model):
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)
    class_name = models.CharField(max_length=100, null=False)
    batch_nick_name = models.CharField(max_length=100, null=True)
    academic_starting_year = models.DateField(null=False)
    academic_ending_year = models.DateField(null=True)
    batch_name = models.CharField(max_length=100,null=False)
    timing = models.ForeignKey(EN_SchoolTimings, on_delete=models.PROTECT, null=False)
    organization_level = models.ForeignKey(TL_InstitutionLevels, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "en_classes"
        unique_together = ("organization","class_name","academic_starting_year")

