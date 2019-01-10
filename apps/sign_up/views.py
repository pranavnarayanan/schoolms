from uuid import uuid4
from apps.notifications.helper import NotificationHelper
from apps.sign_up.forms import *
from django.template import loader
from django.contrib import messages
from apps.users.models import TL_Gender, EN_Users
from apps.utilities.entities.account_status import TL_AccountStatus
from displaykey.display_key import DisplayKey
from apps.sign_up.helper.constants import Constants
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.zipcode import EN_Zipcode
from apps.sign_up.helper.data_commit import SaveRecord
from django.http import HttpResponse, HttpResponseRedirect
from apps.sign_up.helper.session_helper import UserRegistrationSessions
from properties.email_templates import EmailTemplates
from properties.notification_properties import NotificationTypes
from utils.email_util import Email

''''
    Function  : Loads the primary page
    Method    : GET
'''
def index(request):
    template = loader.get_template('userreg_basics_page.html')
    data = {
        "form": UserRegistrationSessions(request).loadFormData(Constants.BasicsPage)
    }
    return HttpResponse(template.render(data, request))


''''
    Function  : Saves the primary page  data
    Method    : POST
'''
def savePrimaryPageDetails(request):
    if(request.method == "POST"):
        form_data = FORM_UserBasicsDetails(request.POST)
        if (request.POST["basic_submit_button"] == "next"):
            if (form_data.is_valid()):
                try:
                    ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
                    ur.name = form_data.cleaned_data.get("name")
                    ur.date_of_birth = form_data.cleaned_data.get("date_of_birth")
                    ur.gender = TL_Gender.objects.get(code=form_data.cleaned_data.get("gender"))
                    ur.save()
                    return HttpResponseRedirect("LoadContactPage")
                except Exception as e:
                    messages.error(request,e.__str__())
                    return index(request)
            else:
                return index(request)
        else:
            return HttpResponseRedirect("../Login")
    else:
        return HttpResponseRedirect("../SignUp")


''''
    Function  : Loads the Contact Page
    Method    : GET
'''
def loadContactPage(request):
    template = loader.get_template('userreg_contact_page.html')
    data = {
        "form": UserRegistrationSessions(request).loadFormData(Constants.ContactPage)
    }
    return HttpResponse(template.render(data, request))


''''
    Function  : Loads the Contact Page Details
    Method    : POST
'''
def saveContactPageDetails(request):
    if(request.method == "POST"):
        form_data = FORM_ContactDetails(request.POST)
        if(request.POST["contact_submit_button"] == "next"):
            if (form_data.is_valid()):
                try:
                    ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
                    ur.mobile_country_code = EN_Country.objects.get(id=form_data.cleaned_data.get("mobile_country_code"))
                    ur.mobile_number = form_data.cleaned_data.get("mobile_number")
                    ur.secondary_number = form_data.cleaned_data.get("secondary_number")
                    ur.is_landline_number = form_data.cleaned_data.get("is_landline_number")
                    ur.email_id = form_data.cleaned_data.get("email_id")
                    ur.website = form_data.cleaned_data.get("website")
                    ur.publish_your_site = form_data.cleaned_data.get("publish_your_site")
                    ur.save()
                    return HttpResponseRedirect("LoadPermanentAddressPage")
                except Exception as e:
                    messages.error(request,e.__str__())
                    return loadContactPage(request)
            else:
                return loadContactPage(request)
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            request.method = "GET"
            return index(request)
    else:
        return HttpResponseRedirect("LoadContactPage")


''''
    Function  : Loads the Permanent Address Page
    Method    : GET
'''
def loadPermanentAddressPage(request):
    template = loader.get_template('userreg_permanent_address_page.html')
    data = {
        "form": UserRegistrationSessions(request).loadFormData(Constants.PermanentAddressPage)
    }
    return HttpResponse(template.render(data, request))


''''
    Function  : Loads the Permanent Page Details
    Method    : POST
'''
def savePermanentAddressPageDetails(request):
    if (request.method == "POST"):
        form_data = FORM_AddressDetails(request.POST)
        if (request.POST["permanent_address_submit_button"] == "next"):
            if (form_data.is_valid()):
                try:
                    ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
                    ur.permanent_house_name= form_data.cleaned_data.get("house_name")
                    ur.permanent_street = form_data.cleaned_data.get("street")
                    ur.permanent_landmark = form_data.cleaned_data.get("landmark")
                    ur.permanent_zipcode = form_data.cleaned_data.get("zipcode")
                    ur.permanent_area_id = int(form_data.cleaned_data.get("area"))
                    ur.is_current_address = form_data.cleaned_data.get("is_current_address")
                    if ur.is_current_address:
                        ur.current_house_name = None
                        ur.current_street = None
                        ur.current_landmark = None
                        ur.current_zipcode = None
                    ur.save()
                    return HttpResponseRedirect("LoadCredentialsPage" if ur.is_current_address else "LoadCurrentAddressPage")
                except Exception as e:
                    messages.error(request, e.__str__())
                    return loadPermanentAddressPage(request)
            else:
                return loadPermanentAddressPage(request)
        if (request.POST["permanent_address_submit_button"] == "zipcode"):
            ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
            zipcode = request.POST.get("zipcode")
            areaList = EN_Zipcode.objects.filter(pincode = zipcode)
            if(areaList.exists()):
                ur.permanent_house_name = request.POST.get("house_name")
                ur.permanent_street = request.POST.get("street")
                ur.permanent_landmark = request.POST.get("landmark")
                ur.permanent_zipcode = zipcode
                ur.permanent_area = areaList.first()
                ur.save()
            else:
                messages.warning(request,"Invalid Zipcode")
            return HttpResponseRedirect("LoadPermanentAddressPage")
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            request.method = "GET"
            return loadContactPage(request)
    else:
        return HttpResponseRedirect("LoadPermanentAddressPage")


''''
    Function  : Loads the Current Address Page
    Method    : GET
'''
def loadCurrentAddressPage(request):
    template = loader.get_template('userreg_current_address_page.html')
    data = {
        "form": UserRegistrationSessions(request).loadFormData(Constants.CurrentAddressPage)
    }
    return HttpResponse(template.render(data, request))


''''
    Function  : Saves Current Page Details
    Method    : POST
'''
def saveCurrentAddressPageDetails(request):
    if (request.method == "POST"):
        form_data = FORM_AddressDetails(request.POST)
        if (request.POST["current_address_submit_button"] == "next"):
            if (form_data.is_valid()):
                try:
                    ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
                    ur.current_house_name= form_data.cleaned_data.get("house_name")
                    ur.current_street = form_data.cleaned_data.get("street")
                    ur.current_landmark = form_data.cleaned_data.get("landmark")
                    ur.current_zipcode = form_data.cleaned_data.get("zipcode")
                    ur.current_area_id = int(form_data.cleaned_data.get("area"))
                    ur.save()
                    return HttpResponseRedirect("LoadCredentialsPage")
                except Exception as e:
                    messages.error(request, e.__str__())
                    return loadCurrentAddressPage(request)
            else:
                return loadCurrentAddressPage(request)
        if (request.POST["current_address_submit_button"] == "zipcode"):
            ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
            zipcode = request.POST.get("zipcode")
            areaList = EN_Zipcode.objects.filter(pincode = zipcode)
            if(areaList.exists()):
                ur.current_house_name = request.POST.get("house_name")
                ur.current_street = request.POST.get("street")
                ur.current_landmark = request.POST.get("landmark")
                ur.current_zipcode = zipcode
                ur.current_area = areaList.first()
                ur.save()
            else:
                messages.warning(request,"Invalid Zipcode")
            return HttpResponseRedirect("LoadCurrentAddressPage")
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            request.method = "GET"
            return loadPermanentAddressPage(request)
    else:
        return HttpResponseRedirect("LoadCurrentAddressPage")

''''
    Function  : Loads the Credentials Page
    Method    : GET
'''
def loadCredentialsPage(request):
    template = loader.get_template('userreg_credentials_page.html')
    data = {
        "form": UserRegistrationSessions(request).loadFormData(Constants.CredentialPage)
    }
    return HttpResponse(template.render(data, request))


''''
    Function  : Loads the Credentials Page Details
    Method    : POST
'''
def saveCredentialPageDetails(request):
    if(request.method == "POST"):
        form_data = FORM_CredentialDetails(request.POST)
        if(request.POST["credential_submit_button"] == "next"):
            if (form_data.is_valid()):
                try:
                    ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
                    ur.username = form_data.cleaned_data.get("username")
                    ur.password = form_data.cleaned_data.get("password")
                    ur.subscribe_for_news_letter= form_data.cleaned_data.get("subscribe_for_news_letter")
                    ur.save()

                    try:
                        user = SaveRecord().save(ur)
                        del request.session[Constants.SESSION_TOKEN]
                        ur.delete()
                        messages.success(request, DisplayKey.get("user_successfully_registered"))
                    except Exception as e:
                        messages.error(request,e.__str__())
                        return loadCredentialsPage(request)

                    template_data = {
                        "url": "{}/SignUp/ActivateAccount".format(request.get_host()),
                        "name": user.name,
                        "token": user.activation_token,
                        "product_id": user.product_id,
                    }
                    try:
                        Email().sendEmail(
                            template=EmailTemplates.ACCOUNT_ACTIVATION_EMAIL,
                            subject="Activate Wokidz Account",
                            recipient_list=[user.contact.email_id],
                            template_data=template_data
                        )
                    except Exception as e:
                        messages.error(request,"Registered Successfully but failed to send activation Email. Please contact site admin")

                    NotificationHelper.notify(recipient_id=user.id, type=NotificationTypes.WELCOME_MESSAGE)
                    return HttpResponseRedirect("../Login")
                except Exception as e:
                    messages.error(request,e.__str__())
                    return loadCredentialsPage(request)
            else:
                return loadCredentialsPage(request)
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
            if (form_data.is_valid()):
                ur.username = form_data.cleaned_data.get("username")
                ur.password = form_data.cleaned_data.get("password")
                ur.subscribe_for_news_letter = form_data.cleaned_data.get("subscribe_for_news_letter")
                ur.save()
                request.method = "GET"
                return loadPermanentAddressPage(request) if ur.is_current_address else loadCurrentAddressPage(request)
            else:
                return loadCredentialsPage(request)
    else:
        return HttpResponseRedirect("LoadCredentialsPage")



def activateAccount(request):
    if request.method == "GET":
        token = request.GET.get("token",0)
        product_id = request.GET.get("product_id",0)
        try:
            user = EN_Users.objects.get(activation_token=token,product_id=product_id)
            user.activation_token = uuid4()
            user.account_status = TL_AccountStatus.objects.get(code="active")
            user.save()
            messages.success(request, "Account activated successfuly.")
        except Exception as e:
            messages.warning(request,"Invalid token / product_id")
    else:
        messages.warning(request,"Access denied - Invalid Request Method")
    return HttpResponseRedirect("../Login")
