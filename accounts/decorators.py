from functools import wraps
from django.core.exceptions import PermissionDenied


def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        raise PermissionDenied

    return wrap


def visitante_required(function):
    def wrap(request, *args, **kwargs):
        raise PermissionDenied

    return wrap
