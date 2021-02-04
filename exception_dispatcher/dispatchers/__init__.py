"""Register all exception dispatcher handlers."""
from exception_dispatcher.dispatchers import (  # noqa: F401
    django,
    rest_framework,
)
from exception_dispatcher.dispatchers.main import exception_dispatcher

__all__ = ('exception_dispatcher',)
