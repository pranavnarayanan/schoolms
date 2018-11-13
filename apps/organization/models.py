from django.db import models
from apps.utilities.entities.account_status import TL_AccountStatus
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.zipcode import EN_Zipcode

'''
    Table   : Institution Type
    Content : School, Engineering, Medicine, Law, Business, Arts
'''
class TL_InstitutionType(models.Model):
    code = models.CharField(max_length=40, unique=True, null=False)
    name = models.CharField(max_length=40, unique=False, null=False)
    description = models.CharField(max_length=100, unique=False, null=True)
    class Meta:
        db_table = "tl_institution_type"


'''
    Table   : Syllabus
    Content : CBSE, ICES, kerala-state, abdual kalam, cusat, mg
'''
class TL_Affiliation(models.Model):
    code        = models.CharField(max_length=40, unique=True,  null=False)
    name        = models.CharField(max_length=40, unique=False, null=False)
    description = models.TextField(null=True)
    class Meta:
        db_table = "tl_affiliation"



'''
    Table   : Organization Group
'''
class EN_OrganizationGroup(models.Model):
    product_id           = models.CharField(max_length=12, unique=True, null=False)
    group_name           = models.CharField(max_length=100, null=False)
    logo                 = models.CharField(max_length=100, null=True)
    website              = models.CharField(max_length=100, null=True)
    publish_your_site    = models.BooleanField(default=False)
    account_status       = models.ForeignKey(TL_AccountStatus, null=False, on_delete=models.PROTECT)
    class Meta:
        db_table = "en_organization_group"
        unique_together = ('group_name', 'website')


'''
    Table   : Organizations
'''
class EN_Organization(models.Model):
    organization_group   = models.ForeignKey(EN_OrganizationGroup, null=False, on_delete=models.CASCADE)
    product_id           = models.CharField(max_length=12, unique=True, null=False)
    school_name          = models.CharField(max_length=12, null=False)
    started_date         = models.DateField(null=False)
    display_picture      = models.CharField(max_length=100, null=True)
    mobile_country_code  = models.ForeignKey(EN_Country, null=False, on_delete=models.DO_NOTHING)
    mobile_number_1      = models.CharField(max_length=10, null=False)
    mobile_number_2      = models.CharField(max_length=10, null=False)
    landline_number_1    = models.CharField(max_length=13, null=False)
    landline_number_2    = models.CharField(max_length=13, null=True)
    email_id             = models.EmailField(null=True)
    website              = models.CharField(max_length=100, null=True)
    publish_your_site    = models.BooleanField(default=True)
    street               = models.CharField(max_length=100, unique=False, null=True)
    zipcode              = models.ForeignKey(EN_Zipcode, on_delete=models.PROTECT, null=False)
    registration_id      = models.CharField(max_length=100, unique=True, null=True)
    account_status       = models.ForeignKey(TL_AccountStatus, null=False, on_delete=models.PROTECT)
    affiliation          = models.ForeignKey(TL_Affiliation, null=True, on_delete=models.PROTECT)
    organization_type    = models.ForeignKey(TL_InstitutionType, null=True, on_delete=models.PROTECT)
    class Meta:
        db_table = "en_organization"
        unique_together = ('school_name','zipcode','registration_id')