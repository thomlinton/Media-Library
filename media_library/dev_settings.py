from base_settings import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPOGATE_EXCEPTIONS = DEBUG

ROOT_URLCONF = 'media_library.urls.development'

# Compressor settings
COMPRESS_DEBUG_TOGGLE = 'disable-compressor'

# Celery settings
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


from local_settings import *
