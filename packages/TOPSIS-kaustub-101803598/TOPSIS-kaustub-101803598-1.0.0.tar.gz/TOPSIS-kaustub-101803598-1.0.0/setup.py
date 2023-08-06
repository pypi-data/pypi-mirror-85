
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-kaustub-101803598",
    version="1.0.0",
    author="Kaustubh",
    author_email="kbhatt_be18@thapar.edu",
    description="A package containing TOPSIS function.",
    long_description='''This package contains the working code of implementation of TOPSIS made by Kaustubh Bhatt.
    TOPSIS method helps in making a decision by ranking the list of items with the help of its algorithm. Feel free to use it.''',
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
