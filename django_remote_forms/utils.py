from django.http import QueryDict
from django.utils.encoding import force_unicode
from django.utils.functional import Promise


def resolve_promise(o):
    if isinstance(o, QueryDict):
        o = dict(o)

    if isinstance(o, dict):
        for k, v in o.items():
            o[k] = resolve_promise(v)
    elif isinstance(o, (list, tuple)):
        o = [resolve_promise(x) for x in o]
    elif isinstance(o, Promise):
        try:
            o = force_unicode(o)
        except:
            # Item could be a lazy tuple or list
            try:
                o = [resolve_promise(x) for x in o]
            except:
                raise Exception('Unable to resolve lazy object %s' % o)
    elif callable(o):
        o = o()

    return o
