from django.db import models
from apps.books.models import EN_Books
from apps.classes.models import EN_Classes
from apps.organization.models import EN_Organization
from apps.roles.models import EN_UserRoles
from apps.users.models import EN_Users

'''
    Table   : Subjects
'''
class EN_Subjects(models.Model):
    subject_name = models.CharField(max_length=100, null=False)
    tag = models.CharField(max_length=100, null=True)
    duration = models.IntegerField(null=True)
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)
    class Meta:
        db_table = "en_subjects"
        unique_together = ("subject_name","tag","organization")


'''
    Table : Subjects Books
    Note  : Org is kept for eazy filtering purpose
'''
class EN_SubjectBooks(models.Model):
    subject = models.ForeignKey(EN_Subjects, on_delete=models.CASCADE, null=False)
    book = models.ForeignKey(EN_Books, on_delete=models.PROTECT, null=False)
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)
    class Meta:
        db_table = "en_subject_books"
        unique_together = ("subject", "book", "organization")


'''
    Table   : Class Subjects
'''
class EN_ClassSubjects(models.Model):
    subject = models.ForeignKey(EN_Subjects, on_delete=models.CASCADE, null=False)
    class_fk = models.ForeignKey(EN_Classes, on_delete=models.CASCADE, null=False)
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)
    class Meta:
        db_table = "en_class_subjects"
        unique_together = ("subject", "class_fk", "organization")



'''
    Table   : Subject Teachers
'''
class EN_SubjectTeachers(models.Model):
    class_subject = models.ForeignKey(EN_ClassSubjects, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(EN_Users, on_delete=models.CASCADE, null=False)
    # NOTE:
    # teacher_role is to protect the particular entry on this table, when TEACHER role is removed
    # for the particular user.
    teacher_role = models.ForeignKey(EN_UserRoles, on_delete=models.PROTECT, null=False)
    note    = models.CharField(max_length=150, null=True)
    organization = models.ForeignKey(EN_Organization, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "en_subject_teachers"
        unique_together = ("class_subject", "teacher",)


