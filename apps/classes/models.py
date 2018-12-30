from django.db import models
from apps.organization.models import EN_Organization, TL_InstitutionLevels
from apps.school_timings.models import EN_SchoolTimings
from apps.users.models import EN_Users

'''
    Table   : Classes
'''
class EN_Classes(models.Model):
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)
    class_name = models.CharField(max_length=30, null=False)
    class_division = models.CharField(max_length=1, null=True)
    batch_nick_name = models.CharField(max_length=50, null=True)
    academic_starting_year = models.DateField(null=False)
    academic_ending_year = models.DateField(null=True)
    batch_name = models.CharField(max_length=100,null=False)
    timing = models.ForeignKey(EN_SchoolTimings, on_delete=models.PROTECT, null=False)
    organization_level = models.ForeignKey(TL_InstitutionLevels, on_delete=models.PROTECT, null=False)
    class_teacher = models.ForeignKey(EN_Users, on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = "en_classes"
        unique_together = ("organization","class_name","class_division","academic_starting_year")

