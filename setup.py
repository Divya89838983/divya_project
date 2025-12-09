"""
Setup configuration for ClearSkies Air Quality Monitor
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clearskies-aqi",
    version="1.0.0",
    author="Divya",
    author_email="your.email@example.com",
    description="Real-time air quality monitoring application using OpenWeather API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Divya89838983/divya_project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.0",
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "plotly>=5.17.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "clearskies=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "module": ["*.py"],
    },
)
