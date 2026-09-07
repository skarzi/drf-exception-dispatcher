"""Tests for release tag validation."""

import pytest

from packaging.version import Version

from tools.validate_release import validate_release

_STABLE_VERSION = '1.2.3'
_PRERELEASE_VERSION = '1.2.3rc1'


@pytest.mark.parametrize(
    ('version_string', 'expected'),
    [
        (_STABLE_VERSION, Version(_STABLE_VERSION)),
        (_PRERELEASE_VERSION, Version(_PRERELEASE_VERSION)),
    ],
)
def test_validate_release(version_string: str, expected: Version) -> None:
    """Accept canonical tags matching the project version."""
    version = validate_release(version_string, version_string)

    assert version == expected
    assert version.is_prerelease is expected.is_prerelease


@pytest.mark.parametrize(
    ('tag', 'project_version', 'message'),
    [
        ('release', _STABLE_VERSION, 'Invalid release tag'),
        ('1.2.3-rc.1', _PRERELEASE_VERSION, 'Release tag is not canonical'),
        ('1.2.4', _STABLE_VERSION, 'does not match project version'),
    ],
)
def test_validate_release_error(
    tag: str,
    project_version: str,
    message: str,
) -> None:
    """Reject invalid, noncanonical, and mismatched tags."""
    with pytest.raises(SystemExit, match=message):
        validate_release(tag, project_version)
