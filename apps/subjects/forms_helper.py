from apps.classes.models import EN_Classes


class SubjectFormsHelper():

    def getClasses(self):
        allClassList = []
        for row in EN_Classes.objects.all():
            classList = []
            classList.append(row.id)
            classList.append(row.class_name)
            allClassList.append(tuple(classList))
        return allClassList
