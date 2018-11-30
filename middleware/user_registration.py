from utils.app_util import AppUtil

'''
    Middleware class for User registration alone 
'''
class MW_UserRegistration():

    permitted_apps = [
        "UserRegistration"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        appName = AppUtil.getAppName(request)
        if appName in self.permitted_apps:
            request.session.set_expiry(6000)

        return self.get_response(request)
