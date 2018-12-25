from apps.roles.models import EN_UserRoles
from properties.app_roles import Roles


class ClassFormsHelper:

    def getTeachers(self, rolesData):
        orgId = EN_UserRoles.objects.get(id = rolesData['role_id'])
        teacherList = []
        filteredList = EN_UserRoles.objects.filter(related_organization=orgId.related_organization, role__code=Roles.TEACHER)
        for row in filteredList:
            classList = []
            classList.append(row.user.id)
            classList.append(row.user.name)
            teacherList.append(tuple(classList))
        return teacherList
