from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles


class SubjectFormsHelper:

    def getClasses(self, rolesData):
        orgId = EN_UserRoles.objects.get(id = rolesData['role_id'])
        allClassList = []
        classList = EN_Classes.objects.filter(organization=orgId.related_organization)
        for row in classList:
            classList = []
            classList.append(row.id)
            classList.append(row.class_name)
            allClassList.append(tuple(classList))
        return allClassList
