import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a*cbv!iky8m&y-1grn@++k9w4dhxcul-$jra0*cgg+)2&=*(pf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#172.31.25.126   --> RDP ip address
#13.126.211.101  --> AWS EC2 instance public ip address
ALLOWED_HOSTS = [
    '172.31.19.246',
    '13.233.196.178',
    '127.0.0.1',
    'localhost'
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'apps.utilities',
    'apps.sign_up',
    'apps.logout',
    'apps.login',
    'apps.roles',
    'apps.activity',
    'apps.users',
    'apps.home',
    'apps.organization',
    'apps.settings',
    'apps.tasks',
    'apps.messaging',
    'apps.books',
    'apps.school_timings',
    'apps.documents',
    'apps.classes',
    'apps.subjects',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.user_registration.MW_UserRegistration',
    'middleware.authentication.MW_Authentication',
    'middleware.post_login.MW_PostLoginCommon',
    'middleware.role_accessiblity_on_app_authentication.MW_RoleAccessiblityOnAppAuthentication',
]

ROOT_URLCONF = 'schoolms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static'),
            os.path.join(BASE_DIR, 'apps/users/templates'),
            os.path.join(BASE_DIR, 'apps/login/templates'),
            os.path.join(BASE_DIR, 'apps/home/templates'),
            os.path.join(BASE_DIR, 'apps/organization/templates'),
            os.path.join(BASE_DIR, 'apps/roles/templates'),
            os.path.join(BASE_DIR, 'apps/activity/templates'),
            os.path.join(BASE_DIR, 'apps/books/templates'),
            os.path.join(BASE_DIR, 'apps/messaging/templates'),
            os.path.join(BASE_DIR, 'apps/settings/templates'),
            os.path.join(BASE_DIR, 'apps/tasks/templates'),
            os.path.join(BASE_DIR, 'apps/school_timings/templates'),
            os.path.join(BASE_DIR, 'apps/documents/templates'),
            os.path.join(BASE_DIR, 'apps/classes/templates'),
            os.path.join(BASE_DIR, 'apps/subjects/templates'),
            os.path.join(BASE_DIR, 'apps/timetable/templates'),
            os.path.join(BASE_DIR, 'apps/attendance/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'schoolms.wsgi.application'

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#ARAVIND : Below keys wont work (custom middleware for session used instead)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1200 #seconds | 20 mins

STATIC_URL = '/static/' #Change it to http://myshishya.com/static/
STATIC_ROOT = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
#media_configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Email Configuration
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mail4myshishya@gmail.com'
EMAIL_HOST_PASSWORD = 'Shapetheworld#123'
EMAIL_PORT = 587

#ARAVIND : Delete this on production - Placed to disable caching of files
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}