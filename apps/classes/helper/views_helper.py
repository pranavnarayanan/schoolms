from properties.session_properties import SessionProperties

class ViewsHelper:

    def __init__(self,request):
        self.user_id = request.session[SessionProperties.USER_ID_KEY]
