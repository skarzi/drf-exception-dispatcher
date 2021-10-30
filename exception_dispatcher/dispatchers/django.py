"""Django's exceptions dispatchers.

This module implement part of `django-rest-framework` default exception
handler, related to `django` `Http404` and `PermissionDenied` exceptions.
Reference:

https://github.com/encode/django-rest-framework/blob/19655edbf782aa1fbdd7f8cd56ff9e0b7786ad3c/rest_framework/views.py#L81

"""
from django.core import exceptions as django_exceptions
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response

from exception_dispatcher.dispatchers.main import exception_dispatcher
from exception_dispatcher.dispatchers.rest_framework import (
    handle_rest_framework_api_exception,
)
from exception_dispatcher.types import ContextType


def handle_django_http404(
    exception: Http404,
    context: ContextType,
) -> Response:
    """Translate django ``Http404`` exception to rest_framework ``NotFound``."""
    return handle_rest_framework_api_exception(
        drf_exceptions.NotFound(),
        context,
    )


def handle_django_permission_denied(
    exception: django_exceptions.PermissionDenied,
    context: ContextType,
) -> Response:
    """Translate django ``PermissionDenied`` exception to rest_framework one."""
    return handle_rest_framework_api_exception(
        drf_exceptions.PermissionDenied(),
        context,
    )


exception_dispatcher.register(Http404, handle_django_http404)
exception_dispatcher.register(
    django_exceptions.PermissionDenied,
    handle_django_permission_denied,
)
