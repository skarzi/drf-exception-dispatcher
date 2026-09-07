"""Tests for API exception parser loading."""

import pytest

from django.test import override_settings
from rest_framework.exceptions import APIException

from exception_dispatcher.dispatchers.rest_framework import (
    get_api_exception_parser,
)
from exception_dispatcher.parsers import parse_rest_framework_api_exception
from exception_dispatcher.types import APIExceptionDetail, ContextType


def dummy_parser(
    exception: APIException,
    context: ContextType,
) -> APIExceptionDetail:
    """``APIException`` dummy parser for testing purposes."""
    return {'context': context, 'detail': exception.detail}


def test_get_api_exception_parser_default() -> None:
    """Ensure default parser is returned when custom parser not specified."""
    parser = get_api_exception_parser()

    assert parser == parse_rest_framework_api_exception


def test_get_api_exception_parser_custom() -> None:
    """Ensure custom parser is returned when setting set."""
    get_api_exception_parser()

    with override_settings(
        EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER=f'{__name__}.dummy_parser',
    ):
        parser = get_api_exception_parser()

    assert parser == dummy_parser


def test_get_api_exception_parser_error() -> None:
    """Ensure ``ImportError`` is raised when parser cannot be imported."""
    with (
        override_settings(
            EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER=(
                'invalid_module.with_exception.parser'
            ),
        ),
        pytest.raises(ImportError, match='Could not import') as exc_info,
    ):
        get_api_exception_parser()

    assert isinstance(exc_info.value.__cause__, ImportError)
