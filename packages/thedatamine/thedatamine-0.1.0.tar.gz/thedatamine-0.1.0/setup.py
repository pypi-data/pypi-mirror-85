import setuptools
import pathlib

ROOT = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'thedatamine'
AUTHOR = 'Kevin Amstutz'
AUTHOR_EMAIL = 'kevin@amstutz.io'
URL = 'https://github.com/TheDataMine/thedatamine_py'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Course package for Purdue University\'s integrative data science initiative, The Data Mine.'
LONG_DESCRIPTION = (ROOT / 'README.md').read_text()
LONG_DESC_TYPE = 'text/markdown'

# INSTALL_REQUIRES = [

# ]

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    url=URL,
    packages=setuptools.find_packages(),
    # install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
