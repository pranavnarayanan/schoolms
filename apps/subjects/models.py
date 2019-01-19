from django.db import models
from apps.classes.models import EN_Classes
from apps.organization.models import EN_Organization
from apps.roles.models import EN_UserRoles
from apps.users.models import EN_Users

'''
    Table   : ClassSubjects
'''
class EN_ClassSubjects(models.Model):
    class_fk = models.ForeignKey(EN_Classes, on_delete=models.CASCADE, null=False)
    subject_name = models.CharField(max_length=100, null=True)
    duration = models.IntegerField(null=True)
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)
    class Meta:
        db_table = "en_class_subjects"
        unique_together = ("class_fk", "subject_name","organization")



'''
    Table   : Subject Teachers
'''
class EN_SubjectTeachers(models.Model):
    subject = models.ForeignKey(EN_ClassSubjects, on_delete=models.CASCADE, null=False)
    teacher = models.ForeignKey(EN_Users, on_delete=models.CASCADE, null=False)
    # NOTE:
    # teacher_role is to protect the particular entry on this table, when TEACHER role is removed
    # for the particular user.
    teacher_role = models.ForeignKey(EN_UserRoles, on_delete=models.PROTECT, null=False)
    note    = models.CharField(max_length=150, null=True)
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "en_subject_teachers"
        unique_together = ("subject", "teacher",)


