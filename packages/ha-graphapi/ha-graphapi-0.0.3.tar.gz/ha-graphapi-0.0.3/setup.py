import pathlib
from setuptools import find_packages, setup

PACKAGES = [f"hagraphapi.{p}" for p in find_packages(where="hagraphapi")]

# This call to setup() does all the work
setup(
    name="ha-graphapi",
    version="0.0.3",
    description="For use with Home Assistant to query Microsoft's Graph API",
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
    packages=PACKAGES,
    install_requires=[
        "aiohttp",
        "appdirs",
        "ms_cv",
        "pydantic",
    ]
)