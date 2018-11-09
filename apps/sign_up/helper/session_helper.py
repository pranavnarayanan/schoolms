from apps.sign_up.forms import *
from apps.sign_up.helper.constants import Constants
from apps.sign_up.models import EN_UserRegistration
from apps.utilities.entities.sequenceutil import EN_SequenceUtil

class UserRegistrationSessions():

    def __init__(self,request):
        self.request = request

    '''
    # Set Form data | Reads data from DB and creates form data
    # Key : Session_Token
    '''
    def loadFormData(self, form_type):

        if Constants.SESSION_TOKEN in self.request.session:
            session_token = self.request.session[Constants.SESSION_TOKEN]
            try:
                ur = EN_UserRegistration.objects.get(session_token=session_token)
            except:
                EN_UserRegistration.objects.filter(session_token=session_token).delete()
                ur = EN_UserRegistration()
                ur.session_token = self.request.session[Constants.SESSION_TOKEN]
                ur.save()
        else:
            self.request.session[Constants.SESSION_TOKEN] = EN_SequenceUtil.genTokenForNewUserRegistration()
            ur = EN_UserRegistration()
            ur.session_token = self.request.session[Constants.SESSION_TOKEN]
            ur.save()
            ur = None

        if form_type == Constants.BasicsPage:
            form = FORM_UserBasicsDetails(self.request.POST) if (self.request.method == "POST") else FORM_UserBasicsDetails()
            if(ur != None):
                form.fields["name"].initial = ur.name
                form.fields["date_of_birth"].initial = ur.date_of_birth
                if ur.gender != None:
                    form.fields["gender"].initial = ur.gender.code

        elif form_type == Constants.PermanentAddressPage:
            form = FORM_AddressDetails(self.request.POST) if (self.request.method == "POST") else FORM_AddressDetails()
            if (ur != None):
                form.fields["house_name"].initial = ur.permanent_house_name
                form.fields["street"].initial = ur.permanent_street
                form.fields["landmark"].initial = ur.permanent_landmark
                form.fields["zipcode"].initial = ur.permanent_zipcode
                form.fields["area"].widget.choices = Choice.getZipcodeAreas(ur.permanent_zipcode)
                form.fields["area"].initial = form.fields["area"].widget.choices.first() if ur.permanent_area == None else ur.permanent_area.id
                form.fields["is_current_address"].initial = ur.is_current_address

        elif form_type == Constants.CurrentAddressPage:
            form = FORM_AddressDetails(self.request.POST) if (self.request.method == "POST") else FORM_AddressDetails()
            if (ur != None):
                form.fields["house_name"].initial = ur.current_house_name
                form.fields["street"].initial = ur.current_street
                form.fields["landmark"].initial = ur.current_landmark
                form.fields["zipcode"].initial = ur.current_zipcode
                form.fields["area"] = Choice.getZipcodeAreas(ur.permanent_zipcode)
                form.fields["is_current_address"].initial = True

        elif form_type == Constants.ContactPage:
            form = FORM_ContactDetails(self.request.POST) if (self.request.method == "POST") else FORM_ContactDetails()
            if (ur != None):
                if ur.mobile_country_code != None:
                    form.fields["mobile_country_code"].initial = ur.mobile_country_code.id
                form.fields["mobile_number"].initial = ur.mobile_number
                form.fields["secondary_number"].initial = ur.secondary_number
                form.fields["is_landline_number"].initial = ur.is_landline_number
                form.fields["email_id"].initial = ur.email_id
                form.fields["website"].initial = ur.website
                form.fields["publish_your_site"].initial = ur.publish_your_site

        elif form_type == Constants.CredentialPage:
            form = FORM_CredentialDetails(self.request.POST) if (self.request.method == "POST") else FORM_CredentialDetails()
            if (ur != None):
                form.fields["username"].initial = ur.username
                form.fields["password"].initial = ur.password
                form.fields["subscribe_for_news_letter"].initial = ur.subscribe_for_news_letter
        else:
            raise Exception("Invalid Form Specified")

        return form



    '''
    # Fetch the corresponding table record form DB
    # Key : Session_Token
    '''
    def getCorrespondingDBRecord(self):
        if Constants.SESSION_TOKEN not in self.request.session:
            raise Exception("Record Not Found in DB")
        else:
            session_token = self.request.session[Constants.SESSION_TOKEN]
            try:
                return EN_UserRegistration.objects.get(session_token=session_token)
            except:
                EN_UserRegistration.objects.filter(session_token=session_token).delete()
                raise Exception("No or Multiple Record(s) Found in DB")
