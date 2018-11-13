from properties.app_roles import Roles

class RoleApprovalHierarchy():

    ROLE_APPROVAL_HIERARCHY = {
        Roles.SITE_ADMIN             : [Roles.SITE_ADMIN],
        Roles.INSTITUTION_SUPER_USER : [Roles.INSTITUTION_SUPER_USER],
        Roles.DIRECTOR               : [Roles.INSTITUTION_SUPER_USER],
        Roles.BOARD_MEMBER           : [Roles.INSTITUTION_SUPER_USER],
        Roles.SCHOOL_ADMIN           : [Roles.INSTITUTION_SUPER_USER],

        Roles.PRINCIPAL              : [Roles.SCHOOL_ADMIN],
        Roles.STUDENT                : [Roles.TEACHER, Roles.SCHOOL_ADMIN],
        Roles.PARENT                 : [Roles.TEACHER, Roles.SCHOOL_ADMIN],
        Roles.TEACHER                : [Roles.SCHOOL_ADMIN],
        Roles.LIBRARIAN              : [Roles.SCHOOL_ADMIN],
        Roles.ACCOUNTANT             : [Roles.SCHOOL_ADMIN],
        Roles.LAB_ASSISTANT          : [Roles.SCHOOL_ADMIN],
        Roles.ENQUIRY_ASSISTANT      : [Roles.SCHOOL_ADMIN],
        Roles.SECURITY               : [Roles.SCHOOL_ADMIN],
    }

    INSTITUTION_SU_APPROVAL_LIST = [Roles.INSTITUTION_SUPER_USER,Roles.DIRECTOR,Roles.BOARD_MEMBER, Roles.SCHOOL_ADMIN]
    SCHOOL_ADMIN_APPROVAL_LIST   = [Roles.SCHOOL_ADMIN,Roles.TEACHER,Roles.PRINCIPAL,Roles.STUDENT,Roles.PARENT,Roles.LIBRARIAN,Roles.ACCOUNTANT,Roles.LAB_ASSISTANT,Roles.ENQUIRY_ASSISTANT,Roles.SECURITY]
    TEACHER_APPROVAL_LIST        = [Roles.STUDENT, Roles.PARENT]