from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from media_library.urls import base


urlpatterns = base.urlpatterns + staticfiles_urlpatterns()

