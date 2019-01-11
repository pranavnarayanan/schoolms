from properties.app_roles import Roles

class AppAccessibilityDictionary():

    # Apps which can be accessed by all roles
    APPS_WITH_FULL_ACCESS_TO_ALL_USERS = [
        "admin", "SignUp", "Logout", "Login", "Notifications","Roles","Home", "Messages", "Settings","Tasks",
        "Books","Users","Subjects","Documents","SchoolTimings","Timetable","Attendance","Batch"
    ]

    # Apps with user role permissions
    APPS_WITH_LIMITED_ACCESS_TO_USERS = {
        "Organization": {
            "Index"                 : [Roles.SITE_ADMIN],
            "OrganizationGroups"    : [Roles.SITE_ADMIN],
            "GetOrganizationGroups" : [Roles.SITE_ADMIN],
            "GetOrganizations"      : [Roles.SITE_ADMIN],
            "Organizations"         : [Roles.SITE_ADMIN],
            "RegisterGroup"         : [Roles.SITE_ADMIN],
            "SaveOrganizationGroup" : [Roles.SITE_ADMIN],
            "RegisterOrganization"  : [Roles.SITE_ADMIN],
            "SaveOrganization"      : [Roles.SITE_ADMIN],
            "LoadAreaFromZipcode"   : [Roles.SITE_ADMIN],
            "Organization"          : [Roles.SITE_ADMIN],
            "OrganizationGroup"     : [Roles.SITE_ADMIN],
        },
        "Roles":{
            "Index"                   : ["all"],
            "RolesRaised"             : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN,Roles.TEACHER],
            "Change"                  : ["all"],
            "AssignRole"              : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN,Roles.TEACHER],
            "GetAllSchoolsOnOrgGroup" : [Roles.INSTITUTION_SUPER_USER],
            "ValidateAssignedRole"    : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN,Roles.TEACHER],
            "SaveAssignedRole"        : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN,Roles.TEACHER],
            "GetUserDetails"          : [Roles.SCHOOL_ADMIN,Roles.TEACHER],
            "GetMyRoles"              : ["all"],
            "GetRolesRaisedByMe"      : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN,Roles.TEACHER],
            "RoleRequestsReceived"    : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN],
            "GetRoleRequestsReceived" : [Roles.INSTITUTION_SUPER_USER,Roles.SCHOOL_ADMIN],
        },
        "Classes":{
            "Index"               : [Roles.SCHOOL_ADMIN, Roles.PRINCIPAL],
            "AddNewClass"         : [Roles.SCHOOL_ADMIN],
            "SaveClass"           : [Roles.SCHOOL_ADMIN],
            "AddSubjectToClass"   : [Roles.SCHOOL_ADMIN],
            "SaveSubjectToClass"  : [Roles.SCHOOL_ADMIN]
        },
        "Announcements":{
            "Index"    : ["all"],
            "Create"   : [Roles.SCHOOL_ADMIN, Roles.PRINCIPAL, Roles.TEACHER],
        },
        "Users":{
            "Index"              : ["all"],
            "ChangeOnlineStatus" : ["all"],
        }
    }
