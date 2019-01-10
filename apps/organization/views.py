import datetime
import json
from math import ceil
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.notifications.helper import NotificationHelper
from apps.organization.forms import *
from apps.organization.models import *
from apps.roles.models import EN_UserRoles, TL_Roles
from apps.users.models import EN_Users
from apps.utilities.entities.account_status import TL_AccountStatus
from apps.utilities.entities.country import EN_Country
from apps.utilities.entities.sequenceutil import EN_SequenceUtil
from apps.utilities.entities.zipcode import EN_Zipcode
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.notification_properties import NotificationTypes
from properties.session_properties import SessionProperties

'''
    # List out all Organization Groups available in the system
    # Method : GET / POST
'''
def index(request):
    data = UIDataHelper(request).getData(page="is_organizations_home")
    template = loader.get_template("org_statics.html")
    return HttpResponse(template.render(data, request))

'''
    # Renders the Org Grp Page
    # Method : POST
'''
def organizationGroupPage(request):
    data = UIDataHelper(request).getData(page="is_list_all_organization_groups_active")
    template = loader.get_template("org_list_all_org_groups.html")
    return HttpResponse(template.render(data, request))

'''
    # List out all Organization Groups available in the system
    # Method : AJAX : POST
'''
@csrf_exempt
def getOrganizationGroups(request):
    if request.is_ajax():
        page = int(request.POST.get('page'))
        page = 1 if page < 1 else page
        pageRowCount = int(request.POST.get('page_row_count'))
        search_keyword = request.POST.get('search_keyword')
        startingIndex = (page-1)*pageRowCount
        endingIndex = page*pageRowCount
        records = EN_OrganizationGroup.objects
        if search_keyword != None:
            records = records.filter(Q(product_id__contains=search_keyword)| Q(group_name__contains=search_keyword))
        total_records_count = records.all().count()
        records = records.all()[startingIndex:endingIndex]
        retList = []
        for record in records:
            returnDict = {
                "product_id":record.product_id,
                "name":record.group_name,
                "logo":record.logo,
                "website":record.website,
                "publish_site":record.publish_your_site,
                "status":record.account_status.code,
            }
            retList.append(returnDict)

        ret = {
            "total_pages" : ceil(total_records_count / pageRowCount),
            "total_records" : total_records_count,
            "data" : retList
        }

        jsonResponse = json.dumps(ret)
        return HttpResponse(jsonResponse)
    else:
        return HttpResponseRedirect("../Redirects/ErrorPage?page=403")

'''
    # Calls out all Organizations Registered on the site
    # Method : GET / POST
'''
def listOrganizations(request):
    data = UIDataHelper(request).getData(page="is_list_all_organization_active")
    template = loader.get_template("org_list_all_organinzations.html")
    return HttpResponse(template.render(data, request))

'''
    # Calls the Organization Group Registration Page
    # Method : GET / POST
'''
def registerOrgGroup(request):
    data = UIDataHelper(request).getData(page="is_new_organization_group_active")
    data.__setitem__("form", FORM_NewOrganizationGroup(request.POST) if request.method == "POST" else FORM_NewOrganizationGroup())
    template = loader.get_template("org_group_registration.html")
    return HttpResponse(template.render(data, request))

'''
    # Calls the Organization Group Registration Page
    # Method : POST
'''
def saveGroupDetails(request):
    if request.method == 'POST':
        form_data = FORM_NewOrganizationGroup(request.POST)
        if form_data.is_valid():
            orgGrp = EN_OrganizationGroup()
            formData = form_data.cleaned_data
            orgGrp.group_name        = formData.get("groupname")
            orgGrp.website           = formData.get("website")
            orgGrp.publish_your_site = formData.get("createpage")
            orgGrp.product_id        = EN_SequenceUtil.genProductIdForOrganizationGroup()
            orgGrp.account_status    = TL_AccountStatus.objects.get(code="active")
            try:
                orgGrp.save()

                # --Roles---------------
                inst_super_user = EN_Users.objects.get(product_id=formData.get("organization_su_prd_id"))
                userRole = EN_UserRoles()
                userRole.user = inst_super_user
                userRole.role = TL_Roles.objects.get(code=Roles.INSTITUTION_SUPER_USER)
                userRole.approved = True
                userRole.request_raised_by_id = 1
                userRole.request_raised_on = datetime.datetime.now()
                userRole.related_organization_group = orgGrp
                userRole.related_organization = None
                userRole.related_user = None
                userRole.request_approved_by_id = 1
                userRole.request_approved_on = datetime.datetime.now()
                try:
                    userRole.save()
                except Exception as e:
                    orgGrp.delete()
                    messages.error(request, "Failed to assign role : {}".format(e.__context__))
                    return HttpResponseRedirect("../Organization/RegisterOrganization")

                try:
                    NotificationHelper.notify(recipient_id=inst_super_user.id,type=NotificationTypes.NEW_ROLE_ADDED)
                except Exception as e:
                    orgGrp.delete()
                    userRole.delete()
                    messages.error(request, "Failed to create activity : {}".format(e.__context__))
                    return HttpResponseRedirect("../Organization/RegisterOrganization")
                # ---------------------


                messages.success(request, DisplayKey.get("org_group_created_successfully"))
                messages.info(request, "WoKidz ID For Organization {} is {}".format(orgGrp.group_name,orgGrp.product_id))
                return HttpResponseRedirect("../Organization/OrganizationGroups")
            except Exception as e:
                messages.warning(request, e.__context__)
                return registerOrgGroup(request)
        else:
            return registerOrgGroup(request)
    else:
        return HttpResponseRedirect("..Redirects/ErrorPage?page=403")

'''
    # Calls the Organization Registration Page
    # Method : GET /POST
'''
def registerOrganization(request):
    data = UIDataHelper(request).getData(page="is_new_organization_active")
    data.__setitem__("form", FORM_NewOrganization(request.POST) if request.method == "POST" else FORM_NewOrganization())
    template = loader.get_template("org_registration.html")
    return HttpResponse(template.render(data, request))

'''
    # Validates the Organization Details Request and Save it
    # Method : POST
'''
def saveOrganizationDetails(request):
    if request.method == 'POST':
        form_data = FORM_NewOrganization(request.POST)
        if form_data.is_valid():
            orgDetails = EN_Organization()
            formData = form_data.cleaned_data
            orgDetails.organization_group  = EN_OrganizationGroup.objects.get(product_id=formData.get("org_group_product_id"))
            orgDetails.affiliation         = TL_Affiliation.objects.get(code=formData.get("affiliation"))
            orgDetails.organization_type   = TL_InstitutionType.objects.get(code=formData.get("institution_type"))
            orgDetails.product_id          = EN_SequenceUtil.genProductIdForOrganization()
            orgDetails.school_name         = formData.get("school_name")
            orgDetails.started_date        = formData.get("org_start_date")
            orgDetails.mobile_country_code = EN_Country.objects.get(id=formData.get("mobile_country_code"))
            orgDetails.mobile_number_1     = formData.get("mobile_number_1")
            orgDetails.mobile_number_2     = formData.get("mobile_number_2")
            orgDetails.landline_number_1   = formData.get("landline_1")
            orgDetails.landline_number_2   = formData.get("landline_2")
            orgDetails.email_id            = formData.get("email_id")
            orgDetails.website             = formData.get("website")
            orgDetails.publish_your_site   = formData.get("createpage")
            orgDetails.account_status      = TL_AccountStatus.objects.get(code="inactive")
            orgDetails.zipcode             = EN_Zipcode.objects.get(id=int(request.POST.get("area")))
            orgDetails.street              = formData.get("street")
            orgDetails.registration_id     = formData.get("school_registration_id")
            try:
                orgDetails.save()
            except Exception as e:
                messages.error(request,"Failed To Save Organization : {}".format(e.__context__))
                return HttpResponseRedirect("../Organization/RegisterOrganization")

            messages.success(request, DisplayKey.get("organization_registration_success"))
            messages.info(request, "WoKidz ID For Organization {} is {}".format(orgDetails.school_name,orgDetails.product_id))
            return HttpResponseRedirect("../Organization/Organizations")
        else:
            return registerOrganization(request)
    else:
        HttpResponseRedirect("RegisterOrganization?message=direct_access_denied")


'''
    # AJAX : Gets all organizations 
    # Method : AJAX POST
'''
@csrf_exempt
def getOrganizations(request):
    if request.is_ajax():
        page = int(request.POST.get('page'))
        page = 1 if page < 1 else page
        pageRowCount = int(request.POST.get('page_row_count'))
        search_keyword = request.POST.get('search_keyword')
        startingIndex = (page-1)*pageRowCount
        endingIndex = page*pageRowCount
        records = EN_Organization.objects
        if search_keyword != None:
            records = records.filter(Q(product_id__contains=search_keyword)| Q(school_name__contains=search_keyword))
        total_records_count = records.all().count()
        records = records.all()[startingIndex:endingIndex]
        retList = []
        for record in records:
            returnDict = {
                "product_id":record.product_id,
                "name":record.school_name,
                "group":record.organization_group.group_name,
                "logo":record.display_picture,
                "website":record.website,
                "publish_site":record.publish_your_site,
                "status":record.account_status.code,
            }
            retList.append(returnDict)

        ret = {
            "total_pages" : ceil(total_records_count / pageRowCount),
            "total_records" : total_records_count,
            "data" : retList
        }

        jsonResponse = json.dumps(ret)
        return HttpResponse(jsonResponse)
    else:
        return HttpResponseRedirect("../Redirects/ErrorPage?page=403")



'''
    Loads organization based on product id
'''
def getOrganization(request):
    if "pid" in request.GET:
        user_product_id = request.GET["pid"].strip()
        try:
            organization = EN_Organization.objects.get(product_id=user_product_id)
        except:
            messages.error(request, DisplayKey.get("invalid_product_id"))
            return index(request)
    else:
        messages.error(request, DisplayKey.get("no_get_atribute_specified"))
        return index(request)

    return HttpResponse("Show Individual Org Details")


'''
    Loads organization group based on product id
'''
def getOrganizationGroup(request):
    if "pid" in request.GET:
        user_product_id = request.GET["pid"].strip()
        try:
            organization_group = EN_OrganizationGroup.objects.get(product_id=user_product_id)
        except:
            messages.error(request, DisplayKey.get("invalid_product_id"))
            return index(request)
    else:
        messages.error(request, DisplayKey.get("no_get_atribute_specified"))
        return index(request)

    return HttpResponse("Show Individual Org Group Details")

'''
    Loads area list from zipcode entered
'''
@csrf_exempt
def ajaxLoadAreaFromZipcode(request):
    pincode = request.POST.get("pincode","0")
    retList = []
    for area in EN_Zipcode.objects.filter(pincode=pincode):
        retDict = {
            "id":area.id,
            "city":area.city,
            "district":area.district,
        }
        retList.append(retDict)
    return HttpResponse(json.dumps(retList))

