from django.utils.translation import ugettext_lazy as _
from media_library.fieldsets import (
    PHYSICAL_MEDIA_OBJECT_ADMIN_FIELDSETS)


TRACKER_ADMIN_FIELDSETS = (
    (_(u'Tracker information'), {
            'fields':('name', 'url', 'is_private', 'torrent_directory',),
            }),
    (_(u'User information'), {
            'fields':('user', 'passcode',),
            'classes':('collapse',),
            }),
)

TORRENT_ADMIN_FIELDSETS = (
    (_(u'Torrent information'), {
            'fields':('tracker',),
            }),
) + PHYSICAL_MEDIA_OBJECT_ADMIN_FIELDSETS
