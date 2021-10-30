import pytest

from django.core.exceptions import (
    DisallowedHost,
    PermissionDenied,
    SuspiciousOperation,
)
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import exception_handler as rest_exception_handler

from exception_dispatcher.handlers import exception_handler


@pytest.mark.parametrize('exception', [
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
    Http404(),
])
def test_rest_framework_exception(exception):
    """Ensure response returned by our and rest_framework handler are equal."""
    rest_framework_response = rest_exception_handler(exception, {})

    response = exception_handler(exception, {})

    assert rest_framework_response
    assert response
    assert response.status_code == rest_framework_response.status_code
    assert set(response.items()) == set(rest_framework_response.items())
    assert response.data == rest_framework_response.data


@pytest.mark.parametrize('exception', [
    Exception(),
    ValueError(),
    TypeError(),
    AssertionError(),
    # `django` exceptions
    DisallowedHost(),
    SuspiciousOperation(),
])
def test_other_exception(exception):
    """Ensure response returned by our and rest_framework handler are equal."""
    assert (
        exception_handler(exception, {})
        == rest_exception_handler(exception, {})
    )
