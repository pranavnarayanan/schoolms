from django.db import models
from apps.users.models import EN_Users

class EN_Message(models.Model):
    send_datetime = models.DateTimeField(null=False, auto_now_add=True)
    send_to = models.ForeignKey(EN_Users, null=False, on_delete=models.CASCADE, related_name='send_to')
    send_by = models.ForeignKey(EN_Users, null=False, on_delete=models.CASCADE, related_name='send_by')
    message = models.CharField(max_length=500, null=False)
    read_status = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "en_message"
        #aravind : dont create UNIQUE_TOGETHER -> Same messages can be repeated
