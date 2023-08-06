""" crmngr setup module. """

from pathlib import Path
import re
from setuptools import setup, find_packages


def find_version(source_file):
    """read __version__ from source file"""
    with open(source_file) as version_file:
        version_match = re.search(r"^__version__\s*=\s* ['\"]([^'\"]*)['\"]",
                                  version_file.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError('Unable to find package version')


setup(
    name='spyhook',
    author='Andre Keller',
    author_email='ak@0x2a.io',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Systems Administration',
    ],
    description='a simple gitlab webhook receiver',
    entry_points={
        'console_scripts': [
            'spyhook = spyhook:setup'
        ]
    },
    install_requires=[
        'aiohttp>=3.4.0',
    ],
    python_requires='>=3.6',
    # BSD 3-Clause License:
    # - https://opensource.org/licenses/MIT
    license='MIT',
    packages=find_packages(),
    url='https://github.com/andrekeller/spyhook',
    version=find_version(str(Path('./spyhook/version.py'))),
)
