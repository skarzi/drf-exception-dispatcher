import logging

from exception_dispatcher.dispatchers.main import exception_dispatcher


def test_returned_value():
    """Ensure ``None`` is returned."""
    assert exception_dispatcher(ValueError(), {}) is None


def test_logger(caplog):
    """Ensure exception is logged."""
    with caplog.at_level(logging.ERROR):
        exception_dispatcher(ValueError(), {})

    assert len(caplog.records) == 1
