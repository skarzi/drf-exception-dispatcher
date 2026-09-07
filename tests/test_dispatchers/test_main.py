"""Tests for the generic exception dispatcher."""

import logging

import pytest

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import APIException

from exception_dispatcher.dispatchers import exception_dispatcher
from exception_dispatcher.dispatchers.django import (
    handle_django_http404,
    handle_django_permission_denied,
)
from exception_dispatcher.dispatchers.rest_framework import (
    handle_rest_framework_api_exception,
)


def test_builtin_dispatchers_are_registered() -> None:
    """Ensure importing the public dispatcher registers built-in handlers."""
    assert exception_dispatcher.dispatch(Http404) is handle_django_http404
    assert (
        exception_dispatcher.dispatch(PermissionDenied)
        is handle_django_permission_denied
    )
    assert (
        exception_dispatcher.dispatch(APIException)
        is handle_rest_framework_api_exception
    )


def test_returned_value() -> None:
    """Ensure ``None`` is returned."""
    assert exception_dispatcher(ValueError(), {}) is None


def test_logger(caplog: pytest.LogCaptureFixture) -> None:
    """Ensure supplied exception and traceback are logged."""
    message = 'Delayed failure.'
    exception = ValueError(message)
    with pytest.raises(ValueError, match=r'Delayed failure\.'):
        raise exception

    with caplog.at_level(logging.ERROR):
        exception_dispatcher(exception, {})

    assert len(caplog.records) == 1
    assert caplog.records[0].exc_info == (
        ValueError,
        exception,
        exception.__traceback__,
    )
