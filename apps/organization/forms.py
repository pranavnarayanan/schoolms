from django import forms
from apps.organization.helper.choice_helper import Choice
from apps.organization.models import TL_Affiliation, TL_InstitutionType, EN_OrganizationGroup
from apps.users.models import EN_Users
from apps.utilities.entities.zipcode import EN_Zipcode

'''
# Organization Group
'''
class FORM_NewOrganizationGroup(forms.Form):
    groupname  = forms.CharField( min_length=1 )
    website    = forms.CharField( min_length=1 )
    createpage = forms.BooleanField(required=False )

    def clean(self):
        data = self.cleaned_data
        if data["groupname"] == None:
            self.add_error("groupname", "Group Name is required")
        if data["website"] == None:
            self.add_error("Website", "Website is required")
        return data


'''
# Organization
'''
class FORM_NewOrganization(forms.Form):
    org_group_product_id    = forms.CharField(required=True)
    school_name             = forms.CharField(required=True)
    organization_su_prd_id  = forms.CharField(min_length=10,max_length=12,required=True)
    org_start_date          = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),required=True)
    affiliation             = forms.ChoiceField(choices = Choice.AffiliationAsChoice(), required = True)
    institution_type        = forms.ChoiceField(choices = Choice.InstitutionTypeAsChoice(),required = True)
    mobile_country_code     = forms.ChoiceField(choices = Choice.countryMobileCodes(),required = True)
    mobile_number_1         = forms.CharField(min_length=10,max_length=10,required=True)
    mobile_number_2         = forms.CharField(min_length=10,max_length=10,required=False)
    landline_1              = forms.CharField(min_length=7,required=True)
    landline_2              = forms.CharField(min_length=7,required=False)
    email_id                = forms.CharField(required=True)
    website                 = forms.CharField(min_length=8)
    zipcode                 = forms.CharField(required=True,min_length=6,max_length=6)
    createpage              = forms.BooleanField(required=False)
    school_registration_id  = forms.CharField(required=True)
    street                  = forms.CharField(required=True)

    def clean(self):
        data = self.cleaned_data
        if not EN_OrganizationGroup.objects.filter(product_id=data["org_group_product_id"]):
            self.add_error("org_group_product_id", "Ïnvalid Myshisya ID entered for Organization Group")
        if not EN_Zipcode.objects.filter(pincode=data["zipcode"]):
            self.add_error("zipcode", "Invalid Zip Code Entered")
        if data["school_name"] == None:
            self.add_error("school_name", "School Name is mandatory")
        if data["org_start_date"] == None:
            self.add_error("org_start_date", "Organization Start Date is mandatory")
        if data["mobile_country_code"] == None:
            self.add_error("mobile_country_code", "Mobile Country Code is mandatory")
        if data["mobile_number_1"] == None:
            self.add_error("mobile_number_1", "Mobile Number-1 is mandatory")
        if data["landline_1"] == None:
            self.add_error("landline_1", "Landline - 1 is mandatory")
        if data["email_id"] == None:
            self.add_error("email_id", "Email Id is mandatory")
        if data["school_registration_id"] == None:
            self.add_error("school_registration_id", "School Registration Id is mandatory")
        if data["street"] == None:
            self.add_error("street", "Street is mandatory")
        if not TL_Affiliation.objects.filter(code=data["affiliation"]).exists():
            self.add_error("affiliation", "Invalid Affiliation")
        if not TL_InstitutionType.objects.filter(code=data["institution_type"]).exists():
            self.add_error("institution_type", "Invalid Institution Type")
        if not EN_Users.objects.filter(product_id=data["organization_su_prd_id"]).exists():
            self.add_error("organization_su_prd_id", "Invalid Super User ID")
        return data