from django.db import models

'''
# TYPELIST : ACCOUNT STATUS
'''
class TL_AccountStatus(models.Model):
    code        = models.CharField(max_length=10, unique=True,  null=False)
    name        = models.CharField(max_length=10, unique=False, null=False)
    description = models.TextField(null=True)
    class Meta:
        db_table = "tl_account_status"



