from base_settings import *
import copy


DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPOGATE_EXCEPTIONS = DEBUG

ROOT_URLCONF = 'media_library.urls.production'

# Celery settings
CELERY_QUEUES = {
    "media_library": {
        "exchange": "media_library",
        "exchange_type": "direct",
        "binding_key": "default",
    },
    "media_library.music": {
        "exchange": "media_library",
        "exchange_type": "direct",
        "binding_key": "default",
    },
}
CELERY_DEFAULT_QUEUE = "media_library"
CELERY_DEFAULT_EXCHANGE = "media_library"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
## Celerybeat settings
CELERYBEAT_SCHEDULE = {
    # Executes every day at 7:00 P.M
#     "reports.centralrepository.generate_report": {
#         "task": "reports.centralrepository.tasks.generate_report",
#         "schedule": crontab(day_of_week="mon-fri", hour=19, minute=0),
#     },
}

# Compressor settings
COMPRESS_OFFLINE = True
COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.datauri.CssDataUriFilter',
    ]
COMPRESS_DATA_URI_MIN_SIZE = 16384 # 16KB
COMPRESS_OFFLINE = True
# COMPRESS_OFFLINE_TIMEOUT = 60 * 60 * 24 * 7
# COMPRESS_OFFLINE_CONTEXT = {}


from local_settings import *
