from django.contrib import admin

from media_library.fieldsets import PHYSICAL_MEDIA_OBJECT_ADMIN_FIELDSETS
from media_library.models import (
    PhysicalMediaObject, Person, Device)


class MediaObjectAdmin(admin.ModelAdmin):
    list_display = ('created_on',)
    list_filter = ('created_on',)

    fieldsets = PHYSICAL_MEDIA_OBJECT_ADMIN_FIELDSETS

class PhysicalMediaObjectAdmin(MediaObjectAdmin):
    list_display = ('path',) + MediaObjectAdmin.list_display
    list_display_links = ('path',)
    search_fields = ('path',)
    readonly_fields = ('path',)

    fieldsets = PHYSICAL_MEDIA_OBJECT_ADMIN_FIELDSETS

admin.site.register(Person)
admin.site.register(Device)
