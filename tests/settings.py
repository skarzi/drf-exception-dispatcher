"""Django's settings used for tests and type checking."""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

SECRET_KEY = 'not very secret in tests'  # noqa: S105
