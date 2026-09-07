"""Default Django REST framework ``APIException`` parser.

This module implements the part of Django REST framework's default exception
handler related to parsing ``APIException`` instances into response data.
Reference:

https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

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
