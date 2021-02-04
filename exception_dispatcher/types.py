"""Frequently used types' aliases."""
from typing import (
    Any,
    Dict,
    List,
    MutableMapping,
    Union,
)

ContextType = MutableMapping[str, Any]
APIExceptionDetail = Union[str, List[Any], Dict[str, Any]]
