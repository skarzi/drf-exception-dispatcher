import pytest

from exception_dispatcher.dispatchers.rest_framework import (
    get_api_exception_parser,
)
from exception_dispatcher.parsers import parse_rest_framework_api_exception


def dummy_parser(exception, context):
    """``APIException`` dummy parser for testing purposes."""


@pytest.fixture
def get_parser():
    """Manage cache of ``get_api_exception_parser``."""
    get_api_exception_parser.cache_clear()
    yield get_api_exception_parser
    get_api_exception_parser.cache_clear()


def test_get_api_exception_parser_default(get_parser):
    """Ensure default parser is returned when custom parser not specified."""
    parser = get_parser()

    assert parser == parse_rest_framework_api_exception


def test_get_api_exception_parser_custom(mocker, get_parser):
    """Ensure custom parser is returned when setting set."""
    settings_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.settings',
    )
    settings_mock.EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER = (
        'test_parser_getter.dummy_parser'
    )

    parser = get_parser()

    assert parser == dummy_parser


def test_get_api_exception_parser_error(mocker, get_parser):
    """Ensure ``ImportError`` is raised when parser cannot be imported."""
    settings_mock = mocker.patch(
        'exception_dispatcher.dispatchers.rest_framework.settings',
    )
    settings_mock.EXCEPTION_DISPATCHER_API_EXCEPTION_PARSER = (
        'invalid_module.with_exception.parser'
    )

    with pytest.raises(ImportError, match='Could not import'):
        get_parser()
