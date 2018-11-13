from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from apps.organization.models import EN_Organization, EN_OrganizationGroup
from apps.users.models import EN_Users


'''
    Table   : Roles Typelist
    Content : site_admin, school_admin, prinipal, teacher
'''
class TL_Roles(models.Model):
    code        = models.CharField(max_length=30, unique=True,  null=False)
    name        = models.CharField(max_length=30, unique=False, null=False)
    description = models.TextField(null=True)
    class Meta:
        db_table = "tl_roles"



'''
    Table   : User Roles
    Content : site_admin, school_admin, prinipal, teacher
'''
class EN_UserRoles(models.Model):
    user = models.ForeignKey(EN_Users, null=False, on_delete=models.PROTECT)
    role = models.ForeignKey(TL_Roles, null=False, on_delete=models.PROTECT)
    related_organization = models.ForeignKey(EN_Organization, default=None, null=True, on_delete=models.CASCADE)
    related_organization_group = models.ForeignKey(EN_OrganizationGroup, default=None, null=True,on_delete=models.CASCADE)
    related_user = models.ForeignKey(EN_Users, default=None, null=True, on_delete=models.CASCADE,related_name='related_user')
    approved  = models.BooleanField(default=False)
    request_raised_by = models.ForeignKey(EN_Users, null=False, on_delete=models.DO_NOTHING,related_name='request_raised_by')
    request_approved_by = models.ForeignKey(EN_Users, null=True, on_delete=models.DO_NOTHING,related_name='request_approved_by')
    request_approved_on = models.DateTimeField(null=True,default=None)
    request_raised_on = models.DateTimeField(default=timezone.now)
    is_selected_role  = models.BooleanField(default=False)

    class Meta:
        db_table = "en_user_roles"
        unique_together = ('user', 'role', 'related_organization', 'related_organization_group','related_user')

    def validate_unique(self, exclude=None):
        this = EN_UserRoles.objects.exclude(id=self.id).filter(user=self.user, role=self.role)
        if self.related_organization_group != None:
            if this.filter(related_organization_group=self.related_organization_group,related_organization__isnull=True,related_user__isnull=True).exists():
                raise ValidationError("Duplicate Entry On Related Organization Group")
        elif self.related_organization != None and self.related_user == None:
            if this.filter(related_organization=self.related_organization,related_organization_group__isnull=True, related_user__isnull=True).exists():
                raise ValidationError("Duplicate Entry On Related Organization")
        elif self.related_organization != None  and self.related_user != None :
            if this.filter(related_organization=self.related_organization,related_user=self.related_user, related_organization_group__isnull=True).exists():
                raise ValidationError("{}, ({}) is already a parent of this student".format(self.user.name,self.user.product_id))
