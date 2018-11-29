from django.db import models
from apps.users.models import TL_Gender
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.zipcode import EN_Zipcode

class EN_UserRegistration(models.Model):
    session_token        = models.CharField(max_length=100, null=False, unique=True)

    mobile_country_code  = models.ForeignKey(EN_Country, null=True, on_delete=models.CASCADE)
    mobile_number        = models.CharField(max_length=10, null=True)
    secondary_number     = models.CharField(max_length=15, null=True)
    is_landline_number   = models.BooleanField(default=True)
    email_id             = models.EmailField(null=True, unique=True)
    website              = models.CharField(max_length=100, null=True)
    publish_your_site    = models.BooleanField(default=False)

    name                 = models.CharField(max_length=100, null=True)
    date_of_birth        = models.DateField(null=True)
    gender               = models.ForeignKey(TL_Gender, null=True, on_delete=models.CASCADE)
    display_picture      = models.CharField(max_length=100, null=True)

    permanent_house_name = models.CharField(max_length=100, null=True)
    permanent_street     = models.CharField(max_length=100, null=True)
    permanent_landmark   = models.CharField(max_length=100, null=True)
    permanent_zipcode    = models.CharField(max_length=7, null=True)
    permanent_area       = models.ForeignKey(EN_Zipcode, on_delete=models.CASCADE, null=True,related_name='permanent_area')
    is_current_address   = models.BooleanField(default=False)

    current_house_name   = models.CharField(max_length=100, null=True)
    current_street       = models.CharField(max_length=100, null=True)
    current_landmark     = models.CharField(max_length=100, null=True)
    current_zipcode      = models.CharField(max_length=7, null=True)
    current_area         = models.ForeignKey(EN_Zipcode, on_delete=models.CASCADE, null=True,related_name='current_area')

    username             = models.CharField(max_length=25, unique=False, null=True)
    password             = models.CharField(max_length=25, null=True)
    subscribe_for_news_letter = models.BooleanField(default=True)

    class Meta:
        db_table = "en_user_registration"