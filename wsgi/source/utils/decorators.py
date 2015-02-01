#@+leo-ver=5-thin
#@+node:lee.20150109093951.3: * @file decorators.py
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.encoding import force_str
from django.shortcuts import resolve_url
from django.conf import settings
from django.utils.six.moves.urllib.parse import urlparse
from django.contrib.auth.views import redirect_to_login
from django.utils.decorators import available_attrs
from functools import wraps
from django.contrib.auth.views import redirect_to_login


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                if request.is_ajax():
                    return HttpResponse(status=401)
                path = request.build_absolute_uri()
                # urlparse chokes on lazy objects in Python 3, force to str
                resolved_login_url = force_str(
                    resolve_url(login_url or settings.LOGIN_URL))
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
                current_scheme, current_netloc = urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme) and
                        (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()

                return redirect_to_login(path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def my_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
#@-leo