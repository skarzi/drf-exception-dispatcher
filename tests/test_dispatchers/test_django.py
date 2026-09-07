"""Tests for Django exception translation."""

from django.core.exceptions import PermissionDenied
from django.http import Http404
from pytest_mock import MockerFixture
from rest_framework import exceptions as rest_exceptions

from exception_dispatcher.dispatchers import django as handlers

API_EXCEPTION_HANDLER_PATH = (
    'exception_dispatcher.dispatchers.django.'
    'handle_rest_framework_api_exception'
)


def test_handle_django_http404(mocker: MockerFixture) -> None:
    """Ensure `rest_framework` handler for ``NotFound`` is called."""
    drf_handler_mock = mocker.patch(API_EXCEPTION_HANDLER_PATH)
    detail = 'Missing object'
    code = 'missing_object'

    handlers.handle_django_http404(Http404(detail, code), {})

    drf_handler_mock.assert_called_once()
    exception, context = drf_handler_mock.call_args[0]
    assert not context
    assert isinstance(exception, rest_exceptions.NotFound)
    assert exception.detail == rest_exceptions.ErrorDetail(detail, code)


def test_handle_django_permission_denied(mocker: MockerFixture) -> None:
    """Ensure `rest_framework` handler for ``PermissionDenied`` is called."""
    drf_handler_mock = mocker.patch(API_EXCEPTION_HANDLER_PATH)
    detail = 'Access denied'
    code = 'access_denied'

    handlers.handle_django_permission_denied(
        PermissionDenied(detail, code),
        {},
    )

    drf_handler_mock.assert_called_once()
    exception, context = drf_handler_mock.call_args[0]
    assert not context
    assert isinstance(exception, rest_exceptions.PermissionDenied)
    assert exception.detail == rest_exceptions.ErrorDetail(detail, code)
