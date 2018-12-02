from django.urls import path
from . import views

urlpatterns = [
    path(r'',views.index, name="Index"),
    path(r'SavePrimaryPageDetails',views.savePrimaryPageDetails, name="Save Primary Page Details"),

    path(r'LoadContactPage',views.loadContactPage, name="Load Contact Page"),
    path(r'SaveContactPageDetails',views.saveContactPageDetails, name="Save Contact Page Details"),

    path(r'LoadPermanentAddressPage',views.loadPermanentAddressPage, name="Load Permanent Address Page"),
    path(r'SavePermanentAddressPageDetails',views.savePermanentAddressPageDetails, name="Save Permanent Address Page Details"),

    path(r'LoadCurrentAddressPage',views.loadCurrentAddressPage, name="Load Current Address Page"),
    path(r'SaveCurrentAddressPageDetails',views.saveCurrentAddressPageDetails, name="Save Current Address Page Details"),

    path(r'LoadCredentialsPage',views.loadCredentialsPage, name="Load Credentials Page"),
    path(r'SaveCredentialPageDetails',views.saveCredentialPageDetails, name="Save Credential Page Details"),
    
    path(r'ActivateAccount',views.activateAccount, name="Activates account | Called from email send to user"),
]