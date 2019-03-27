from django.db import models
from django.utils import timezone
from apps.classes.models import EN_Classes
from apps.organization.models import EN_Organization
#from apps.subjects.models import EN_ClassSubjects
from apps.users.models import EN_Users

class EN_Attendance(models.Model):
    date = models.DateField(default=timezone.now)
    organization = models.ForeignKey(EN_Organization, null=False, on_delete=models.DO_NOTHING)
    attendance_for_class = models.ForeignKey(EN_Classes, null=False, on_delete=models.DO_NOTHING)
    attendance_by = models.ForeignKey(EN_Users, null=False, on_delete=models.DO_NOTHING)
 #   subject = models.ForeignKey(EN_ClassSubjects, null=False, on_delete=models.DO_NOTHING)
    duration = models.IntegerField()
    attendance_took_time = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "en_attendance"


class EN_ClassAbsentees(models.Model):
    attendance = models.ForeignKey(EN_Attendance, null=False, on_delete=models.CASCADE)
    student = models.ForeignKey(EN_Users, null=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "en_student_attendance"

