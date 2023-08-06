import pathlib
from setuptools import setup
from packaage.__init__ import __version__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="packaage",
    version=__version__,
    description='Packaage is a Python library with few AI utils',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["packaage"],
    install_requires=['unidecode'],
    include_package_data=True,
)
