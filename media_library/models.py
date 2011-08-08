from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from taggit.managers import TaggableManager
from media_library.db.fields import PathField
from media_library import enums

import datetime


class MediaObject(models.Model):
    """
    The most basic element in the media library.
    """
    created_on = CreationDateTimeField(_('created on'))
    modified_on = ModificationDateTimeField(_('modified on'))

    class Meta:
        abstract = True

class PhysicalMediaObject(MediaObject):
    """
    Represents some on-disk entity that contains media of some variety.
    """
    type = models.PositiveSmallIntegerField(_(u'type'), choices=enums.MEDIA_OBJECT_TYPE_CHOICES)
    path = PathField(_('path'), path=settings.MEDIA_LIBRARY_PATH, recursive=True, unique=True)

    class Meta:
        abstract = True

    tags = TaggableManager()

class Person(MediaObject):
    residence = models.CharField(_('residence'), max_length=128)
    born_on = models.DateField(_('born on'))

    def _get_age(self):
        current_date = datetime.date.today()
        return current_date - self.born_on
    age = property(_get_age)

    class Meta:
        app_label = 'media_library'
        verbose_name = _(u'person')
        verbose_name_plural = _(u'people')

class Artwork(MediaObject):
    type = models.PositiveSmallIntegerField(_(u'type'), choices=enums.ARTWORK_TYPE_CHOICES)
    file = models.FilePathField(_(u'file'), path=settings.MEDIA_LIBRARY_PATH, recursive=True, unique=True)

    class Meta:
        abstract = True

class Device(MediaObject):
    name = models.CharField(_(u'device name'), max_length=128)
    type = models.PositiveSmallIntegerField(_(u'device type'), choices=enums.DEVICE_TYPE_CHOICES)
    manufacturer = models.CharField(_(u'manufacturer'), max_length=128)

    class Meta:
        app_label = 'media_library'
        verbose_name = _(u'device')

class BaseRelease(MediaObject):
    encoding = models.PositiveSmallIntegerField(_(u'encoding'), choices=enums.ENCODING_TYPE_CHOICES)
    bitrate = models.PositiveSmallIntegerField(_(u'bitrate'), choices=enums.BITRATE_CHOICES)
    bitdepth = models.PositiveSmallIntegerField(_(u'bit depth'), choices=enums.BIT_DEPTH_CHOICES)
    sampling_frequency = models.PositiveSmallIntegerField(_(u'sampling frequency'), choices=enums.SAMPLING_FREQUENCY_CHOICES)

    info = models.FilePathField(_(u'info file'), path=settings.MEDIA_LIBRARY_PATH, unique=True, blank=True)

    class Meta:
        abstract = True
