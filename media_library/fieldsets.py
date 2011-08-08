from django.utils.translation import ugettext_lazy as _


MEDIA_OBJECT_ADMIN_FIELDSETS = (
    # (_(u'Metadata'), {
    #         'fields':('created_on', 'modified_on',),
    #         'classes':('collapse',),
    #         }),
)

PHYSICAL_MEDIA_OBJECT_ADMIN_FIELDSETS = (
    (_(u'Media information'), {
            'fields':('path',)
            }),
) + MEDIA_OBJECT_ADMIN_FIELDSETS
