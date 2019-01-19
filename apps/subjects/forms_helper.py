from apps.classes.models import EN_Classes
from apps.roles.models import EN_UserRoles
from properties.session_properties import SessionProperties


class SubjectFormsHelper:

    def __init__(self,request):
        self.request = request
        self.user_id = request.session[SessionProperties.USER_ID_KEY]
        self.divisions = []

    def getClasses(self, rolesData):
        orgId = EN_UserRoles.objects.get(id = rolesData['role_id'])
        allClassList = []
        classList = EN_Classes.objects.filter(organization=orgId.related_organization)
        for row in classList:
            classList = []
            classList.append(row.id)
            class_display_name =row.class_name + "-" + row.class_division
            class_display_name = (class_display_name+"("+row.batch_nick_name+")") if row.batch_nick_name != "" else class_display_name
            classList.append(class_display_name)
            allClassList.append(tuple(classList))
        return allClassList

    def getClassesForFilter(self):
        try:
            user_role = EN_UserRoles.objects.get(user_id=self.user_id, approved=True, is_selected_role=True)
            retArray = []
            divArray = []
            divArray.append(tuple(["all","List All"]))
            retArray.append(tuple(["all","List All"]))
            for cls in EN_Classes.objects.filter(organization=user_role.related_organization):
                array = []
                divDetail = []
                array.append(cls.class_name)
                array.append("Class - "+cls.class_name)
                divDetail.append(cls.class_division)
                divDetail.append("Division - "+cls.class_division)
                divArray.append(tuple(divDetail))
                retArray.append(tuple(array))
            self.divisions = divArray
            return tuple(set(retArray))
        except:
            return ((None, "No Permission"))


    def getDivisionForFilter(self):
        try:
            return tuple(set(self.divisions))
        except:
            return ((None, "No Permission"))
