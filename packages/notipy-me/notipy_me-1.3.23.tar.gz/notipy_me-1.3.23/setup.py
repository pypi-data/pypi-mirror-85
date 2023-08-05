import os
import re

# To use a consistent encoding
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def read(*parts):
    with open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("notipy_me", "__version__.py")

test_deps = ['pytest', 'pytest-cov', 'coveralls', 'validate_version_code']

extras = {
    'test': test_deps,
}

setup(
    name='notipy_me',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='A simple python package to send you and any other receiver an email when a portion of code is done running.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/LucaCappelletti94/notipy_me',

    # Author details
    author='Luca Cappelletti',
    author_email='cappelletti.luca94@gmail.com',

    # Choose your license
    license='MIT',

    include_package_data=True,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='>3.5.2',
    install_requires=[
        "humanize",
        "validate_email",
        "tabulate",
        "environments_utils",
        "validators",
        "userinput",
        "sanitize_ml_labels>=1.0.16"
    ],
    tests_require=test_deps,
    extras_require=extras,
)


def status(s):
    print('\033[1m{0}\033[0m'.format(s))
