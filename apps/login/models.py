from django.db import models
from django.utils import timezone
from apps.users.models import EN_Users

'''
# ENTITY : LOGIN CREDENTIALS
'''
class EN_LoginCredentials(models.Model):
    username               = models.CharField(max_length=25, unique=True, null=False)
    password               = models.CharField(max_length=25, null=False)
    password_history       = models.CharField(max_length=130, null=True)
    last_logged_in_time    = models.DateTimeField(null=True)
    current_logged_in_time = models.DateTimeField(default=timezone.now)
    is_online              = models.BooleanField(default=False,null=False)
    user                   = models.OneToOneField(EN_Users,on_delete=models.CASCADE)
    class Meta:
        db_table = "en_login_credentials"

