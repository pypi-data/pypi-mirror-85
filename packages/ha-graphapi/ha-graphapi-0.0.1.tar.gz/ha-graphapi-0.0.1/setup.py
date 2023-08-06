import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ha-graphapi",
    version="0.0.1",
    description="For use with Home Assistant to query Microsoft's Graph API",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Jamie Weston",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["hagraphapi"],
    install_requires=[
        "aiohttp",
        "appdirs",
        "ms_cv",
        "pydantic",
    ]
)