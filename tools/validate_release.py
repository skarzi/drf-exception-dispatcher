"""Validate a release tag and export GitHub Actions outputs."""

import os
import sys
import tomllib

from pathlib import Path

from packaging.version import InvalidVersion, Version


def validate_release(tag: str, project_version: str) -> Version:
    """Return a canonical tag matching the project version."""
    try:
        version = Version(tag)
    except InvalidVersion:
        message = f'Invalid release tag: {tag}.'
        sys.exit(message)
    if tag != str(version):
        message = f'Release tag is not canonical: {tag}.'
        sys.exit(message)
    if version != Version(project_version):
        message = (
            f'Release tag {tag!r} does not match '
            f'project version {project_version!r}.'
        )
        sys.exit(message)
    return version


def main() -> None:
    """Validate the requested tag and write workflow outputs."""
    project = tomllib.loads(Path('pyproject.toml').read_text())['project']
    version = validate_release(os.environ['TARGET_TAG'], project['version'])
    prerelease = str(version.is_prerelease).lower()
    output = Path(os.environ['GITHUB_OUTPUT'])
    with output.open('a', encoding='utf-8') as stream:
        stream.write(f'tag={version}\n')
        stream.write(f'prerelease={prerelease}\n')


if __name__ == '__main__':
    main()
