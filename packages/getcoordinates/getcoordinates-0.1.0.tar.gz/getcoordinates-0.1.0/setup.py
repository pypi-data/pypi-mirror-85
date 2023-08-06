"""Packaging file."""
from distutils.core import setup


__version__ = "0.1.0"
URL = "https://github.com/massard-t/getcoordinates/archive/{}.tar.gz".format(__version__)

setup(
    name="getcoordinates",
    packages=["getcoordinates"],
    install_requires=['requests'],
    version=__version__,
    description="Get a location (latitude, longitude) from an address.",
    author="Theo 'Bob' Massard",
    author_email="massar_t@etna-alternance.net",
    url="https://github.com/tbobm/getcoordinates",
    download_url=URL,
    keywords=["cli", "location"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    entry_points={"console_scripts": ["getcoordinates=getcoordinates:main"]},
)
