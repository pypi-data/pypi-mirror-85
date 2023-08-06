
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="TOPSIS-Pranshu-101803102",
    version="0.0.1",
    py_modules = ["TOPSIS"],
    description=("This package allows you to run The Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS) on your dataset for Multiple Attribute Decision Making(MADM)'"),   # Give a short description about your library
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Pranshu Goyal",
    author_email="pgoyal_be18@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["TOPSIS-Pranshu-101803102"],
    include_package_data=True,
    install_requires=["requests"],
    
)
