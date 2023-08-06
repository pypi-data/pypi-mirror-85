import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.2.1'
PACKAGE_NAME = 'toposis-parth-101853019'
AUTHOR = 'Parth Khandelwal'
AUTHOR_EMAIL = 'parthmanan1999@gmail.com'
URL = 'https://github.com/you/your_package'

LICENSE = 'Apache License 2.0'

DESCRIPTION = 'TOPSIS is an algorithm for the determination of the best choice out of many using Positive Ideal Solution and Negative Ideal'
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