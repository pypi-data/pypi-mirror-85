from setuptools import setup

VERSION = "v1.2"

readme = open("readme.md", "r").read();

setup(
    name = "pymulticrypt",
    packages = ["pymulticrypt"],
    version = VERSION,
    license = "MIT",
    description = "Python Module for secure End-2-End encryption using the Multicrypt algorithm made by me",
    long_description = readme,
    long_description_content_type = "text/markdown",
    author = "Abhay Tripathi",
    author_email = "abhay.triipathi@gmail.com",
    url = "https://github.com/AbhayTr/PyMulticrypt",
    download_url = "https://github.com/AbhayTr/PyMulticrypt/archive/" + VERSION + ".tar.gz",
    keywords = ["PyMulticrypt", "Encryption", "Asymmetric Encryption", "Symmetric Encryption", "End2End Encryption", "End2End", "Signal Protocol"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
