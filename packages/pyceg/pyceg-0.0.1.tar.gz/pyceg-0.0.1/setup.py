import pathlib
from setuptools import setup, find_packages
from pyceg.pypi import PyPi

HERE = pathlib.Path(__file__).parent

PACKAGE_NAME = 'pyceg'
VERSION = "0.0.1"
AUTHOR = 'Nevin WS Ganesan'
AUTHOR_EMAIL = 'PyNevin@idarkduck.com'
URL = 'https://github.com/iDuckDark/PyNevin'

LICENSE = 'Apache License 2.0'
DESCRIPTION = "Bringing Computer Architectures and Real Time Systems to Life Through Pythonic Implementations"
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'click',
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      entry_points='''
            [console_scripts]
            pyceg=pyceg.cli:cli
        ''',
      )