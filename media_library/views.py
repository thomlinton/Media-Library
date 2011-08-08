from django.views.defaults import page_not_found, server_error
from django.conf.urls.defaults import *


def server_error(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, RequestContext, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    ctxt = RequestContext(request,{})
    return HttpResponseServerError(t.render(ctxt))
