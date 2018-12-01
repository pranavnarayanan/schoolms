from django.db import models
from django.utils import timezone
from apps.users.models import EN_Users

class EN_Documents(models.Model):
    file_name = models.FileField(max_length=30, null=False,unique=False,upload_to='documents/')
    unique_name = models.CharField(max_length=100, null=False,unique=True)
    file_description = models.CharField(max_length=300, null=True,unique=False)
    tag = models.CharField(max_length=50, null=True,unique=False)
    type = models.CharField(max_length=30, null=False,unique=True)
    uploaded_on = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(EN_Users, null=False, on_delete=models.CASCADE)
    no_of_days_to_keep_file = models.IntegerField(null=True)

    class Meta:
        db_table = "en_documents"