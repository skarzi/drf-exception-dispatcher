"""django-rest-framework's exceptions dispatchers.

This module implement part of `django-rest-framework` default exception
handler, related to its `APIException`.
Reference:

https://github.com/encode/django-rest-framework/blob/19655edbf782aa1fbdd7f8cd56ff9e0b7786ad3c/rest_framework/views.py#L86

"""
import functools

from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import set_rollback

from exception_dispatcher.dispatchers.main import exception_dispatcher
from exception_dispatcher.types import ContextType


@functools.lru_cache(maxsize=1)
def get_api_exception_parser():
    """Get callable object used to parse ``APIException`` based on settings."""
    parser_path = getattr(
        settings,
        'EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER',
        'exception_dispatcher.parsers.parse_rest_framework_api_exception',
    )
    try:
        return import_string(parser_path)
    except ImportError as exc:
        message = 'Could not import "{0}" for setting "{1}". {2}: {3}.'.format(
            parser_path,
            'EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER',
            exc.__class__.__name__,
            exc,
        )
        raise ImportError(message)


def handle_rest_framework_api_exception(
    exception: APIException,
    context: ContextType,
) -> Response:
    """Handle all ``APIException`` subclasses' instances."""
    headers = {}
    auth_header = getattr(exception, 'auth_header', None)
    if auth_header:
        headers['WWW-Authenticate'] = auth_header
    wait_value = getattr(exception, 'wait', None)
    if wait_value:
        headers['Retry-After'] = str(wait_value)
    response_data = get_api_exception_parser()(exception, context)
    if getattr(settings, 'EXCEPTION_DISPATCHER_SET_ROLLBACK', True):
        set_rollback()
    return Response(
        response_data,
        status=exception.status_code,
        headers=headers,
    )


exception_dispatcher.register(APIException, handle_rest_framework_api_exception)
