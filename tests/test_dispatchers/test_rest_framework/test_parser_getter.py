"""Tests for API exception parser loading."""

from collections.abc import Callable, Generator

import pytest

from pytest_mock import MockerFixture
from rest_framework.exceptions import APIException

from exception_dispatcher.dispatchers.rest_framework import (
    APIExceptionParser,
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


@pytest.fixture
def get_parser() -> Generator[Callable[[], APIExceptionParser], None, None]:
    """Manage cache of ``get_api_exception_parser``."""
    get_api_exception_parser.cache_clear()
    yield get_api_exception_parser
    get_api_exception_parser.cache_clear()


def test_get_api_exception_parser_default(
    get_parser: Callable[[], APIExceptionParser],
) -> None:
    """Ensure default parser is returned when custom parser not specified."""
    parser = get_parser()

    assert parser == parse_rest_framework_api_exception


def test_get_api_exception_parser_custom(
    mocker: MockerFixture,
    get_parser: Callable[[], APIExceptionParser],
) -> None:
    """Ensure custom parser is returned when setting set."""
    settings_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.settings',
    )
    settings_mock.EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER = (
        f'{__name__}.dummy_parser'
    )

    parser = get_parser()

    assert parser == dummy_parser


def test_get_api_exception_parser_error(
    mocker: MockerFixture,
    get_parser: Callable[[], APIExceptionParser],
) -> None:
    """Ensure ``ImportError`` is raised when parser cannot be imported."""
    settings_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.settings',
    )
    settings_mock.EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER = (
        'invalid_module.with_exception.parser'
    )

    with pytest.raises(ImportError, match='Could not import') as exc_info:
        get_parser()

    assert isinstance(exc_info.value.__cause__, ImportError)
