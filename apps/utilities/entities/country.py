from django.db import models

'''
# ENTITY : COUNTRIES
'''
class EN_Country(models.Model):
    name        = models.CharField(max_length=100, null=False, unique=True)
    mobile_code = models.CharField(max_length=5, null=False)
    css_code    = models.CharField(max_length=15, null=False)
    class Meta:
        db_table = "en_country"
        unique_together = ('name', 'mobile_code', 'css_code')
