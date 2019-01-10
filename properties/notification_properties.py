#Note : Max len - 50 Chars
class NotificationTypes:
    WELCOME_MESSAGE = "login_welcome_message"
    NEW_ROLE_ADDED = "new_role_added"
    ROLE_APPROVAL_REQUEST_RECEIVED = "role_approval_request_received"


    Message = {
        WELCOME_MESSAGE : "Welcome to WoKidz.com",
        NEW_ROLE_ADDED : "You are assigned with {} role for {} ", # {Teacher} role for {Sabarigiri Residential School}
        ROLE_APPROVAL_REQUEST_RECEIVED : "{} role request received for approval." #{Teacher} role request
    }