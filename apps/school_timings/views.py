from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from apps.roles.models import EN_UserRoles
from apps.school_timings.forms import FORM_SchoolTiming
from apps.school_timings.models import EN_SchoolTimings
from apps.utilities.helper.ui_data_helper import UIDataHelper
from displaykey.display_key import DisplayKey
from properties.app_roles import Roles
from properties.session_properties import SessionProperties
from django.contrib import messages


def index(request):
    data = UIDataHelper(request).getData(page="is_list_school_timings")
    template = loader.get_template("school_timings_list_all_timings.html")
    return HttpResponse(template.render(data, request))


def addSchoolTimings(request):
    data = UIDataHelper(request).getData(page="is_add_school_timings")
    data.__setitem__("form",FORM_SchoolTiming(request.POST) if request.method == "POST" else FORM_SchoolTiming())
    template = loader.get_template("school_timings_add_new_timing.html")
    return HttpResponse(template.render(data, request))


def submitSchoolDetails(request):
    if request.method == "POST":
        form_data = FORM_SchoolTiming(request.POST)
        if form_data.is_valid():
            user_id = request.session[SessionProperties.USER_ID_KEY]

            timing_name                   = form_data["timing_name"].value()
            school_start_time             = form_data["school_start_time"].value()
            school_closing_time           = form_data["school_closing_time"].value()
            total_periods                 = form_data["total_periods"].value()
            school_off_days               = form_data["school_off_days"].value()
            interval_1_starting_time      = form_data["interval_1_starting_time"].value()
            interval_1_ending_time        = form_data["interval_1_ending_time"].value()
            interval_2_starting_time      = form_data["interval_2_starting_time"].value()
            interval_2_ending_time        = form_data["interval_2_ending_time"].value()
            interval_3_starting_time      = form_data["interval_3_starting_time"].value()
            interval_3_ending_time        = form_data["interval_3_ending_time"].value()
            interval_4_starting_time      = form_data["interval_4_starting_time"].value()
            interval_4_ending_time        = form_data["interval_4_ending_time"].value()
            breakfast_break_starting_time = form_data["breakfast_break_starting_time"].value()
            breakfast_break_ending_time   = form_data["breakfast_break_ending_time"].value()
            lunch_break_starting_time     = form_data["lunch_break_starting_time"].value()
            lunch_break_ending_time       = form_data["lunch_break_ending_time"].value()
            dinner_break_starting_time    = form_data["dinner_break_starting_time"].value()
            dinner_break_ending_time      = form_data["dinner_break_ending_time"].value()
            assembly_starting_time        = form_data["assembly_starting_time"].value()
            assembly_ending_time          = form_data["assembly_ending_time"].value()
            assembly_on_days              = form_data["assembly_on_days"].value()

            user_role = EN_UserRoles.objects.filter(approved=True,user_id=user_id,is_selected_role=True, role__code=Roles.SCHOOL_ADMIN)
            if user_role.exists():
                user_role = user_role.first()
                if(user_role.related_organization != None):

                    try:
                        st = EN_SchoolTimings()
                        st.organization                      = user_role.related_organization
                        st.timing_name                       = timing_name
                        st.school_starting_time              = school_start_time
                        st.school_closing_time               = school_closing_time
                        st.breakfast_starting_time           = breakfast_break_starting_time
                        st.breakfast_ending_time             = breakfast_break_ending_time
                        st.lunch_starting_time               = lunch_break_starting_time
                        st.lunch_ending_time                 = lunch_break_ending_time
                        st.dinner_starting_time              = dinner_break_starting_time
                        st.dinner_ending_time                = dinner_break_ending_time
                        st.no_of_periods                     = int(total_periods)
                        st.first_interval_starting_time      = interval_1_starting_time
                        st.first_interval_ending_time        = interval_1_ending_time
                        st.second_interval_starting_time     = interval_2_starting_time
                        st.second_interval_ending_time       = interval_2_ending_time
                        st.third_interval_starting_time      = interval_3_starting_time
                        st.third_interval_ending_time        = interval_3_ending_time
                        st.fourth_interval_starting_time     = interval_4_starting_time
                        st.fourth_interval_ending_time       = interval_4_ending_time
                        st.assembly_on_days                  = assembly_on_days.__str__()
                        st.assembly_starting_time            = assembly_starting_time
                        st.assembly_ending_time              = assembly_ending_time
                        st.off_days                          = school_off_days.__str__()
                        st.save()
                    except Exception as e:
                        messages.warning(request, str(e))
                        return addSchoolTimings(request)
                else:
                    messages.warning(request, DisplayKey.get("no_organization_associated_to_this_role"))
                    return HttpResponseRedirect("../SchoolTimings")
            else:
                messages.warning(request, DisplayKey.get("current_role_cannot_perform_this_action"))
                return HttpResponseRedirect("../SchoolTimings")

            return HttpResponseRedirect("../SchoolTimings")
        else:
            return addSchoolTimings(request)
    else:
        messages.warning(request, DisplayKey.get("error_not_a_post_request"))
        return HttpResponseRedirect("../Home")