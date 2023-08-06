"""Setup the candystore package."""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="candystore",
    version="0.3.0",
    author="Craig Franklin",
    author_email="craigjfranklin@gmail.com",
    description="Factories for randomised AFL data sets for testing purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tipresias/candystore",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy>=1.0,<2.0",
        "pandas>=0.24.0,<2.0",
        "faker>=4.0,<5.0",
        "mypy>=0.70,<1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
