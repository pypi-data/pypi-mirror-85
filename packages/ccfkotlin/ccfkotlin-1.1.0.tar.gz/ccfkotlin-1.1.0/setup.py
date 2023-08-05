import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ccfkotlin",
    packages=["ccfkotlin"],
    entry_points={
        "console_scripts": ['ccfkotlin = ccfkotlin.__main__:main']
    },
    version="1.1.0",
    description="Kotlin code conversions fixer",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Alexandra Kmet",
    url="https://github.com/alexandrakmet/Metaprogramming",
)

