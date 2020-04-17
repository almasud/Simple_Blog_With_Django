""" 
    We declare our custom function here.
"""
from functools import wraps
from urllib.parse import urlparse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from time import strftime
from django.contrib import messages


def user_passes_test(test_func, login_url=None, redirect_field_name=None,
	message=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.error(request, message)
            else:
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def login_required(function=None, redirect_field_name="next", login_url=None, 
    message="You must login to access!"):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


import os

# Post uploaded directory path
def post_directory_path(instance, filename):
    file_name, file_extension = os.path.splitext(filename)
    # file will be uploaded to MEDIA_ROOT/user_<id>/blog_post/user_<id>_post_<Year><Month><Day><Second>
    return ('{0}/blog/user_{1}_' + strftime('%Y%m%d%s') + '{2}').format(instance.author, instance.author.id, file_extension)

# Profile uploaded directory path
def profile_directory_path(instance, filename):
    file_name, file_extension = os.path.splitext(filename)
    # file will be uploaded to MEDIA_ROOT/user_<id>/account_userprofile/user_<id>__userprofile_<id>_<Year><Month><Day><Second>
    return ('{0}/account/user_{1}_' + strftime('%Y%m%d%s') + '{2}').format(instance.user, instance.user.id, file_extension)



