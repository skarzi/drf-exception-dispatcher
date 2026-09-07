"""Frequently used types' aliases."""

from collections.abc import MutableMapping
from typing import Any

ContextType = MutableMapping[str, Any]
APIExceptionDetail = str | list[Any] | dict[str, Any]
