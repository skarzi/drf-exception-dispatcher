from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions as rest_exceptions

from exception_dispatcher.dispatchers import django as handlers

API_EXCEPTION_HANDLER_PATH = (
    'exception_dispatcher.dispatchers.django'
    + '.handle_rest_framework_api_exception'
)


def test_handle_django_http404(mocker):
    """Ensure `rest_framework` handler for ``NotFound`` is called."""
    drf_handler_mock = mocker.patch(API_EXCEPTION_HANDLER_PATH)

    handlers.handle_django_http404(Http404(), {})

    drf_handler_mock.assert_called_once()
    exception, context = drf_handler_mock.call_args[0]
    assert not context
    assert isinstance(exception, rest_exceptions.NotFound)


def test_handle_django_permission_denied(mocker):
    """Ensure `rest_framework` handler for ``PermissionDenied`` is called."""
    drf_handler_mock = mocker.patch(API_EXCEPTION_HANDLER_PATH)

    handlers.handle_django_permission_denied(PermissionDenied(), {})

    drf_handler_mock.assert_called_once()
    exception, context = drf_handler_mock.call_args[0]
    assert not context
    assert isinstance(exception, rest_exceptions.PermissionDenied)
