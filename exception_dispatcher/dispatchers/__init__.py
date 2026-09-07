"""Register all exception dispatcher handlers."""

from exception_dispatcher.dispatchers import (
    django,
    rest_framework,
)
from exception_dispatcher.dispatchers.main import exception_dispatcher

__all__ = ('exception_dispatcher',)
