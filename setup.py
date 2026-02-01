#!/usr/bin/env python
"""Setup script for Tombo Language"""

from setuptools import setup, find_packages

setup(
    name="tombo-language",
    version="1.0.0",
    description="Tombo (TO) - A universal interpreted programming language with hardware access",
    author="Tombo Team",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "tombo=core.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Interpreters",
    ],
)
