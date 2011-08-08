from django.utils.translation import ugettext_lazy as _


MEDIA_TYPE_CD = 1
MEDIA_TYPE_DVD = 2
MEDIA_TYPE_VINYL = 3
MEDIA_TYPE_SOUNDBOARD = 4
MEDIA_TYPE_SACD = 5
MEDIA_TYPE_DAT = 6
MEDIA_TYPE_CASSETTE = 7
MEDIA_TYPE_WEB = 8
MEDIA_TYPE_BD = 9
MEDIA_TYPE_CHOICES = (
    (MEDIA_TYPE_CD,_(u'CD')),
    (MEDIA_TYPE_DVD,_(u'DVD')),
    (MEDIA_TYPE_VINYL,_(u'Vinyl')),
    (MEDIA_TYPE_SOUNDBOARD,_(u'Soundboard')),
    (MEDIA_TYPE_SACD,_(u'SACD')),
    (MEDIA_TYPE_DAT,_(u'DAT')),
    (MEDIA_TYPE_CASSETTE,_(u'Cassette')),
    (MEDIA_TYPE_BD,_(u'Blu-ray')),
)
