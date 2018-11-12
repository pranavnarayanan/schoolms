class AppUtil:

    def __init__(self, request):
        fullPath = request.get_full_path()
        if list(fullPath).__contains__("?"):
            fullPathList = list((fullPath.split("?")[0]).split("/"))
        else:
            fullPathList = list(fullPath.split("/"))

        for uri in fullPathList:
            if uri.strip() == "":
                fullPathList.remove(uri)

        self.__fullPathArray__ = fullPathList


    def App(self):
        return self.__fullPathArray__[0]

    def Method(self):
        return "Index" if self.__fullPathArray__.__len__() == 1 else self.__fullPathArray__[1]

    @staticmethod
    def getAppName(request):
        return request.path.split("/")[1]
