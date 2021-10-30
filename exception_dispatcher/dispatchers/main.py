"""Generic exception dispatcher directly used by exception handler."""
import functools
import logging

from typing import Optional

from django.conf import settings
from rest_framework.response import Response

from exception_dispatcher.types import ContextType

logger_name = getattr(
    settings,
    'EXCEPTION_DISPATCHER_LOGGER_NAME',
    'exception_dispatcher',
)
logger = logging.getLogger(logger_name)


@functools.singledispatch
def exception_dispatcher(
    exception: Exception,
    context: ContextType,
) -> Optional[Response]:
    """Dispatch exception handling based on ``exception`` type.

    To register new specific exceptions type handler define callable
    decorated with ``exception_dispatcher`` decorator and provide
    type annotation of first argument - `exception`, e.g::

        @exception_dispatcher.register
        def handle_key_error(exception: KeyError, context: ContextType) -> None:
            print(f'handling KeyError: {exception}')
            return None

    If registering via decorator causes any `mypy` errors, simply register
    new dispatchers with direct call of ``register`` method, e.g::

        def handle_key_error(exception: KeyError, context: ContextType) -> None:
            print(f'handling KeyError: {exception}')
            return None


        exception_dispatcher.register(handle_key_error)
        # or when using Python 3.6.x:
        exception_dispatcher.register(KeyError, handle_key_error)

    """
    # log exception, so it can be processed by logging and monitoring services
    logger.exception(exception)
    return None  # noqa: WPS324
