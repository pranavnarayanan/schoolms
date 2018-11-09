from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Renders Login Page"),
    path(r'Authenticate',views.validateLogin, name="Credentials Authentication"),
    path(r'Reset',views.resetPassword, name="Renders Reset Password Page"),
    path(r'ValidateResetPassword',views.resetPasswordValidate, name="Validate And Reset Password"),
]