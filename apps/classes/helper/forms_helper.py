import json

from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from apps.school_timings.models import EN_SchoolTimings
from properties.app_roles import Roles
from properties.session_properties import SessionProperties

class FormsHelper:

    def __init__(self,request):
        self.request = request
        self.user_id = request.session[SessionProperties.USER_ID_KEY]

    def getTeachers(self):
        roleData = json.loads(self.request.session[SessionProperties.USER_SELECTED_ROLE_KEY])
        try:
            orgId = EN_UserRoles.objects.get(id = roleData['role_id'])
            teacherList = []
            for row in EN_UserRoles.objects.filter(related_organization=orgId.related_organization, role__code=Roles.TEACHER, approved=True):
                classList = []
                classList.append(row.user.id)
                classList.append(row.user.name)
                teacherList.append(tuple(classList))
            return tuple(teacherList)
        except:
            return ((None,"No Permission"))

    def getPatterns(self):
        try:
            role = EN_UserRoles.objects.get(user_id=self.user_id, approved=True, is_selected_role=True)
            retArray = []
            for timing in EN_SchoolTimings.objects.filter(organization= role.related_organization):
                array = []
                array.append(timing.id)
                array.append(timing.timing_name)
                retArray.append(tuple(array))
            return tuple(retArray)
        except:
            return ((None,"No Permission"))

    def getClasses(self):
        try:
            user_role = EN_UserRoles.objects.get(user_id=self.user_id, approved=True, is_selected_role=True)
            retArray = []
            retArray.append(tuple(["all","List All"]))
            for cls in EN_Classes.objects.filter(organization=user_role.related_organization):
                array = []
                array.append(cls.class_name)
                array.append("Class - "+cls.class_name)
                retArray.append(tuple(array))
            return tuple(set(retArray))
        except:
            return ((None, "No Permission"))