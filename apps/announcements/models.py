from django.db import models
from apps.organization.models import EN_OrganizationGroup
from apps.users.models import EN_Users


class EN_Announcements(models.Model):
    content = models.CharField(max_length=1000, null=False)
    sms_content = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(null=False)
    priority = models.SmallIntegerField(default=3)
    announced_by= models.ForeignKey(EN_Users, null=False, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "en_announcements"


class EN_AnnouncementRecipients(models.Model):
    organization_group = models.ForeignKey(EN_OrganizationGroup, null=False, on_delete=models.DO_NOTHING)
    organization = models.CharField(max_length=255, null=True)
    class_fk = models.CharField(max_length=255, null=True)
    role = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = "en_announcement_recipients"



