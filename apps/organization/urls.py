from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name="Renders the Organization Groups UI"),

    path(r'OrganizationGroups', views.organizationGroupPage, name="Loads Organization Groups Page"),
    path(r'GetOrganizationGroups', views.getOrganizationGroups, name="AJAX - Return all Organization Groups"),
    path(r'RegisterGroup', views.registerOrgGroup, name="Renders Organization Group Registration Page"),
    path(r'SaveOrganizationGroup', views.saveGroupDetails, name="Save Organization Group Details"),

    path(r'Organizations', views.listOrganizations, name="List All Organization Groups"),
    path(r'GetOrganizations', views.getOrganizations, name="AJAX - List All Organization"),
    path(r'RegisterOrganization', views.registerOrganization, name="Save Organization Details"),
    path(r'SaveOrganization', views.saveOrganizationDetails, name="Save Organization Details"),
    path(r'LoadAreaFromZipcode', views.ajaxLoadAreaFromZipcode, name="Load Area From Zipcode Entered"),

    path(r'Organization', views.getOrganization, name="Get Organization Details"),
    path(r'OrganizationGroup', views.getOrganizationGroup, name="Get Organization Group Details")

]