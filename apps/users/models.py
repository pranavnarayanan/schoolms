from django.db import models
from apps.utilities.entities.account_status import TL_AccountStatus
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.zipcode import EN_Zipcode

'''
# TYPELIST : GENDER 
'''
class TL_Gender(models.Model):
    code        = models.CharField(max_length=10, unique=True,  null=False)
    name        = models.CharField(max_length=10, unique=False, null=False)
    description = models.TextField(null=True)
    class Meta:
        db_table = "tl_gender"


'''
# ENTITY : CONTACTS
'''
class EN_Contacts(models.Model):
    mobile_country_code  = models.ForeignKey(EN_Country, null=False, on_delete=models.DO_NOTHING)
    mobile_number        = models.CharField(max_length=10, null=False)
    secondary_number     = models.CharField(max_length=15, null=True)
    is_landline_number   = models.BooleanField(default=True)
    email_id             = models.EmailField(null=True, unique=True)
    website              = models.CharField(max_length=100, null=True)
    publish_your_site    = models.BooleanField(default=False)
    class Meta:
        db_table = "en_contacts"


'''
# ENTITY : USERS
'''
class EN_Users(models.Model):
    product_id           = models.CharField(max_length=15, unique=True, null=False)
    name                 = models.CharField(max_length=12, null=False)
    date_of_birth        = models.DateField(null=False)
    gender               = models.ForeignKey(TL_Gender, null=False, on_delete=models.PROTECT)
    display_picture      = models.CharField(max_length=100, null=True)
    account_status       = models.ForeignKey(TL_AccountStatus, null=False, on_delete=models.PROTECT)
    contact              = models.OneToOneField(EN_Contacts,on_delete=models.CASCADE)
    newsletter_subscribe = models.BooleanField(default=True)
    class Meta:
        db_table = "en_users"


'''
# ENTITY : ADDRESS BOOK
'''
class EN_AddressBook(models.Model):
    user                 = models.ForeignKey(EN_Users, on_delete=models.DO_NOTHING, null=False)
    house_name           = models.CharField(max_length=100, unique=False, null=False)
    street               = models.CharField(max_length=100, unique=False, null=True)
    landmark             = models.CharField(max_length=100, unique=False, null=True)
    zipcode              = models.ForeignKey(EN_Zipcode, on_delete=models.PROTECT, null=False)
    is_current_address   = models.BooleanField(default=True)
    is_permanent_address = models.BooleanField(default=False)
    class Meta:
        db_table  = "en_address_book"
        unique_together = ('user', 'house_name', 'zipcode', 'is_current_address','is_permanent_address')

