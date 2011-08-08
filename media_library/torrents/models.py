from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

from django_extensions.db.fields import AutoSlugField
from media_library.models import MediaObject, PhysicalMediaObject
from media_library.db.fields import PathField
from torrents import enums


class Tracker(MediaObject):
    name = models.CharField(_(u'name'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='name')

    url = models.URLField(_(u'tracker url'))
    is_private = models.BooleanField(_(u'is private'))
    user = models.CharField(_(u'user'), max_length=64, blank=True)
    passcode = models.CharField(_(u'passcode'), max_length=64, blank=True)
    torrent_directory = PathField(_(u'torrent directory'), path=settings.TORRENT_PATH, recursive=True)

    class Meta:
        app_label = 'torrents'
        verbose_name = _(u'tracker')

    def __unicode__(self):
        return self.name

class Torrent(PhysicalMediaObject):
    tracker = models.ForeignKey('torrents.Tracker')

    class Meta:
        app_label = 'torrents'
        verbose_name = _(u'torrent')

    def __unicode__(self):
        return u'Torrent %s on tracker %s' % (self.path, self.tracker.name)
