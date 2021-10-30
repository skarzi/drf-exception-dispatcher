import os

import django

from django.conf import settings


def pytest_configure(config):
    """Configure Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    settings.configure()
    django.setup()
