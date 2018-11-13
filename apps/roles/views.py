import datetime
import json
import re
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from math import ceil
from apps.organization.models import EN_Organization
from apps.roles.helper.roles_view_helper import RolesViewHelper
from apps.roles.models import EN_UserRoles, TL_Roles
from apps.users.models import EN_Users, EN_AddressBook
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.roles import Roles
from properties.session_properties import SessionProperties
from .forms import FORM_UserRoleAssignment
from .helper.role_approval_hierarchy import RoleApprovalHierarchy
from properties.activity_patterns import ActivityPattern
from apps.activity.helper import ActivityHelper


''''
    Function  : Loads the roles page [lists the active and pending roles ona  user]
    Privelage : ALL
    Method    : ANY
'''
def index(request):
    user_id = request.session[SessionProperties.USER_ID_KEY]
    data = UIDataHelper(request).getData(page="is_roles")
    rh = RolesViewHelper(user_id)
    roles = rh.getRolesToDisplayOnRolesScreen()
    if roles == None:
        messages.error(request, DisplayKey.get("invalid_table_name_on_user_role"))
        return HttpResponseRedirect("/Home/")
    else:
        data.__setitem__("user_roles", roles)
        data.__setitem__("system_roles", rh.getSystemRolesAsList())
        template = loader.get_template("roles_list_all_roles_of_user.html")
        return HttpResponse(template.render(data, request))


''''
    Function  : Loads All approved and requested roles
    Privelage : TEACHER / SCHOOL ADMIN / SUPER USER
    Method    : ANY
'''
def listAllRaisedRoles(request):
    data = UIDataHelper(request).getData(page="is_raised_roles")
    template = loader.get_template("roles_list_all_requested_and_approved_roles.html")
    return HttpResponse(template.render(data, request))



''''
    Function  : Function loads the user role adding page
    Privelage : Institution SU , School Admin , Teachers
    Method    : GET
'''
def loadRoleSettingPage(request):
    data = UIDataHelper(request).getData(page="is_raise_role_request")
    user_id = request.session[SessionProperties.USER_ID_KEY]
    accepted_user_list = [Roles.INSTITUTION_SUPER_USER, Roles.SCHOOL_ADMIN, Roles.TEACHER]
    ur = EN_UserRoles.objects.filter(approved=True, user_id=user_id, role__code__in=accepted_user_list, is_selected_role=True)
    if ur.exists():
        ur = ur[0]
        if ur.role.code == Roles.INSTITUTION_SUPER_USER:
            approvalList = RoleApprovalHierarchy.INSTITUTION_SU_APPROVAL_LIST
        elif ur.role.code == Roles.SCHOOL_ADMIN:
            approvalList = RoleApprovalHierarchy.SCHOOL_ADMIN_APPROVAL_LIST
        elif ur.role.code == Roles.TEACHER:
            approvalList = RoleApprovalHierarchy.TEACHER_APPROVAL_LIST
        else:
            approvalList = []

        roles = [{
            "code": role.code,
            "name": role.name
        } for role in TL_Roles.objects.filter(code__in=approvalList)]
        schools_list = []
        if ur.related_organization_group != None:
            schools_list = [{
                "org_id":org.id,
                "org_name":org.school_name+", "+org.street
            } for org in EN_Organization.objects.filter(organization_group=ur.related_organization_group)]
        elif ur.related_organization != None:
            schools_list = [{
                "org_id": ur.related_organization.id,
                "org_name": ur.related_organization.school_name + ", " + ur.related_organization.street
            }]
        data.__setitem__("roles", roles)
        data.__setitem__("schools_list", schools_list)
        data.__setitem__("form", FORM_UserRoleAssignment(request.POST) if request.method == "POST" else FORM_UserRoleAssignment())
        template = loader.get_template("roles_assign_roles_to_user.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.error(request,DisplayKey.get("current_role_doesnot_have_permission_to_do_this_action"))
        return HttpResponseRedirect("../Home")


''''
    Function  : Function validates and save all assigned roles
    Privelage : Institution SU , School Admin , Teachers
    Method    : POST
'''
def validateAssignedRole(request):
    if request.method == "POST":
        user_id = request.session[SessionProperties.USER_ID_KEY]
        accepted_user_list = [Roles.INSTITUTION_SUPER_USER, Roles.SCHOOL_ADMIN, Roles.TEACHER]
        ur = EN_UserRoles.objects.filter(approved=True, user_id=user_id, role__code__in=accepted_user_list,is_selected_role=True)
        if ur.exists():
            ur = ur[0]
            form_data = FORM_UserRoleAssignment(request.POST)
            try:
                selected_role = TL_Roles.objects.get(code=request.POST["role_selected"])
            except:
                messages.error(request, "Invalid Role Selected")
                return loadRoleSettingPage(request)

            str = form_data["product_ids"].data
            prdIdListString = (str.replace(" ", "")).strip()
            productIdList = list(prdIdListString.split(","))
            users = EN_Users.objects.filter(product_id__in=productIdList)
            retList = []
            prodComparisonList = []
            active_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, role__code__in=accepted_user_list,is_selected_role=True)
            if active_role.exists():
                active_role = active_role.first()
            else:
                messages.error(request, DisplayKey.get("selected_role_lacks_permission_to_send_or_approve_role_request"))
                return loadRoleSettingPage(request)

            students_not_of_this_org = []
            for user in users:
                if selected_role.code == Roles.PARENT:
                    ur = EN_UserRoles.objects.filter(approved=True, related_organization=active_role.related_organization, user=user, role__code=Roles.STUDENT)
                    if not ur.exists():
                        students_not_of_this_org.append(user.product_id)

            if students_not_of_this_org.__len__() > 0:
                messages.error(request,"User(s) {} are not approved students of {}".format(list(students_not_of_this_org).__str__(),active_role.related_organization.school_name))
                return loadRoleSettingPage(request)

            for user in users:
                addr = EN_AddressBook.objects.get(user=user, is_permanent_address=True)
                permanent_adr = addr.house_name + ", " + addr.street
                retDict = {
                    "id": user.id,
                    "name": user.name,
                    "gender": user.gender.code,
                    "contact_no": user.contact.mobile_number,
                    "address": permanent_adr,
                    "dp": user.display_picture,
                    "product_id": user.product_id
                }
                prodComparisonList.append(user.product_id)
                retList.append(retDict)
            diff = set(productIdList) - set(prodComparisonList)
            if diff.__len__() > 0:
                messages.warning(request, "Invalid Myshishya IDs found : {}".format((", ".join(diff))))
                return loadRoleSettingPage(request)

            data = UIDataHelper(request).getData(page="is_raise_role_request")
            data.__setitem__("organization_id", 0 if "organization_id" not in request.POST else request.POST["organization_id"])
            data.__setitem__("selected_role", selected_role.code)
            try:
                data.__setitem__("my_role", ur.role.code)
            except:
                data.__setitem__("my_role", ur[0].role.code)
            data.__setitem__("user_list", retList)

            template = "roles_parent_role_page.html" if selected_role.code == Roles.PARENT else "roles_user_list_page.html"
            template = loader.get_template("templates/" + template)
            return HttpResponse(template.render(data, request))
        else:
            return loadRoleSettingPage(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")

''''
    Function  : Saves the assigned role
    Privelage : Institution SU , School Admin , Teachers
    Method    : AJAX - POST
'''
@csrf_exempt
def saveAssignedRole(request):
    if request.is_ajax():
        if request.method == "POST":
            retDict = {
                "status": False,
                "message": None
            }
            ids = request.POST["ids"]
            selected_role = TL_Roles.objects.get(code=request.POST["selected_role"])
            user_id = request.session[SessionProperties.USER_ID_KEY]
            accepted_user_list = [Roles.INSTITUTION_SUPER_USER, Roles.SCHOOL_ADMIN, Roles.TEACHER]
            active_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, role__code__in=accepted_user_list,is_selected_role=True)
            if active_role.exists():
                active_role = active_role.first()
                approved = (active_role.role.code in [Roles.INSTITUTION_SUPER_USER, Roles.SCHOOL_ADMIN])
                idList = [int(s) for s in (ids.strip()).split(',')]
                activity = ActivityHelper(user_id)
                for user in EN_Users.objects.filter(id__in=idList):
                    userRole = EN_UserRoles()
                    userRole.user = user
                    userRole.role = selected_role
                    userRole.approved = approved
                    userRole.request_raised_by_id = user_id
                    userRole.request_raised_on = datetime.datetime.now()
                    if ((selected_role.code in [Roles.INSTITUTION_SUPER_USER, Roles.DIRECTOR, Roles.BOARD_MEMBER]) and (active_role.role.code in [Roles.INSTITUTION_SUPER_USER])):
                        userRole.related_organization_group = active_role.related_organization_group
                        userRole.request_approved_by_id = user_id
                        userRole.request_approved_on = datetime.datetime.now()
                        try:
                            userRole.validate_unique()
                            userRole.save()
                            activity.createActivity(ActivityPattern.ROLE_REQUEST_APPROVED, user, userRole, True)
                            retDict["status"] = True
                        except Exception as e:
                            retDict["message"] = e.__str__()

                    #---- SCHOOL ADMIN----------------------
                    elif ((selected_role.code in [Roles.SCHOOL_ADMIN]) and (active_role.role.code in [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN])):
                        selected_organization = EN_Organization.objects.filter(id=int(request.POST["organization_id"]))
                        if selected_organization.exists():
                            selected_organization = selected_organization.first()
                            if active_role.related_organization_group.id == selected_organization.organization_group.id:
                                userRole.related_organization = selected_organization
                                userRole.request_approved_by_id = user_id
                                userRole.request_approved_on = datetime.datetime.now()
                                userRole.validate_unique()
                                try:
                                    userRole.save()
                                    activity.createActivity(ActivityPattern.ROLE_REQUEST_APPROVED, user, userRole, True)
                                    retDict["status"] = True
                                except Exception as e:
                                    retDict["message"] = e.__str__()
                            else:
                                retDict["message"] = DisplayKey.get("current_role_have_no_privilage_on_selected_organization")
                        else:
                            retDict["message"] = DisplayKey.get("invalid_organization_id")

                    # ---- ALL SCHOOL LEVEL ROLES FROM SCHOOL ADMIN ----------------------
                    elif ((selected_role.code in [Roles.PRINCIPAL, Roles.TEACHER, Roles.STUDENT, Roles.PARENT, Roles.LIBRARIAN, Roles.ACCOUNTANT, Roles.LAB_ASSISTANT,Roles.ENQUIRY_ASSISTANT, Roles.SECURITY]) and (active_role.role.code in [Roles.SCHOOL_ADMIN])):
                        if selected_role.code == Roles.PARENT:
                            selected_student = EN_Users.objects.filter(id=int(request.POST["student_id"]))
                            if selected_student.exists():
                                selected_student_role = EN_UserRoles.objects.filter(approved=True,related_organization=active_role.related_organization,role__code=Roles.STUDENT)
                                if selected_student_role.exists():
                                    userRole.related_user = selected_student.first()
                        userRole.related_organization = active_role.related_organization
                        userRole.request_approved_by_id = user_id
                        userRole.request_approved_on = datetime.datetime.now()
                        try:
                            userRole.validate_unique()
                            userRole.save()
                            activity.createActivity(ActivityPattern.ROLE_REQUEST_APPROVED, user, userRole, True)
                            retDict["status"] = True
                        except Exception as e:
                            retDict["message"] = e.__str__()


                    # ---- STUDENT REQUEST FROM TEACHER----------------------
                    elif ((selected_role.code in [Roles.STUDENT]) and (active_role.role.code in [Roles.TEACHER])):
                        userRole.related_organization = active_role.related_organization
                        try:
                            userRole.validate_unique()
                            userRole.save()
                            approvers = EN_UserRoles.objects.filter(approved=True,related_organization=active_role.related_organization,role__code=Roles.SCHOOL_ADMIN)
                            if approvers.exists():
                                for approver in approvers:
                                    activity.createActivity(ActivityPattern.RECEIVED_ROLE_REQUEST, approver.user, userRole,False)
                                retDict["status"] = True
                            else:
                                userRole.delete()
                                retDict["message"] = DisplayKey.get("no_approvers_found_for_this_organization")
                        except Exception as e:
                            retDict["message"] = e.__str__()
                    elif ((selected_role.code in [Roles.PARENT]) and (active_role.role.code in [Roles.TEACHER])):
                        selected_student = EN_Users.objects.filter(id=int(request.POST["student_id"]))
                        if selected_student.exists():
                            selected_student_role = EN_UserRoles.objects.filter(approved=True,related_organization=active_role.related_organization,role__code=Roles.STUDENT)
                            if selected_student_role.exists():
                                userRole.related_organization = active_role.related_organization
                                userRole.related_user = selected_student.first()
                                try:
                                    userRole.validate_unique()
                                    userRole.save()
                                    approvers = EN_UserRoles.objects.filter(approved=True,related_organization=active_role.related_organization,role__code=Roles.SCHOOL_ADMIN)
                                    if approvers.exists():
                                        for approver in approvers:
                                            activity.createActivity(ActivityPattern.RECEIVED_ROLE_REQUEST, approver.user,userRole, False)
                                        retDict["status"] = True
                                    else:
                                        userRole.delete()
                                        retDict["message"] = DisplayKey.get("no_approvers_found_for_this_organization")
                                except Exception as e:
                                    retDict["message"] = e.__str__()
                            else:
                                retDict["message"] = DisplayKey.get("selected_student_does_not_belong_to_your_school")
                        else:
                            retDict["message"] = DisplayKey.get("student_not_found")
                    else:
                        retDict["message"] = DisplayKey.get("selected_role_lacks_permission_to_send_or_approve_role_request")
            else:
                retDict["message"] = DisplayKey.get("selected_role_lacks_permission_to_send_or_approve_role_request")

            if retDict["status"] == True and selected_role.code != Roles.PARENT:
                messages.success(request, DisplayKey.get("role_raised_successfully"))
            return HttpResponse(json.dumps(retDict))
        else:
            messages.warning(request, DisplayKey.get("error_not_a_post_request"))
            return HttpResponseRedirect("../Home")
    else:
        return HttpResponseRedirect("../Redirects/ErrorPage?page=404")


''''
    Function  : Ajax function to get all user details as per myshishya id provided
    Method    : AJAX POST
'''
@csrf_exempt
def getUserDetails(request):
    if request.is_ajax():
        product_ids = request.POST["product_ids"]
        student_id = request.POST["student_id"]
        retDict = {
            "status" : False,
            "message": None,
            "data": []
        }
        prdIdListString = (product_ids.replace(" ", "")).strip()
        if (re.match('^[MY0-9,]+$', prdIdListString) == None):
            retDict["message"] = DisplayKey.get("invalid_characters_in_product_id_list")
        else:
            prdId_list = list(prdIdListString.split(","))
            student = EN_Users.objects.get(id=int(student_id))
            if student.product_id in prdId_list:
                retDict["message"] = DisplayKey.get("parent_id_and_student_id_cannot_be_same")
            else:
                users = EN_Users.objects.filter(product_id__in=prdId_list)
                retList = []
                prodComparisonList = []
                for user in users:
                    addr = EN_AddressBook.objects.get(user=user, is_permanent_address=True)
                    permanent_adr = addr.house_name + ", " + addr.street
                    retUserDict = {
                        "id": user.id,
                        "name": user.name,
                        "gender": user.gender.code,
                        "contact_no": user.contact.mobile_number,
                        "address": permanent_adr,
                        "dp": user.display_picture,
                        "product_id": user.product_id
                    }
                    prodComparisonList.append(user.product_id)
                    retList.append(retUserDict)
                diff = set(prdId_list) - set(prodComparisonList)
                if diff.__len__() > 0:
                    retDict["message"] = "Could not find Myshishya ID(s) : {}".format(diff.__str__())
                else:
                    retDict["status"] = True
                    retDict["data"] = retList
        return HttpResponse(json.dumps(retDict))
    else:
        messages.warning(request, DisplayKey.get("direct_access_denied"))
        return HttpResponse("../Page404/")


'''
    Function  : Change the role from the session and redirects to home page
    Method    : POST 
'''
def changeRole(request):
    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role_id = 0 if not "user_role_id" in request.POST else int(request.POST["user_role_id"])
    if user_role_id == 0:
        EN_UserRoles.objects.filter(user_id = user_id, is_selected_role=True).update(is_selected_role = False)
        messages.success(request, DisplayKey.get("role_changes_successfully"))
    else:
        try:
            ur = EN_UserRoles.objects.get(id=user_role_id, approved=True,user_id=user_id)
            if ur.is_selected_role:
                messages.warning(request, DisplayKey.get("already_on_the_same_role"))
            else:
                EN_UserRoles.objects.filter(user_id=user_id, is_selected_role=True).update(is_selected_role=False)
                ur.is_selected_role = True
                ur.validate_unique()
                ur.save()
                messages.success(request, DisplayKey.get("role_changes_successfully"))
        except:
            messages.error(request, DisplayKey.get("no_such_role_for_user"))
    return HttpResponseRedirect('../Home')


@csrf_exempt
def getRolesRaisedByMe(request):
    if request.is_ajax():
        page = int(request.POST.get('page'))
        page = 1 if page < 1 else page
        pageRowCount = int(request.POST.get('page_row_count'))
        search_keyword = request.POST.get('search_keyword').strip()
        startingIndex = (page-1)*pageRowCount
        endingIndex = page*pageRowCount
        user_id = request.session[SessionProperties.USER_ID_KEY]
        records = EN_UserRoles.objects.filter(request_raised_by_id = user_id).order_by('-id')
        records = records.filter(Q(role__code__contains=search_keyword))

        total_records_count = records.all().count()
        records = records.all()[startingIndex:endingIndex]
        retList = []
        for record in records:
            returnDict = {
                "user_role_id"        :record.id,
                "role_name"           :record.role.name,
                "status"              :record.approved,
                "request_raised_by"   :record.request_raised_by.name,
                "request_approved_by" :record.request_approved_by.name if record.request_approved_by != None else None,
                "request_approved_on" :(record.request_approved_on.__str__().split(" "))[0]  if record.request_approved_by != None else None,
                "request_raised_on"   :(record.request_raised_on.__str__().split(" "))[0]
            }

            if record.related_organization_group != None:
                returnDict.__setitem__("is_org_grp_related",True)
                returnDict.__setitem__("group_id",record.related_organization_group.id)
                returnDict.__setitem__("group_name",record.related_organization_group.group_name)
                returnDict.__setitem__("group_prd_id",record.related_organization_group.product_id)
                returnDict.__setitem__("dp",record.related_organization_group.logo)
            elif record.related_organization != None and record.related_user == None :
                returnDict.__setitem__("is_org_related", True)
                returnDict.__setitem__("school_id", record.related_organization.id)
                returnDict.__setitem__("school_name", record.related_organization.school_name)
                returnDict.__setitem__("school_prd_id", record.related_organization.product_id)
                returnDict.__setitem__("school_street", record.related_organization.street)
                returnDict.__setitem__("dp", record.related_organization.display_picture)
            elif record.related_organization != None and record.related_user != None :
                returnDict.__setitem__("is_parent", True)
                returnDict.__setitem__("user_id", record.related_user.id)
                returnDict.__setitem__("user_name", record.related_user.name)
                returnDict.__setitem__("user_gender", record.related_user.gender.name)
                returnDict.__setitem__("user_prd_id", record.related_user.product_id)
                returnDict.__setitem__("dp", record.related_user.display_picture)
                returnDict.__setitem__("school_name", record.related_organization.school_name)
                returnDict.__setitem__("school_prd_id", record.related_organization.product_id)
                returnDict.__setitem__("school_street", record.related_organization.street)

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

@csrf_exempt
def getMyRoles(request):
    if request.is_ajax():
        page = int(request.POST.get('page'))
        page = 1 if page < 1 else page
        pageRowCount = int(request.POST.get('page_row_count'))
        search_keyword = request.POST.get('search_keyword')
        startingIndex = (page-1)*pageRowCount
        endingIndex = page*pageRowCount
        user_id = request.session[SessionProperties.USER_ID_KEY]
        records = EN_UserRoles.objects.filter(user_id = user_id)
        if search_keyword != None:
            records = records.filter(Q(role__code__contains=search_keyword))
        total_records_count = records.all().count()
        records = records.all()[startingIndex:endingIndex]
        retList = []
        for record in records:
            returnDict = {
                "user_role_id"               :record.id,
                "role_name"                  :record.role.name,
                "status"                     :record.approved,
                "is_current_role"            :record.is_selected_role,
                "request_raised_by_prd_id"   :record.request_raised_by.product_id,
                "request_raised_by"          :record.request_raised_by.name,
                "request_approved_by_prd_id" :record.request_approved_by.product_id if record.request_approved_by != None else None,
                "request_approved_by"        :record.request_approved_by.name if record.request_approved_by != None else None,
                "request_approved_on"        :(record.request_approved_on.__str__().split(" "))[0]  if record.request_approved_by != None else None,
                "request_raised_on"          :(record.request_raised_on.__str__().split(" "))[0]
            }

            if record.related_organization_group != None:
                returnDict.__setitem__("is_org_grp_related",True)
                returnDict.__setitem__("group_id",record.related_organization_group.id)
                returnDict.__setitem__("group_name",record.related_organization_group.group_name)
                returnDict.__setitem__("group_prd_id",record.related_organization_group.product_id)
                returnDict.__setitem__("dp",record.related_organization_group.logo)
            elif record.related_organization != None and record.related_user == None :
                returnDict.__setitem__("is_org_related", True)
                returnDict.__setitem__("school_id", record.related_organization.id)
                returnDict.__setitem__("school_name", record.related_organization.school_name)
                returnDict.__setitem__("school_prd_id", record.related_organization.product_id)
                returnDict.__setitem__("school_street", record.related_organization.street)
                returnDict.__setitem__("dp", record.related_organization.display_picture)
            elif record.related_organization != None and record.related_user != None :
                returnDict.__setitem__("is_parent", True)
                returnDict.__setitem__("user_id", record.related_user.id)
                returnDict.__setitem__("user_name", record.related_user.name)
                returnDict.__setitem__("user_gender", record.related_user.gender.name)
                returnDict.__setitem__("user_prd_id", record.related_user.product_id)
                returnDict.__setitem__("dp", record.related_user.display_picture)
                returnDict.__setitem__("school_name", record.related_organization.school_name)
                returnDict.__setitem__("school_prd_id", record.related_organization.product_id)
                returnDict.__setitem__("school_street", record.related_organization.street)

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


def roleRequestsReceived(request):
    data = UIDataHelper(request).getData(page="is_role_requests_received")
    template = loader.get_template("roles_role_requests_received.html")
    return HttpResponse(template.render(data, request))



@csrf_exempt
def getRoleRequestsReceived(request):
    if request.is_ajax():
        page = int(request.POST.get('page'))
        page = 1 if page < 1 else page
        pageRowCount = int(request.POST.get('page_row_count'))
        search_keyword = request.POST.get('search_keyword')
        startingIndex = (page-1)*pageRowCount
        endingIndex = page*pageRowCount
        user_id = request.session[SessionProperties.USER_ID_KEY]
        my_role = EN_UserRoles.objects.filter(user_id = user_id, is_selected_role=True, role__code__in=[Roles.SCHOOL_ADMIN,Roles.INSTITUTION_SUPER_USER], approved=True)
        if my_role.exists():
            my_role = my_role[0]
            records = EN_UserRoles.objects.filter(approved=False, related_organization=my_role.related_organization, related_organization_group=my_role.related_organization_group)
            if search_keyword != None:
                records = records.filter(Q(role__code__contains=search_keyword))
            total_records_count = records.all().count()
            records = records.all()[startingIndex:endingIndex]
            retList = []
            for record in records:
                returnDict = {
                    "user_role_id"        :record.id,
                    "role_name"           :record.role.name,
                    "status"              :record.approved,
                    "is_current_role"     :record.is_selected_role,
                    "request_raised_by"   :record.request_raised_by.name,
                    "request_approved_by" :record.request_approved_by.name if record.request_approved_by != None else None,
                    "request_approved_on" :(record.request_approved_on.__str__().split(" "))[0]  if record.request_approved_by != None else None,
                    "request_raised_on"   :(record.request_raised_on.__str__().split(" "))[0]
                }

                if record.related_organization_group != None:
                    returnDict.__setitem__("is_org_grp_related",True)
                    returnDict.__setitem__("group_id",record.related_organization_group.id)
                    returnDict.__setitem__("group_name",record.related_organization_group.group_name)
                    returnDict.__setitem__("group_prd_id",record.related_organization_group.product_id)
                    returnDict.__setitem__("dp",record.related_organization_group.logo)
                elif record.related_organization != None and record.related_user == None :
                    returnDict.__setitem__("is_org_related", True)
                    returnDict.__setitem__("school_id", record.related_organization.id)
                    returnDict.__setitem__("school_name", record.related_organization.school_name)
                    returnDict.__setitem__("school_prd_id", record.related_organization.product_id)
                    returnDict.__setitem__("school_street", record.related_organization.street)
                    returnDict.__setitem__("dp", record.related_organization.display_picture)
                elif record.related_organization != None and record.related_user != None :
                    returnDict.__setitem__("is_parent", True)
                    returnDict.__setitem__("user_id", record.related_user.id)
                    returnDict.__setitem__("user_name", record.related_user.name)
                    returnDict.__setitem__("user_gender", record.related_user.gender.name)
                    returnDict.__setitem__("user_prd_id", record.related_user.product_id)
                    returnDict.__setitem__("dp", record.related_user.display_picture)
                    returnDict.__setitem__("school_name", record.related_organization.school_name)
                    returnDict.__setitem__("school_prd_id", record.related_organization.product_id)
                    returnDict.__setitem__("school_street", record.related_organization.street)

                retList.append(returnDict)
            ret = {
                "total_pages" : ceil(total_records_count / pageRowCount),
                "total_records" : total_records_count,
                "data" : retList
            }

            jsonResponse = json.dumps(ret)
            return HttpResponse(jsonResponse)
        else:
            # no permitted /  active role
            # return error message
            pass
    else:
        return HttpResponseRedirect("../Redirects/ErrorPage?page=403")