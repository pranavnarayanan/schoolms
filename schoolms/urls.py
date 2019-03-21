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
    path(r'SignUp/', include("apps.sign_up.urls")),
    path(r'Logout/', include("apps.logout.urls")),
    path(r'Login/', include("apps.login.urls")),
    path(r'Roles/', include("apps.roles.urls")),
    path(r'Home/', include("apps.home.urls")),
    path(r'Organization/', include("apps.organization.urls")),
    path(r'Books/', include("apps.books.urls")),
    path(r'Messages/', include("apps.messaging.urls")),
    path(r'Settings/', include("apps.settings.urls")),
    path(r'Tasks/', include("apps.tasks.urls")),
    path(r'SchoolTimings/', include("apps.school_timings.urls")),
    path(r'Documents/', include("apps.documents.urls")),
    path(r'Classes/', include("apps.classes.urls")),
    path(r'Subjects/', include("apps.subjects.urls")),
    path(r'Timetable/', include("apps.timetable.urls")),
    path(r'Attendance/', include("apps.attendance.urls")),
    path(r'Batch/', include("apps.batch.urls")),
    path(r'Announcements/', include("apps.announcements.urls")),
    path(r'Notifications/', include("apps.notifications.urls")),
    path(r'Users/', include("apps.users.urls")),
    path(r'ClassCalendar/', include("apps.class_calendar.urls")),

]


