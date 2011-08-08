from django.contrib import admin

from music.models import (
    Label, RecordingStudio, Artist, Edition, Album, Track, AlbumArtwork, 
    Collection, CollectionArtwork, Release, SignalPathElement, Recording
)

admin.site.register(Label)
admin.site.register(RecordingStudio)
admin.site.register(Artist)
admin.site.register(Edition)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(AlbumArtwork)
admin.site.register(Collection)
admin.site.register(CollectionArtwork)
admin.site.register(Release)
admin.site.register(SignalPathElement)
admin.site.register(Recording)
