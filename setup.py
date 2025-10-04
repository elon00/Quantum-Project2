"""
Setup configuration for Deutsch-Jozsa Quantum Algorithm package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

dev_requirements = []
with open("requirements-dev.txt", encoding="utf-8") as f:
    dev_requirements = [
        line.strip() 
        for line in f 
        if line.strip() and not line.startswith("#") and not line.startswith("-r")
    ]

setup(
    name="quantum-deutsch-jozsa",
    version="1.0.0",
    author="Martin Luther",
    author_email="martinlutherupa1@gmail.com",
    description="Professional implementation of the Deutsch-Jozsa quantum algorithm using Qiskit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elon00/Quantum-Project2",
    project_urls={
        "Bug Tracker": "https://github.com/elon00/Quantum-Project2/issues",
        "Documentation": "https://github.com/elon00/Quantum-Project2#readme",
        "Source Code": "https://github.com/elon00/Quantum-Project2",
        "Changelog": "https://github.com/elon00/Quantum-Project2/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests", "tests.*", "docs", ".github"]),
    py_modules=["deutsch_jozsa"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    keywords=[
        "quantum computing",
        "quantum algorithm",
        "deutsch-jozsa",
        "qiskit",
        "quantum mechanics",
        "quantum information",
        "quantum simulation",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=8.0.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
        ],
        "docs": [
            "sphinx>=7.2.0",
            "sphinx-rtd-theme>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "deutsch-jozsa=deutsch_jozsa:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    platforms=["any"],
    license="MIT",
)