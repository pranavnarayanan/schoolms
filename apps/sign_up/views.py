import json
from apps.sign_up.forms import *
from django.template import loader
from django.contrib import messages
from apps.users.models import TL_Gender
from displaykey.display_key import DisplayKey
from apps.sign_up.helper.constants import Constants
from django.views.decorators.csrf import csrf_exempt
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.zipcode import EN_Zipcode
from apps.sign_up.helper.data_commit import SaveRecord
from django.http import HttpResponse, HttpResponseRedirect
from apps.sign_up.helper.session_helper import UserRegistrationSessions

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
        messages.error(request,DisplayKey.get("error_not_a_post_request"))
        return index(request)


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
        messages.error(request,DisplayKey.get("error_not_a_post_request"))
        return loadContactPage(request)


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
                    ur.permanent_zipcode = EN_Zipcode.objects.get(id=form_data.cleaned_data.get("zipcode"))
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
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            request.method = "GET"
            return loadContactPage(request)
    else:
        messages.error(request, DisplayKey.get("error_not_a_post_request"))
        return loadPermanentAddressPage(request)


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
    if(request.method == "POST"):
        form_data = FORM_AddressDetails(request.POST)
        if(request.POST["current_address_submit_button"] == "next"):
            if (form_data.is_valid()):
                try:
                    ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
                    ur.current_house_name= form_data.cleaned_data.get("house_name")
                    ur.current_street = form_data.cleaned_data.get("street")
                    ur.current_landmark = form_data.cleaned_data.get("landmark")
                    ur.current_zipcode = EN_Zipcode.objects.get(id=form_data.cleaned_data.get("zipcode"))
                    ur.save()
                    return HttpResponseRedirect("LoadCredentialsPage")
                except Exception as e:
                    messages.error(request,e.__str__())
                    return loadCurrentAddressPage(request)
            else:
                return loadCurrentAddressPage(request)
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            request.method = "GET"
            return loadPermanentAddressPage(request)
    else:
        messages.error(request,DisplayKey.get("error_not_a_post_request"))
        return loadCurrentAddressPage(request)




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
                        SaveRecord().save(ur)
                        del request.session[Constants.SESSION_TOKEN]
                        ur.delete()
                        messages.success(request, DisplayKey.get("user_successfully_registered"))
                    except Exception as e:
                        messages.error(request,e.__str__())
                        return loadCredentialsPage(request)

                    #Todo : Do Activity logging here
                    return HttpResponseRedirect("../Login")
                except Exception as e:
                    messages.error(request,e.__str__())
                    return loadCredentialsPage(request)
            else:
                return loadCredentialsPage(request)
        else:
            # Note: Converting method to GET from POST
            # If not changed, in session_helper class, form validation will be trigerred
            request.method = "GET"
            ur = UserRegistrationSessions(request).getCorrespondingDBRecord()
            return loadPermanentAddressPage(request) if ur.is_current_address else loadCurrentAddressPage(request)
    else:
        messages.error(request,DisplayKey.get("error_not_a_post_request"))
        return loadCredentialsPage(request)






''''
    Function  : Ajax function to get all areas associated with a zipcode
    Method    : POST
'''
@csrf_exempt
def ajaxGetAreaFromZipcode(request):
    if request.is_ajax():
        zipcode = request.POST["zipcode"]
        countryID = request.POST["country"]
        rows = EN_Zipcode.objects.values("id","city","district","state").filter(pincode=zipcode, country_id = countryID)
        returnList = []
        for row in rows:
            rowDict = {
                "id"       : row["id"],
                "city"     : row["city"],
                "district" : row["district"],
                "state"    : row["state"]
            }
            returnList.append(rowDict)

        jsonResponse = json.dumps(returnList)
        return HttpResponse(jsonResponse)
    else:
        return HttpResponseRedirect("BasicDetails?message=direct_access_denied")


