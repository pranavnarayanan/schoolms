"""schoolms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('SignUp/', include("apps.sign_up.urls")),
    path('Logout/', include("apps.logout.urls")),
    path('Login/', include("apps.login.urls")),
    path('Notification/', include("apps.activity.urls")),
    path('Roles/', include("apps.roles.urls")),
    path('Home/', include("apps.home.urls")),
    path('Organization/', include("apps.organization.urls")),

]

