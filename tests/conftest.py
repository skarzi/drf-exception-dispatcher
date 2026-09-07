"""Shared pytest configuration."""

import os

import django


def pytest_configure() -> None:
    """Configure Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    django.setup()
