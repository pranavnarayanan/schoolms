from utils.app_util import AppUtil

'''
    Middleware class for handling all post logins
'''
class MW_PostLoginCommon():

    excluded_apps = [
        "SignUp",
        "Login",
        "Logout",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        appName = AppUtil.getAppName(request)
        if appName not in self.excluded_apps:
            request.session.set_expiry(1200)

        return self.get_response(request)
