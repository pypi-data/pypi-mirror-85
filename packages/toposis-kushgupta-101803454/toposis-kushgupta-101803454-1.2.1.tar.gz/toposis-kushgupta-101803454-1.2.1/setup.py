import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.2.1'
PACKAGE_NAME = 'toposis-kushgupta-101803454'
AUTHOR = 'Kush Gupta'
AUTHOR_EMAIL = 'kgupta1_be18@thapar.edu'
URL = 'https://github.com/you/your_package'

LICENSE = 'Apache License 2.0'

DESCRIPTION = 'TOPSIS is an algorithm to determine the best choice out of many using Positive Ideal Solution and Negative Ideal'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'tabulate',
      'scipy'
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
      packages=find_packages()
      )
