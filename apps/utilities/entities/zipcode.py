from django.db import models
from apps.utilities.entities.country import EN_Country

'''
# ENTITY : ZIPCODES
'''
class EN_Zipcode(models.Model):
    pincode  = models.CharField(max_length=8,  unique=False, null=False)
    city     = models.CharField(max_length=20, unique=False, null=False)
    district = models.CharField(max_length=20, unique=False, null=False)
    state    = models.CharField(max_length=20, unique=False, null=False)
    country  = models.ForeignKey(EN_Country, null=False, on_delete=models.PROTECT)
    class Meta:
        db_table = "en_zipcode"

