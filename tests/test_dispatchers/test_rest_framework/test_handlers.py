import pytest

from rest_framework import exceptions as rest_exceptions

from exception_dispatcher.dispatchers import rest_framework as handlers


class _TestAuthenticationException(rest_exceptions.AuthenticationFailed):
    auth_header = 'Bearer realm="Access testing API"'


@pytest.mark.parametrize(('exception', 'expected_headers'), [
    (rest_exceptions.ParseError(), {}),
    (rest_exceptions.Throttled(wait=120), {'Retry-After': '120'}),
    (
        _TestAuthenticationException(),
        {'WWW-Authenticate': _TestAuthenticationException.auth_header},
    ),
])
def test_response_headers(exception, expected_headers):
    """Ensure response with expected headers is returned."""
    response = handlers.handle_rest_framework_api_exception(exception, {})
    assert set(expected_headers.items()) <= set(response.items())


def test_response_data():
    """Ensure response with expected data is returned."""
    detail = 'Dummy detail'
    code = 'dummy_code'
    exception = rest_exceptions.APIException(detail=detail, code=code)

    response = handlers.handle_rest_framework_api_exception(exception, {})

    assert code in str(response.data)
    assert detail in str(response.data)


def test_response_status_code():
    """Ensure response with expected status code is returned."""
    exception = rest_exceptions.PermissionDenied()

    response = handlers.handle_rest_framework_api_exception(exception, {})

    assert response.status_code == exception.status_code


def test_set_rollback_default(mocker):
    """Ensure ``set_rollback`` is called by default."""
    set_rollback_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.set_rollback',
    )

    handlers.handle_rest_framework_api_exception(
        rest_exceptions.AuthenticationFailed(),
        {},
    )

    set_rollback_mock.assert_called_once()


def test_set_rollback_disabled(mocker):
    """Ensure ``set_rollback`` is not called when disabled via settings."""
    set_rollback_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.set_rollback',
    )
    settings_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.settings',
    )
    settings_mock.EXCEPTION_DISPATCHER_SET_ROLLBACK = False

    handlers.handle_rest_framework_api_exception(
        rest_exceptions.AuthenticationFailed(),
        {},
    )

    set_rollback_mock.assert_not_called()
