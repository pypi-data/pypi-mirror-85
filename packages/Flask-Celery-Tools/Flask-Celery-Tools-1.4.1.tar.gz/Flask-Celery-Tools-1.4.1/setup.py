#!/usr/bin/env python
"""Setup script for the project."""

import os
import re
from typing import List

from setuptools import Command, find_packages, setup

IMPORT = 'flask_celery'
LICENSE = 'MIT'
INSTALL_REQUIRES = [
    'flask>=1.0.2',
    'celery<=5.0.2',
    'redis>=3.5.3',
    'sqlalchemy>=1.2.7'
]
NAME = 'Flask-Celery-Tools'
VERSION = '1.4.1'


def requirements(path='requirements.txt') -> List[str]:
    """Read requirements.txt file.

    :param str path: Path to requirments.txt file.
    :return: File lines.
    :rtype: List[str]
    """
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    with open(path, 'r') as requirements_handle:
        return [line.strip() for line in requirements_handle.readlines()]


def readme(path='README.md') -> str:
    """Try to read README.md or return empty string if failed.

    :param str path: Path to README file.

    :return: File contents.
    :rtype: str
    """
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    with open(path, 'r') as readme_handle:
        return readme_handle.read()


class CheckVersion(Command):
    """Make sure version strings and other metadata match here, in module/package, tox, and other places."""

    description = 'verify consistent version/etc strings in project'
    user_options = []

    @classmethod
    def initialize_options(cls):  # noqa: D401
        """Required by distutils."""

    @classmethod
    def finalize_options(cls):  # noqa: D401
        """Required by distutils."""

    @classmethod
    def run(cls):
        """Check variables."""
        project = __import__(IMPORT, fromlist=[''])
        for expected, var in [('@Salamek', '__author__'), (LICENSE, '__license__'), (VERSION, '__version__')]:
            if getattr(project, var) != expected:
                raise SystemExit('Mismatch: {0}'.format(var))
        # Check changelog.
        if not re.compile(r'^%s - \d{4}-\d{2}-\d{2}[\r\n]' % VERSION, re.MULTILINE).search(readme()):
            raise SystemExit('Version not found in readme/changelog file.')
        # Check tox.
        requirements_without_version = [re.split(r'(>=|==|<=)', req)[0] for req in INSTALL_REQUIRES]
        contents = readme('tox.ini')
        section = re.compile(r'[\r\n]+install_requires =[\r\n]+(.+?)[\r\n]+\w', re.DOTALL).findall(contents)
        if not section:
            raise SystemExit('Missing install_requires section in tox.ini.')
        in_tox = re.findall(r'    ([^=]+)==[\w\d.-]+', section[0])
        if requirements_without_version != in_tox:
            raise SystemExit('Missing/unordered pinned dependencies in tox.ini.')


if __name__ == '__main__':
    setup(
        author='@Salamek',
        author_email='adam.schubert@sg1-game.net',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Web Environment',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Framework :: Flask',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development :: Libraries',
        ],
        cmdclass=dict(check_version=CheckVersion),
        description='Celery support for Flask without breaking PyCharm inspections.',
        install_requires=INSTALL_REQUIRES,
        keywords='flask celery redis',
        license=LICENSE,
        long_description=readme(),
        long_description_content_type='text/markdown',
        name=NAME,
        packages=find_packages(exclude=['tests', 'tests.*']),
        url='https://github.com/Salamek/' + NAME,
        version=VERSION,
        zip_safe=False
    )
