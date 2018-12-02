from django.db import models

from apps.classes.models import EN_Classes

'''
    Table   : ClassSubjects
'''
class EN_ClassSubjects(models.Model):
    class_fk = models.ForeignKey(EN_Classes, on_delete=models.CASCADE, null=False)
    subject_name = models.CharField(max_length=100, null=True)
    duration = models.IntegerField(null=True)

    class Meta:
        db_table = "en_class_subjects"
        unique_together = ("class_fk", "subject_name",)
