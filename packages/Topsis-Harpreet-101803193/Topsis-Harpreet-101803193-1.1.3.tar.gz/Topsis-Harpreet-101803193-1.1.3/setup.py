from sys import version
from setuptools import _install_setup_requires, setup


# This call to setup() does all the work
setup(
    name="Topsis-Harpreet-101803193",
    version="1.1.3",
    description="Implements Topsis",

    author="Harpreet singh",
    author_email="harpreetng22@gmail.com",
    license="MIT",
    packages=['topsis'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=['pandas',
                      'numpy'],
)

