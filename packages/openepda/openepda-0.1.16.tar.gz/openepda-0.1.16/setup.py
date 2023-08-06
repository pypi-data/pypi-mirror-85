import io
import setuptools

from _version import __version__

import os

if not os.path.exists("README"):
    os.link("README.rst", "README")

with io.open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

long_description = long_description.replace(
    ".. _changes: CHANGES",
    ".. _changes: https://openepda.org/pypi_package/history_of_changes.html",
)
long_description = long_description.replace(
    ".. _authors: AUTHORS", ".. _authors: https://openepda.org/about.html"
)

# Remove badges not available from outside gitlab
long_description = long_description.replace("|ci| |coverage| ", "")

with open("requirements.txt", "r") as fh:
    # remove newline characters
    install_requires = [p[:-1] for p in fh.readlines()]

setuptools.setup(
    name="openepda",
    version=__version__,
    author="Dzmitry Pustakhod",
    author_email="d.pustakhod@tue.nl",
    description="Implementation of open standards for electronic-photonic design automation",
    keywords="EPDA data science electronics photonics design automation standard CAD PDA PIC",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="http://openepda.org",
    packages=setuptools.find_packages(),
    package_data={"openepda": ["schemas/*.*"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
    ],
    install_requires=install_requires,
)
