#!/usr/bin/env python3
"""
Setup script for AI Racing Simulator
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
version = {}
with open("src/__init__.py", "r", encoding="utf-8") as fh:
    exec(fh.read(), version)

setup(
    name="ai-racing-simulator",
    version=version["__version__"],
    author=version["__author__"],
    author_email="ai-racing-simulator@example.com",
    description=version["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-racing-simulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Simulation",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - pure Python!
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "coverage>=5.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai-racing-demo=src.visualization.showcase_finale:main",
            "ai-racing-championship=src.visualization.grand_prix_finale:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-racing-simulator/issues",
        "Source": "https://github.com/yourusername/ai-racing-simulator",
        "Documentation": "https://github.com/yourusername/ai-racing-simulator/docs",
    },
    keywords="ai racing simulation game artificial-intelligence motorsports",
)