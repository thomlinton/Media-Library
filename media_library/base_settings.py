# -*- coding: utf-8 -*-
gettext = lambda s: s

from celery.schedules import crontab
import djcelery; djcelery.setup_loader()
import os, os.path


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_ETAGS = True
USE_I18N = True
USE_L10N = True

ugettext = lambda s: s
LANGUAGES = (
    ('en',ugettext('English')),
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.csrf",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
)

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

INSTALLED_APPS = [
    ### Django ###
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    ### Django Libs ###
    'django_extensions',
    'django_filters',
    'compressor',
    'reversion',
    'djcelery',
    'haystack',
    'taggit',
    'south',

    ### Project Apps ###
    'media_library',
    'music',
    'torrents',
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'media_libary': {
            'handlers': ['console', 'mail_admins'], 
            'level': 'INFO',
        }
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'propagate': False,
            'level': 'ERROR',
        },
        'media_library': {
            'handlers': ['console', 'mail_admins'],
            'propagate': False,
            'level': 'INFO'
        },
    }
}

# Base path info
BASE_PATH = os.path.dirname(__file__)
PROJECT_ROOT = BASE_PATH

# Template & rendering settings
TEMPLATE_DIRS = (
    os.path.join( BASE_PATH, 'templates' ),
)
FIXTURE_DIRS = (
    os.path.join( BASE_PATH, 'fixtures' ),
)

# Staff & development ACL/whitelist
INTERNAL_IPS = (
   '127.0.0.1',
)

# Media mount points
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Filesystem data roots & mounts
STATIC_ROOT = os.path.join( BASE_PATH, '../static/' )
MEDIA_ROOT = os.path.join( BASE_PATH, '../media/' )

# Session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Message settings
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# Haystack settings
HAYSTACK_SITECONF = 'media_library.search_sites'
HAYSTACK_DEFAULT_OPERATOR = 'OR'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_XAPIAN_PATH = os.path.join( BASE_PATH, 'search_index' )

# Celery settings
CELERY_SEND_TASK_ERROR_EMAILS = True
## Celeryd settings
CELERYD_CONCURRENCY = 1
## Result store settings
CELERY_IGNORE_RESULT = True
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "sqlite:///%s" % (os.path.join( BASE_PATH, 'celery.db' ))

## Celerybeat settings
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Staticfiles settings
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Email/correspondence settings
SERVER_EMAIL = 'media-library@ninjawirel.us'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
EMAIL_SUBJECT_PREFIX = "[Media Library] "

# Compatibility settings
CACHE_BACKEND = 'dummy://'
