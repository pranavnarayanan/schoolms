from apps.login.models import EN_LoginCredentials
from properties.session_properties import SessionProperties

'''
    # Login Helper Class 
'''
class LoginHelper():

    def __init__(self,request):
        self.request =  request

    '''    
    # Autherize and Authenticate the username and password entered
    '''
    def getUserIdAfterAuthentication(self, username=None, password=None):
        if not username == None or password == None:
            loginCredentials = EN_LoginCredentials.objects.filter(username=username)
            if loginCredentials.exists():
                loginCredentials = loginCredentials[0]
                if loginCredentials.password == password:
                    self.user = loginCredentials.user
                    return loginCredentials.user_id
        return None

    '''    
    # Set Static UI Data
    '''
    def setStaticUIData(self):
        self.request.session[SessionProperties.USER_NAME_KEY] = self.user.name
        self.request.session[SessionProperties.USER_PRODUCT_ID_KEY] = self.user.product_id
        self.request.session[SessionProperties.USER_DP_KEY] = self.user.display_picture
        self.request.session[SessionProperties.USER_ONLINE_KEY] = self.user.en_logincredentials.is_online
        self.request.session[SessionProperties.USER_GENDER_KEY] = self.user.gender.code

    '''    
    # Set Active Role Of User
    '''
    def setActiveRole(self):
        self.request.session[SessionProperties.USER_ACTIVE_ROLE_KEY] = None


    '''    
    # Update Online Status and logged in time
    '''
    def updateOnlineStatusAndLoggedInTime(self):
        import datetime
        lc = self.user.en_logincredentials
        lc.is_online = True
        lc.last_logged_in_time = lc.current_logged_in_time
        lc.current_logged_in_time = datetime.datetime.now()
        lc.save()

