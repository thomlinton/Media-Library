from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.db import models

from media_library.models import MediaObject, PhysicalMediaObject, Person, Artwork, Device, BaseRelease
from music import enums


class Label(MediaObject):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name')

    founders = models.ManyToManyField('media_library.Person', verbose_name=_(u'founders'), related_name='labels_founded')
    founded_on = models.DateTimeField(_(u'founded on'))
    location = models.CharField(_(u'location'), max_length=128, blank=True)

    class Meta:
        app_label = 'music'
        verbose_name = _(u'label')

class RecordingStudio(MediaObject):
    name = models.CharField(_(u'name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name')
    location = models.CharField(_(u'location'), max_length=128, blank=True)

    class Meta:
        app_label = 'music'
        verbose_name = _(u'recording studio')

class Artist(Person):
    name = models.CharField(_('first name'), max_length=128)
    slug = AutoSlugField(_('slug'), populate_from='name')

    url = models.URLField(_(u'url'), verify_exists=True, null=True, blank=True)
    bio = models.TextField(_(u'bio'), blank=True)

    labels = models.ManyToManyField('music.Label')
    members = models.ManyToManyField('self')
    related_artists = models.ManyToManyField('self')

    class Meta:
        app_label = 'music'
        verbose_name = _(u'artist')

class Edition(MediaObject):
    title = models.CharField(_(u'title'), max_length=128)
    media_type = models.PositiveSmallIntegerField(_(u'media'), choices=enums.MEDIA_TYPE_CHOICES)
    released_on = models.DateTimeField(_(u'released on'))
    label = models.ForeignKey('music.Label')
    url = models.URLField(_(u'url'), verify_exists=True, null=True, blank=True)

class Album(PhysicalMediaObject):
    title = models.CharField(_(u'title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title')
    description = models.TextField(_(u'description'), blank=True)

    artist = models.ForeignKey('music.Artist')
    released_on = models.DateTimeField(_(u'released on'))
    recorded_at = models.ForeignKey('music.RecordingStudio', null=True, blank=True)
    engineered_by = models.ManyToManyField('media_library.Person', related_name='albums_engineered')
    mastered_by = models.ManyToManyField('media_library.Person', related_name='albums_mastered')

    class Meta:
        app_label = 'music'
        verbose_name = _(u'album')

class Track(PhysicalMediaObject):
    edition = models.ForeignKey('music.Edition')
    track_number = models.PositiveSmallIntegerField(_(u'track number'))
    title = models.CharField(_(u'title'), max_length=128)

    class Meta:
        app_label = 'music'
        verbose_name = _(u'track')

class AlbumArtwork(Artwork):
    album = models.ForeignKey('music.Album')

    class Meta:
        app_label = 'music'
        verbose_name = _(u'album artwork')
        verbose_name_plural = _(u'album artwork')

class Collection(PhysicalMediaObject):
    title = models.CharField(_(u'title'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='title')
    albums = models.ManyToManyField('music.Album', related_name='in_collections')

    class Meta:
        app_label = 'music'
        verbose_name = _(u'collection')

class CollectionArtwork(Artwork):
    collection = models.ForeignKey('music.Collection')

    class Meta:
        app_label = 'music'
        verbose_name = _(u'collection artwork')
        verbose_name_plural = _(u'collection artwork')

class Release(BaseRelease):
    edition = models.ForeignKey('music.Edition')

    class Meta:
        app_label = 'music'
        verbose_name = _(u'release')

class SignalPathElement(MediaObject):
    device = models.ForeignKey('media_library.Device')
    ordering = models.PositiveSmallIntegerField(_(u'ordering'), default=0)

    class Meta:
        app_label = 'music'
        verbose_name = _(u'signal path element')

class Recording(PhysicalMediaObject):
    edition = models.ForeignKey('music.Edition')
