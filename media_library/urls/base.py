from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()


handler500 = 'media_library.views.server_error'
urlpatterns = patterns('',
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^music/', include('media_library.music.urls')),
    url(r'^torrents/', include('media_library.torrents.urls')),
)
