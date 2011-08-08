from dev_settings import *
import copy


ROOT_URLCONF = 'media_library.urls.debug'
_INSTALLED_APPS = copy.copy( INSTALLED_APPS )
_INSTALLED_APPS.extend([
    'template_repl',
    'debug_toolbar',
    'django_dowser',
])
INSTALLED_APPS = _INSTALLED_APPS

_MIDDLEWARE_CLASSES = copy.copy( MIDDLEWARE_CLASSES )
_MIDDLEWARE_CLASSES.extend([
    'debug_toolbar.middleware.DebugToolbarMiddleware',
])
MIDDLEWARE_CLASSES = _MIDDLEWARE_CLASSES

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

from local_settings import *
