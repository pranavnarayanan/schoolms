from django.db import models
from apps.users.models import EN_Users
from apps.utilities.entities.sequenceutil import EN_SequenceUtil

class EN_Documents(models.Model):
    data_file = models.FileField(max_length=500, null=True, upload_to='documents/')
    parent_folder = models.ForeignKey("EN_Documents", null=True, on_delete=models.CASCADE)
    is_file = models.BooleanField(default=False,null=False)
    is_folder = models.BooleanField(default=False,null=False)
    type = models.CharField(max_length=30, null=True)
    file_size = models.IntegerField(null=True)
    name = models.CharField(max_length=100, null=False)
    unique_name = models.CharField(max_length=500, null=False, unique=True, default=("doc_{}".format(EN_SequenceUtil.next("UNIQUE_FILE_NAME"))))
    description = models.CharField(max_length=1000, null=True)
    owner = models.ForeignKey(EN_Users, null=False, on_delete=models.CASCADE)
    no_of_days_to_keep_file = models.IntegerField(null=True)
    moved_to_aws = models.BooleanField(default=False)
    is_root = models.BooleanField(default=False)

    class Meta:
        db_table = "en_documents"