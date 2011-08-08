from django.forms.fields import ChoiceField
import os


class PathField(ChoiceField):
    def __init__(self, path, match=None, recursive=False, required=True,
                 widget=None, label=None, initial=None, help_text=None,
                 *args, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        super(PathField, self).__init__(choices=(), required=required,
            widget=widget, label=label, initial=initial, help_text=help_text,
            *args, **kwargs)

        if self.required:
            self.choices = []
        else:
            self.choices = [("", "---------")]

        if self.match is not None:
            self.match_re = re.compile(self.match)

        if recursive:
            for root, dirs, files in sorted(os.walk(self.path)):
                for d in dirs:
                    if self.match is None or self.match_re.search(f):
                        f = os.path.join(root, f)
                        self.choices.append((f, f.replace(path, "", 1)))
        else:
            try:
                for d in sorted(os.listdir(self.path)):
                    full_path = os.path.join(self.path, d)
                    if os.path.isdir(full_path) and (self.match is None or self.match_re.search(d)):
                        self.choices.append((full_path, d))
            except OSError:
                pass

        self.widget.choices = self.choices

class PathField(Field):
    description = _("File path")

    def __init__(self, verbose_name=None, name=None, path='', match=None, recursive=False, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        kwargs['max_length'] = kwargs.get('max_length', 255)
        Field.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'path': self.path,
            'match': self.match,
            'recursive': self.recursive,
            'form_class': PathField,
        }
        defaults.update(kwargs)
        return super(PathField, self).formfield(**defaults)

    def get_internal_type(self):
        return "PathField"
