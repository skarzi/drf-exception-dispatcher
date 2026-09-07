"""Tests for built-in API exception parsers."""

import pytest

from rest_framework.exceptions import (
    APIException,
    ErrorDetail,
)

from exception_dispatcher import parsers
from exception_dispatcher.types import APIExceptionDetail


@pytest.mark.parametrize(
    ('exception', 'expected_result'),
    [
        (
            APIException('string', 'code'),
            {'detail': ErrorDetail('string', 'code')},
        ),
        (APIException(['error1'], 'list'), [ErrorDetail('error1', 'list')]),
        (APIException({'dict': 'error2'}, 'dict'), {'dict': 'error2'}),
    ],
)
def test_parse_rest_framework_api_exception(
    exception: APIException,
    expected_result: APIExceptionDetail,
) -> None:
    """Ensure ``APIException`` instance is properly parsed."""
    parsed_exception = parsers.parse_rest_framework_api_exception(exception, {})

    assert parsed_exception == expected_result
