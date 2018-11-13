from django.db import models
from django.core.exceptions import ValidationError
from apps.roles.models import EN_UserRoles
from apps.users.models import EN_Users

'''
# Activity Pattern
'''
class EN_ActivityPattern(models.Model):
    pattern_name    = models.CharField(max_length=100, unique=True, null=False)
    subject         = models.CharField(max_length=100, unique=False, null=False)
    description     = models.CharField(max_length=500, unique=False, null=False)
    priority        = models.IntegerField(null=False, default=5)
    escalation_days = models.IntegerField(null=False, default=10)
    class Meta:
        db_table  = "en_activity_pattern"


'''
# Activity Entity
'''
class EN_Activity(models.Model):
    pattern = models.ForeignKey(EN_ActivityPattern, on_delete=models.CASCADE, null=False, related_name='pattern')
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EN_Users, on_delete=models.CASCADE, null=True, related_name='created_by')
    created_to = models.ForeignKey(EN_Users, on_delete=models.CASCADE, null=False, related_name='created_to')
    table_name = models.CharField(max_length=100, unique=False, null=True)
    en_user_role = models.ForeignKey(EN_UserRoles, on_delete=models.CASCADE, null=True, related_name='en_user_roles')
    read_status = models.BooleanField(default=False)
    escalated_from = models.ForeignKey(EN_Users, on_delete=models.CASCADE, null=True, related_name='escalated_from')
    can_change_read_status_direclty = models.BooleanField(default=True, null=False)

    class Meta:
        db_table  = "en_activity"

    def validate_unique(self, exclude=None):
        this = EN_Activity.objects.exclude(id=self.id).filter(
            table_name=self.table_name,
            pattern=self.pattern,
            created_on=self.created_on,
            created_to=self.created_to,
            read_status=self.read_status)

        if self.en_user_role != None:
            if this.filter(en_user_role=self.en_user_role).exists():
                raise ValidationError("Duplicate Entry On UserRoles on Activity Entity")

