from django.urls import path

from apps.roles import views_modify_roles
from . import views

urlpatterns = [

    #loads the index page and loads the user roles
    path(r'',views.index, name="Roles Index Page"),
    path(r'GetMyRoles', views.getMyRoles, name="Get Roles On MyName| AJAX"),

    # Change the current role
    path(r'Change',views.changeRole, name="Change Role"),

    #New Role assignement
    path(r'AssignRole',views.loadRoleSettingPage, name="Assign Role For Other Users"),
    path(r'ValidateAssignedRole',views.validateAssignedRole, name="Save Assigned Roles"),
    path(r'SaveAssignedRole',views.saveAssignedRole, name="Confirm Save Assigned Roles"),
    path(r'GetUserDetails',views.getUserDetails, name="Get User Details"),

    #Raised Roles History
    path(r'RolesRaised', views.listAllRaisedRoles, name="All Raised Roles"),
    path(r'GetRolesRaisedByMe', views.getRolesRaisedByMe,name="Get Roles Raised By This User| AJAX"),

    #Role Approval List
    path(r'RoleRequestsReceived', views.roleRequestsReceived,name="Get Roles Received For This User"),
    path(r'GetRoleRequestsReceived', views.getRoleRequestsReceived,name="Get Roles Received For This User| AJAX"),

    #User Roles Modification
    path(r'ModifyUserRoles', views_modify_roles.modifyUserRoles, name="Renders User Role Modification Page "),
    path(r'FilterUser', views_modify_roles.filterUser, name="Filter user using the filter conditions"),

]