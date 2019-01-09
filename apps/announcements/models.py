from django.db import models
from apps.classes.models import EN_Classes
from apps.organization.models import EN_OrganizationGroup, EN_Organization
from apps.roles.models import TL_Roles
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
    organization_group = models.ForeignKey(EN_OrganizationGroup, null=True, on_delete=models.DO_NOTHING)
    organization = models.ForeignKey(EN_Organization, null=True, on_delete=models.DO_NOTHING)
    class_fk = models.ForeignKey(EN_Classes, null=True, on_delete=models.DO_NOTHING)
    role = models.ForeignKey(TL_Roles, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "en_announcement_recipients"



