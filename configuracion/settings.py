# Django settings for programacion_docente project.
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Gerardo Linares', 'gerardevil@gmail.com'), ('Jesus Gomez', 'jesus.igp009@gmail.com'))

MANAGERS = ADMINS

if not ('test' in sys.argv):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'dbprogramacion',             
            'USER': 'devlabsadmin',
            'PASSWORD': 'devlabs2013',
            'HOST': 'devlabsdb.webfactional.com', 
            'PORT': ''
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'testdb',             
            'USER': 'root',
            'PASSWORD': 'testdb2013@devlabsdb',
            'HOST': '108.168.149.236', 
            'PORT': '27511'
        }
    }
    """ Speeding Up AuthenticationMiddleware """
    PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    )

#Profile definitios for get_profile( ) function usage
AUTH_PROFILE_MODULE = 'principal.Usuario'

#Login URL for login_required usage
LOGIN_URL = '/login'

#Logout URL for login_required usage
LOGIN_OUT = '/logout'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Caracas'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ve'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

'''
STATIC_ROOT is only used if a call to 
the 'manage.py collectstatic' manangement command is performed

[Only used for deploy process on server]

'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR,'..', '..', '..', 'static').replace('\\','/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATICFILES_DIRS = (
    ('js', os.path.join(BASE_DIR, '..', 'static', 'js').replace('\\','/')),
    ('css', os.path.join(BASE_DIR, '..', 'static', 'css').replace('\\','/')),
    ('img', os.path.join(BASE_DIR, '..', 'static', 'img').replace('\\','/')),
    ('logos', os.path.join(BASE_DIR, '..', 'static', 'logos').replace('\\','/')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2heu7&0@!phd)wy^apsp7gujg-k#m%uol!jx4=-laeto4@=5f&'

# Using heaven key for reset process
HEAVEN_KEY = '$*H@E-&%/A12$%&s(dfVEN(df-o!@KE!-Y*$'

# Using 24hrs like timeot period for reset process
RESET_PASSWORD_TIMEOUT = 24*60*60

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #Non default middleware
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'configuracion.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'configuracion.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    #Non Django App: Team Apps
    'principal'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ejemplo@gmail.com'
EMAIL_HOST_PASSWORD = '1234'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
