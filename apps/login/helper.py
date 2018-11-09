from apps.login.models import EN_LoginCredentials

class LoginHelper():

    def __init__(self,request):
        self.request =  request

    def getUserIdAfterAuthentication(self, username=None, password=None):
        if not username == None or password == None:
            loginCredentials = EN_LoginCredentials.objects.filter(username=username)
            if loginCredentials.exists():
                loginCredentials = loginCredentials[0]
                if loginCredentials.password == password:
                    return loginCredentials.user_id
        return None