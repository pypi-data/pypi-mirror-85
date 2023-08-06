# -*- coding: utf-8 -*-
"""Setup configuration."""

from setuptools import find_packages
from setuptools import setup

setup(
    name="curibio.sdk",
    version="0.8.0",
    description="CREATE A DESCRIPTION",
    url="https://github.com/CuriBio/curibio.sdk",
    project_urls={"Documentation": "https://curibiosdk.readthedocs.io/en/latest/"},
    author="Curi Bio",
    author_email="contact@curibio.com",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages("src"),
    namespace_packages=["curibio"],
    install_requires=[
        "h5py>=2.10.0",
        "nptyping>=1.3.0",
        "numpy>=1.19.0",
        "immutabledict>=1.0",
        "XlsxWriter>=1.3.3",
        "openpyxl>=3.0.5",
        "matplotlib>=3.3.1",
        "mantarray-file-manager>=0.4.1",
        "stdlib_utils>=0.3.1",
        "mantarray-waveform-analysis>=0.5.8",
        "labware-domain-models>=0.2",
        'importlib-metadata ~= 1.0 ; python_version < "3.8"',
    ],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
)
