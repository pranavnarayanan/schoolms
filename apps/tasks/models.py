from django.db import models

from apps.users.models import EN_Users


class EN_Tasks(models.Model):
    created_date  = models.DateTimeField(null=False, auto_now_add=True)
    to_be_done_on = models.DateField(null=False)
    to_be_done_at = models.TimeField(null=True)
    priority      = models.IntegerField(null=False, default=3)
    assigned_to   = models.ForeignKey(EN_Users, null=True, on_delete=models.CASCADE, related_name='assigned_to')
    assigned_by   = models.ForeignKey(EN_Users, null=False, on_delete=models.CASCADE, related_name='assigned_by')
    task          = models.CharField(max_length=200, null=False)
    done_status   = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "en_tasks"
        unique_together = ('to_be_done_on', 'to_be_done_at', 'assigned_to','task')

