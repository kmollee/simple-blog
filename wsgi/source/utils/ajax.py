#@+leo-ver=5-thin
#@+node:lee.20150101103558.96: * @file ajax.py
import json
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateformat import format
from django.conf import settings


def login_required_ajax(function=None):

    # ensure the user is authenticated to access a certain ajax view
    # otherwise return a json object notifying the user access is denied
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                now = format(timezone.now(), 'U')
                # delete all existing kwargs
                # as they cause HttpResponse to throw TypeError: __init__() got an unexpected keyword argument
                kwargs = {'content_type': 'application/json'}
                response = {
                    'status': '401',
                    'message': 'Unknown authentication scheme',
                    'timestamp': now,
                    'errorcode': settings.API_ERROR_AUTHENTICATION
                }
                return HttpResponse(status=401, content=json.dumps(response), **kwargs)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)
#@-leo
