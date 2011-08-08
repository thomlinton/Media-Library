from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import Field
from media_library import forms


class PathField(Field):
    description = _("Path")

    def __init__(self, verbose_name=None, name=None, path='', match=None, recursive=False, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        kwargs['max_length'] = kwargs.get('max_length', 255)
        Field.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'path': self.path,
            'match': self.match,
            'recursive': self.recursive,
            'form_class': forms.PathField,
        }
        defaults.update(kwargs)
        return super(PathField, self).formfield(**defaults)

    def get_internal_type(self):
        return "PathField"

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
