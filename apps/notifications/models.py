from django.db import models
from apps.users.models import EN_Users

'''
# Notifications Entity
'''
class EN_Notifications(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(EN_Users, on_delete=models.DO_NOTHING, default=1, null=True, related_name='created_by')
    created_to = models.ForeignKey(EN_Users, on_delete=models.CASCADE, null=False, related_name='created_to')
    notification_type = models.CharField(max_length=50, null=False)
    seen = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    can_change_read_status_direclty = models.BooleanField(default=True, null=False)

    class Meta:
        db_table  = "en_notifications"