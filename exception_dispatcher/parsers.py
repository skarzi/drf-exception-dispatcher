"""Default `django-rest-framework` ``APIException`` parser.

This module implement part of `django-rest-framework` default exception
handler, related to `APIException` parsing into response's data.
Reference:

https://github.com/encode/django-rest-framework/blob/19655edbf782aa1fbdd7f8cd56ff9e0b7786ad3c/rest_framework/views.py#L93

"""
from rest_framework.exceptions import APIException

from exception_dispatcher.types import (
    APIExceptionDetail,
    ContextType,
)


def parse_rest_framework_api_exception(
    exception: APIException,
    context: ContextType,
) -> APIExceptionDetail:
    """Parse ``APIException`` to response's data."""
    if isinstance(exception.detail, (list, dict)):
        return exception.detail
    return {'detail': exception.detail}
