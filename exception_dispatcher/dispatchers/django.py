"""Django exception dispatchers.

This module implements the part of Django REST framework's default exception
handler related to Django's ``Http404`` and ``PermissionDenied`` exceptions.
Reference:

https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

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
        drf_exceptions.NotFound(*exception.args),
        context,
    )


def handle_django_permission_denied(
    exception: django_exceptions.PermissionDenied,
    context: ContextType,
) -> Response:
    """Translate django ``PermissionDenied`` exception to rest_framework one."""
    return handle_rest_framework_api_exception(
        drf_exceptions.PermissionDenied(*exception.args),
        context,
    )


exception_dispatcher.register(Http404, handle_django_http404)
exception_dispatcher.register(
    django_exceptions.PermissionDenied,
    handle_django_permission_denied,
)
