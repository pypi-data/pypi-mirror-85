import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="packaage",
    version="0.0.1",
    description='Packaage is a Python library with few AI utils',
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["packaage"],
    install_requires=['unidecode'],
    include_package_data=True,
)
