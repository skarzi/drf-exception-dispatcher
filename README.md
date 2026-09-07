# Django REST framework exception dispatcher

A Django REST framework
[exception handler](https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling)
built with
[`functools.singledispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch).

## Compatibility

- Python 3.12+
- Django 5.2 LTS, 6.0, or 6.1
- Django REST framework 3.18

## Installation

```console
pip install drf-exception-dispatcher
```

Configure Django REST framework to use the dispatcher:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'exception_dispatcher.handlers.exception_handler',
}
```

The handler supports these optional Django settings:

| Setting | Default | Purpose |
| --- | --- | --- |
| `EXCEPTION_DISPATCHER_SET_ROLLBACK` | `True` | Call DRF's `set_rollback()` before returning an API exception response. |
| `EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER` | `exception_dispatcher.parsers.parse_rest_framework_api_exception` | Convert an exception and context into response data. |
| `EXCEPTION_DISPATCHER_LOGGER_NAME` | `exception_dispatcher` | Log exceptions without a registered dispatcher. |

A custom parser must match this interface:

```python
from rest_framework.exceptions import APIException

from exception_dispatcher.types import APIExceptionDetail, ContextType


def parse_api_exception(
    exception: APIException,
    context: ContextType,
) -> APIExceptionDetail:
    return {'detail': exception.detail}
```

## Custom handlers

Register application-specific exception types on the public dispatcher:

```python
from django.core.exceptions import SuspiciousOperation
from rest_framework import status
from rest_framework.response import Response

from exception_dispatcher.dispatchers import exception_dispatcher
from exception_dispatcher.types import ContextType


@exception_dispatcher.register
def handle_suspicious_operation(
    exception: SuspiciousOperation,
    context: ContextType,
) -> Response:
    return Response(
        {'detail': 'Invalid request.'},
        status=status.HTTP_400_BAD_REQUEST,
    )
```

Built-in handlers cover DRF `APIException`, Django `Http404`, and Django
`PermissionDenied`. Other exceptions are logged and return `None`, allowing
DRF's normal fallback behavior.

## Development

Install and activate [mise](https://mise.jdx.dev/), then bootstrap the pinned
tools, locked dependencies, and Git hooks:

```console
make install-dev
make check
```

Common commands:

| Command | Purpose |
| --- | --- |
| `make help` | List all targets and argument conventions. |
| `make test` | Run the full test suite with branch coverage. |
| `make test -- tests/test_handlers.py -q` | Run targeted tests. |
| `make lint` | Run read-only checks. |
| `make lint-fix` | Format files and run all checks. |
| `make check` | Run lint, tests, and package validation. |
| `make update-deps` | Update Python and Node lockfiles. |
| `make build` | Build the wheel and source distribution. |

Leaf lint and fix targets accept paths after `--`, for example:

```console
make lint-fix-python -- tests/test_handlers.py
```

## Releasing

1. Update the version in `pyproject.toml` and add the release to `CHANGELOG.md`.
2. Run `make check` and `make audit`.
3. Push an unprefixed version tag, such as `1.0.0`, matching the project version.

The release workflow validates the tagged revision before publishing its
artifacts to PyPI.
