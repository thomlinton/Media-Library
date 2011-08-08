from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms.fields import CharField

import os


class PathField(CharField):
    def __init__(self, path, match=None, recursive=False, required=True,
                 widget=None, label=None, initial=None, help_text=None,
                 *args, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        super(PathField, self).__init__(required=required,
            widget=widget, label=label, initial=initial, help_text=help_text,
            *args, **kwargs)
        self.help_text = _(u"Enter a valid path rooted at '%s'" % (self.path))

    def validate(self, value):
        valid_paths = []

        if self.match is not None:
            self.match_re = re.compile(self.match)

        if self.recursive:
            for root, dirs, files in sorted(os.walk(self.path)):
                for d in dirs:
                    if self.match is None or self.match_re.search(d):
                        valid_paths.append( os.path.join(root, d) )
        else:
            try:
                for d in sorted(os.listdir(self.path)):
                    full_path = os.path.join(self.path, d)
                    if os.path.isdir(full_path) and (self.match is None or self.match_re.search(d)):
                        valid_paths.append( full_path )
            except OSError:
                pass

        if value not in valid_paths:
            raise ValidationError(u"Chosen path %s does not exist." % (value))
