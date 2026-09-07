"""`django-rest-framework` exception handler definition.

Refer to `django-rest-framework` docs about custom exception handler to see how
to use ``exception_handler`` defined in this module.

Reference:
https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

"""

from rest_framework.response import Response

from exception_dispatcher.dispatchers import exception_dispatcher
from exception_dispatcher.types import ContextType


def exception_handler(
    exception: Exception,
    context: ContextType,
) -> Response | None:
    """`django-rest-framework` exception handler.

    Following exception handler is built with ``functools.singledispatch``
    https://docs.python.org/3/library/functools.html#functools.singledispatch
    To add new handler for any ``Exception`` subclass refer to e.g.
    `exception_dispatcher.dispatchers.django`.

    """
    return exception_dispatcher(exception, context)
