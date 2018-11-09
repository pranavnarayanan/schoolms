import re
import datetime
from django import forms
from apps.login.models import EN_LoginCredentials
from apps.sign_up.helper.choice_helper import Choice
from apps.users.models import EN_Contacts
from apps.utilities.entities.zipcode import EN_Zipcode

'''
    # Basic Details Form
'''
class FORM_UserBasicsDetails(forms.Form):
    name          = forms.CharField(min_length=3,max_length=30,required=False)
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(format="%Y-%m-%d",attrs={'type': 'date'}),required=False)
    gender        = forms.ChoiceField(choices = Choice.genderAsChoice(),required=False)

    def clean(self):
        data = self.cleaned_data
        name = data["name"]
        gender = data["gender"]
        dob = data["date_of_birth"]

        if name == "" or name.strip() == None:
            self.add_error("name", "Name is required")
        elif not re.match("^[a-zA-Z ]*$", name):
            self.add_error("name","Numbers or special char's found in name")
        if dob == None:
            self.add_error("date_of_birth", "Date Of Birth is required")
        if gender == None:
            self.add_error("gender", "Gender is required")

        if dob != None:
            today = datetime.datetime.now().date()
            yearDiff = ((today - dob).days/365)
            if yearDiff < 5: # Should be more than 5 years old
                self.add_error("date_of_birth", "User must be minimum 5 years old")
        return data


'''
    # Address Details Form
'''
class FORM_AddressDetails(forms.Form):

    def __init__(self, *args, **kwargs):
        super(FORM_AddressDetails, self).__init__(*args, **kwargs)
        try:
            if len(self.data) > 0:
                self.fields['area'].choices = Choice.getZipcodeAreas(self.data["zipcode"])
        except Exception as e:
            print(" --- ERROR : "+e.__str__())

    house_name         = forms.CharField(min_length=2,max_length=100,required=False)
    street             = forms.CharField(min_length=2,max_length=100,required=False)
    landmark           = forms.CharField(max_length=100,required=False)
    zipcode            = forms.CharField(min_length=4,max_length=6,required=False)
    area               = forms.ChoiceField(choices=[],required=False)
    is_current_address = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data
        house_name = data["house_name"]
        street = data["street"]
        zipcode = data["zipcode"]

        if house_name == "" or house_name == None:
            self.add_error("house_name", "House Name is mandatory")
        if street == "" or street == None:
            self.add_error("street", "Street is mandatory")
        if zipcode == "" or zipcode == None:
            self.add_error("zipcode", "Zipcode is mandatory")
        else:
            if not EN_Zipcode.objects.filter(pincode=zipcode).exists():
                self.add_error("zipcode", "Invalid zipcode entered")
            else:
                try:
                    area = data["area"]
                    if area == None or area == "":
                        self.add_error("area", "Area is mandatory")
                    elif not EN_Zipcode.objects.filter(id=area).exists():
                        self.add_error("area", "Invalid area selected")
                except:
                    pass
        return data


'''
    # Contact Details Form
'''
class FORM_ContactDetails(forms.Form):
    mobile_country_code = forms.ChoiceField(choices = Choice.countryMobileCodes(),required=False)
    mobile_number       = forms.CharField(min_length=10,max_length=10,required=False)
    secondary_number    = forms.CharField(min_length=6,max_length=12,required=False)
    is_landline_number  = forms.BooleanField(required=False)
    email_id            = forms.CharField(min_length=6,max_length=60,required=False)
    website             = forms.CharField(min_length=6,max_length=60,required=False)
    publish_your_site   = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data
        mobileCountryCode = data["mobile_country_code"]
        mobileNumber      = data["mobile_number"]
        emailId           = data["email_id"]
        if mobileCountryCode == "" or mobileCountryCode == None:
            self.add_error("mobile_country_code", "Country code is mandatory")
        if mobileNumber == "" or mobileNumber == None:
            self.add_error("mobile_number", "Mobile Number is mandatory")
        if emailId == "" or emailId == None:
            self.add_error("email_id", "Email Id is mandatory")
        elif EN_Contacts.objects.filter(email_id=emailId).exists():
            self.add_error("email_id", "Email Id already exists")
        return data


'''
    # Credentials Form
'''
class FORM_CredentialDetails(forms.Form):
    username                  = forms.CharField(min_length=5,max_length=15,required=False)
    password                  = forms.CharField(min_length=5,max_length=15,required=False)
    subscribe_for_news_letter = forms.BooleanField(required=False)

    def clean(self):
        data = self.cleaned_data
        uName = data["username"]
        pWord = data["password"]
        if EN_LoginCredentials.objects.filter(username=uName).exists():
            self.add_error("username", "Username already exists")
        elif uName == "" or uName == None:
            self.add_error("username", "Username cannot be null")
        if pWord == "" or pWord == None:
            self.add_error("password", "Password cannot be null")
        return data