import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from apps.roles.models import EN_UserRoles
from apps.school_timings.forms import FORM_SchoolTiming, FORM_AddModifySchoolTiming_Page1
from apps.school_timings.models import EN_SchoolTimings, EN_SchoolTimingBreakup
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties
from django.contrib import messages


def index(request):
    data = UIDataHelper(request).getData(page="is_list_school_timings")

    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True,role__code=Roles.SCHOOL_ADMIN)
    if user_role.exists():
        user_role = user_role.first()
        timings = EN_SchoolTimings.objects.filter(organization=user_role.related_organization)
        dataList = []
        for timing in timings:
            off_days = ""
            if timing.class_off_on_sunday:
                off_days += "Sunday, "
            if timing.class_off_on_monday:
                off_days += "Monday, "
            if timing.class_off_on_tuesday:
                off_days += "Tuesday, "
            if timing.class_off_on_wednesday:
                off_days += "Wednesday, "
            if timing.class_off_on_thursday:
                off_days += "Thursday, "
            if timing.class_off_on_friday:
                off_days += "Friday, "
            if timing.class_off_on_saturday:
                off_days += "Saturday, "
            off_days = off_days.strip()
            if off_days.__len__() > 0:
                if off_days[-1] == ",":
                    off_days = off_days[:-1]

            dataList.append({
                "name" : timing.timing_name,
                "timing":"{} to {} ".format(timing.school_starting_time,timing.school_closing_time),
                "off_days":off_days,
            })

        data.__setitem__("timings",dataList)
        template = loader.get_template("school_timings_list_all_timings.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.warning(request, DisplayKey.get("current_role_cannot_perform_this_action"))
        return HttpResponseRedirect("../Home")


def addSchoolTimings_Page1(request):
    data = UIDataHelper(request).getData(page="is_add_school_timings")
    form = FORM_AddModifySchoolTiming_Page1(request.POST, request=request) if request.method == "POST" else FORM_AddModifySchoolTiming_Page1(request=request)
    template = loader.get_template("school_timings_page_1.html")

    data.__setitem__("form", form)
    messages.info(request,"You can create a new timing or modify an existing timing")
    return HttpResponse(template.render(data, request))


def addSchoolTimings_Page1_Submit(request):
    if request.method == "POST":
        form_data = FORM_AddModifySchoolTiming_Page1(request.POST, request=request)
        if form_data.is_valid():
            if request.POST["type"] not in ["update","new"]:
                messages.warning(request, DisplayKey.get("invalid_school_timing_submit_type"))
                return HttpResponseRedirect("../SchoolTimings")
            else:
                request.session["PAGE_1_DATA"] = json.dumps({
                    "school_timing_name" : form_data["school_timing_name"].value(),
                    "school_timing_id" : 0 if request.POST["type"] != "update" else int(form_data["available_timings"].value()),
                })
                return HttpResponseRedirect("TimingDetails")
        else:
            return addSchoolTimings_Page1(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")



def addSchoolTimings_Page2(request):
    if "PAGE_1_DATA" in request.session:
        data = UIDataHelper(request).getData(page="is_add_school_timings")
        data.__setitem__("form",FORM_SchoolTiming(request.POST,request=request) if request.method == "POST" else FORM_SchoolTiming(request=request))
        template = loader.get_template("school_timings_page_2.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.warning(request, "Set/Select Timing Name First ")
        return HttpResponseRedirect("AddModifyTiming")


def addSchoolTimings_Page2_Submit(request):
    if request.POST["action"] == "forward":
        if "PAGE_1_DATA" in request.session:
            user_id = request.session[SessionProperties.USER_ID_KEY]
            user_role = EN_UserRoles.objects.filter(approved=True,user_id=user_id,is_selected_role=True, role__code=Roles.SCHOOL_ADMIN)
            if user_role.exists():
                user_role = user_role.first()
                if(user_role.related_organization != None):
                    form_data = FORM_SchoolTiming(request.POST,request=request)
                    if form_data.is_valid():
                        pageData = json.loads(request.session["PAGE_1_DATA"])
                        if pageData["school_timing_id"] == 0:
                            st = EN_SchoolTimings()
                        else:
                            st = EN_SchoolTimings.objects.get(id=int(pageData["school_timing_id"]))
                        try:
                            st.organization = user_role.related_organization
                            st.timing_name = form_data["school_timing_name"].value()
                            st.school_starting_time = form_data["school_start_time"].value()
                            st.school_closing_time  = form_data["school_closing_time"].value()
                            st.assembly_duration    = int(form_data["assembly_duration"].value()) if form_data["assembly_duration"].value() != "" else None

                            st.assembly_on_sunday    = form_data["assembly_on_sunday"].value()
                            st.assembly_on_monday    = form_data["assembly_on_monday"].value()
                            st.assembly_on_tuesday   = form_data["assembly_on_tuesday"].value()
                            st.assembly_on_wednesday = form_data["assembly_on_wednesday"].value()
                            st.assembly_on_thursday  = form_data["assembly_on_thursday"].value()
                            st.assembly_on_friday    = form_data["assembly_on_friday"].value()
                            st.assembly_on_saturday  = form_data["assembly_on_saturday"].value()

                            st.class_off_on_sunday    = form_data["class_off_on_sunday"].value()
                            st.class_off_on_monday    = form_data["class_off_on_monday"].value()
                            st.class_off_on_tuesday   = form_data["class_off_on_tuesday"].value()
                            st.class_off_on_wednesday = form_data["class_off_on_wednesday"].value()
                            st.class_off_on_thursday  = form_data["class_off_on_thursday"].value()
                            st.class_off_on_friday    = form_data["class_off_on_friday"].value()
                            st.class_off_on_saturday  = form_data["class_off_on_saturday"].value()

                            st.save()
                            del(request.session["PAGE_1_DATA"])
                            messages.success(request, "Successfully added/modified school timing")
                        except Exception as e:
                            messages.warning(request, e.__str__())
                            return addSchoolTimings_Page2(request)
                    else:
                        return addSchoolTimings_Page2(request)
                else:
                    messages.warning(request, DisplayKey.get("no_organization_associated_to_this_role"))
                    return HttpResponseRedirect("../SchoolTimings")
            else:
                messages.warning(request, DisplayKey.get("current_role_cannot_perform_this_action"))
                return HttpResponseRedirect("../SchoolTimings")

            return HttpResponseRedirect("../SchoolTimings")
        else:
            messages.warning(request, DisplayKey.get("School Timing Session Expired"))
            return HttpResponseRedirect("AddModifyTiming")
    else:
        return HttpResponseRedirect("AddModifyTiming")


def addSchoolTimings_Page3(request):
    data = UIDataHelper(request).getData(page="is_add_school_timings")
    user_id = request.session[SessionProperties.USER_ID_KEY]
    user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True,role__code=Roles.SCHOOL_ADMIN)
    if user_role.exists():
        user_role = user_role.first()
        data.__setitem__("school_timings",[{
            "id":st.id,
            "name":st.timing_name
        }for st in EN_SchoolTimings.objects.filter(organization=user_role.related_organization)])

        template = loader.get_template("school_timings_page_3.html")
        return HttpResponse(template.render(data, request))
    else:
        messages.warning(request, DisplayKey.get("current_role_cannot_perform_this_action"))
        return HttpResponseRedirect("../Home")



@csrf_exempt
def addSchoolTimings_loadBreakUpData(request):
    if request.is_ajax():
        user_id = request.session[SessionProperties.USER_ID_KEY]
        user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True,role__code=Roles.SCHOOL_ADMIN)
        if user_role.exists():
            user_role = user_role.first()
            school_timing_id = int(request.POST["school_timing_id"])
            st = EN_SchoolTimings.objects.filter(organization=user_role.related_organization,id=school_timing_id)
            if st.exists():
                st = st.first()
                retData = {
                 "data" : [{
                        "is_period": timing_breakup.is_period,
                        "is_break": timing_breakup.is_break,
                        "duration": timing_breakup.duration,
                        "description": timing_breakup.description
                    } for timing_breakup in EN_SchoolTimingBreakup.objects.filter(timing=st)],
                 "school_starting_time":(st.school_starting_time.hour*60)+st.school_starting_time.minute,
                 "school_closing_time":(st.school_closing_time.hour*60)+st.school_closing_time.minute
                }
                return HttpResponse(json.dumps(retData))
            else:
                # No timing available
                return HttpResponse(-1)
        else:
            # No Permission
            return HttpResponse(-2)
    else:
        messages.warning(request,"Direct Access Denied")
        return HttpResponseRedirect("../Home")


@csrf_exempt
def addSchoolTimings_saveBreakUpData(request):
    if request.is_ajax():
        user_id = request.session[SessionProperties.USER_ID_KEY]
        user_role = EN_UserRoles.objects.filter(approved=True, user_id=user_id, is_selected_role=True,role__code=Roles.SCHOOL_ADMIN)
        if user_role.exists():
            user_role = user_role.first()
            school_timing_id = int(request.POST["school_timing_id"])
            timing_data = json.loads(request.POST["timing_data"])
            st = EN_SchoolTimings.objects.filter(organization=user_role.related_organization,id=school_timing_id)
            if st.exists():
                st = st.first()
                EN_SchoolTimingBreakup.objects.filter(timing=st).delete()
                for timing in timing_data:
                    stb = EN_SchoolTimingBreakup()
                    stb.timing = st
                    stb.is_period = True if (timing["type"] == "Period") else False
                    stb.is_break = (not stb.is_period)
                    stb.duration = int(timing["duration"])
                    stb.save()
                return HttpResponse(1)
            else:
                # No timing available
                return HttpResponse(-1)
        else:
            # No Permission
            return HttpResponse(-2)
    else:
        messages.warning(request,"Direct Access Denied")
        return HttpResponseRedirect("../Home")
