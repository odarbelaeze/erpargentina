# Django settings for erpargentina project.
# coding=utf-8

from os import path, pardir

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Oscar David Arbeláez', 'odarbelaeze@gmail.com'),
)

PROJECT_ROOT = path.dirname(path.abspath(__file__))

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openscience_erpargentina',
        'USER': 'openscience',
        'PASSWORD': 'elToby29',
        'HOST': 'postgresql1.alwaysdata.com',
        'PORT': '',
    }
}

TIME_ZONE = 'America/Buenos_Aires'

LANGUAGE_CODE = 'es-co'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_ROOT = path.join(PROJECT_ROOT, pardir, 'public', 'site_media')

MEDIA_URL = '/media/'

STATIC_ROOT = path.join(PROJECT_ROOT, pardir, 'public', 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    path.join(PROJECT_ROOT, pardir, 'resourses', 'bootstrap'),
    path.join(PROJECT_ROOT, pardir, 'resourses', 'jquery'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9zbp6lndfazv(+smog@)h@$3_(su$k^w3t&amp;j&amp;4@01amml=eqqi'

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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'erpargentina.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'erpargentina.wsgi.application'

TEMPLATE_DIRS = (
    path.join(PROJECT_ROOT, pardir, 'resourses', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',
    'stocks',
    'humanresources',
    'clients',
)

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

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
