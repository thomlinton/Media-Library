from django.contrib import admin

from media_library.admin import MediaObjectAdmin, PhysicalMediaObjectAdmin
from torrents.fieldsets import (
    TRACKER_ADMIN_FIELDSETS, TORRENT_ADMIN_FIELDSETS)
from torrents.models import (
    Tracker, Torrent)


class TrackerAdmin(MediaObjectAdmin):
    list_display = ('name', 'url', 'is_private', 'torrent_directory',) + MediaObjectAdmin.list_display
    list_filter = ('is_private',) + MediaObjectAdmin.list_filter
    search_fields = ('name',)
    readonly_fields = ('torrent_directory',)

    fieldsets = TRACKER_ADMIN_FIELDSETS

class TorrentAdmin(PhysicalMediaObjectAdmin):
    list_display = ('tracker',) + PhysicalMediaObjectAdmin.list_display
    list_filter = ('tracker',) + PhysicalMediaObjectAdmin.list_filter

    fieldsets = TORRENT_ADMIN_FIELDSETS

admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Torrent, TorrentAdmin)
