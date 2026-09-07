"""Tests for the public exception handler."""

from typing import Never

import pytest

from django.core.exceptions import (
    DisallowedHost,
    PermissionDenied,
    SuspiciousOperation,
)
from django.http import Http404
from django.test import override_settings
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework.views import exception_handler as rest_exception_handler

from exception_dispatcher.handlers import exception_handler


class _ExceptionView(APIView):
    def get(self, _request: Request) -> Never:
        """Raise an exception for DRF's handler integration test."""
        raise Http404


@pytest.mark.parametrize(
    'exception',
    [
        exceptions.APIException('detail', 'code'),
        exceptions.AuthenticationFailed(),
        exceptions.MethodNotAllowed('GET'),
        exceptions.NotAcceptable(),
        exceptions.NotAuthenticated(),
        exceptions.NotFound(),
        exceptions.ParseError(),
        exceptions.PermissionDenied(),
        exceptions.Throttled(),
        exceptions.UnsupportedMediaType('application/vnd.skarzi+json'),
        exceptions.ValidationError(),
        # special cases of `django` exceptions
        PermissionDenied(),
        PermissionDenied('Access denied', 'access_denied'),
        Http404(),
        Http404('Missing object', 'missing_object'),
    ],
)
def test_rest_framework_exception(exception: Exception) -> None:
    """Ensure response returned by our and rest_framework handler are equal."""
    rest_framework_response = rest_exception_handler(exception, {})

    response = exception_handler(exception, {})

    assert rest_framework_response
    assert response
    assert response.status_code == rest_framework_response.status_code
    assert set(response.items()) == set(rest_framework_response.items())
    assert response.data == rest_framework_response.data


@pytest.mark.parametrize(
    'exception',
    [
        Exception(),
        ValueError(),
        TypeError(),
        AssertionError(),
        # `django` exceptions
        DisallowedHost(),
        SuspiciousOperation(),
    ],
)
def test_other_exception(exception: Exception) -> None:
    """Ensure response returned by our and rest_framework handler are equal."""
    assert exception_handler(exception, {}) == rest_exception_handler(
        exception, {}
    )


def test_drf_view_handler_parity() -> None:
    """Ensure DRF's view machinery produces the same rendered response."""
    view = _ExceptionView.as_view()
    request = APIRequestFactory().get('/')

    with override_settings(
        REST_FRAMEWORK={
            'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
            'UNAUTHENTICATED_USER': None,
        },
    ):
        rest_framework_response = view(request)
    with override_settings(
        REST_FRAMEWORK={
            'EXCEPTION_HANDLER': (
                'exception_dispatcher.handlers.exception_handler'
            ),
            'UNAUTHENTICATED_USER': None,
        },
    ):
        response = view(request)

    rest_framework_response.render()
    response.render()
    assert response.status_code == rest_framework_response.status_code
    assert set(response.items()) == set(rest_framework_response.items())
    assert response.data == rest_framework_response.data
    assert response.content == rest_framework_response.content
