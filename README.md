# Django REST framework exception dispatcher

[`django-rest-framework`](https://github.com/encode/django-rest-framework)
[exception handler](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling)
build with
[`funtools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch).

## Installation

To use `drf-exception-dispatcher` simply install it with your package manager,
e.g. to with `pip`:

```bash
pip install drf-exception-dispatcher
```

Then simply use `exception_dispatcher.handlers.exception_handler` (
or your own exception handler built on `exception_dispatcher`) in Django's
settings `REST_FRAMEWORK` section:

```python
REST_FRAMEWORK = {
  # ...
  'EXCEPTION_HANDLER': 'exception_dispatcher.handlers.exception_handler',
  # ...
}
```

### Configuration

Following settings are present to make default `exception_dispatcher` handler
configurable:

+ `EXCEPTION_DISPATCHER_SET_ROLLBACK` (defaults to `True`) - indicate if
  [`set_rollback`](https://github.com/encode/django-rest-framework/blob/71e6c30034a1dd35a39ca74f86c371713e762c79/rest_framework/views.py#L65)
  should be called before returning response from exception handler
+ `EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER` (defaults to
  `exception_dispatcher.parsers.parse_rest_framework_api_exception'`) - import
  path to callable that is used to translate occurred `exception` to response
  data

## Usage

To add new handlers to `exception_dispatchers` simply use dispatcher's
`register()` method, e.g. to add handler of `SuspiciousOperation` exceptions:

```python
from exception_dispatcher.dispatchers import exception_dispatcher
from exception_dispatcher.types import ContextType
from rest_framework.response import Response


@exception_dispatcher.register
def handler_suspicious_operation(
    exception: SuspiciousOperation,
    context: ContextType,
) -> Response | None:
    """Handle Django's `SuspiciousOperation` exceptions."""
    # custom ``exception` handler logic goes here
    return None
```
