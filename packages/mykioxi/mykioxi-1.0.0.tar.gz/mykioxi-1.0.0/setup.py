import setuptools
import sys

if sys.version_info < (3,5):
    sys.exit("Python 3.5 or newer is required.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mykioxi",
    version="1.0.0",
    author="Radoslav Gerganov",
    author_email="rgerganov@gmail.com",
    description="Command line program for Myki oximeter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rgerganov/mykioxi",
    packages=['myki'],
    install_requires=[
        'bleak>=0.9.1',
        ],
    entry_points={
        'console_scripts': [
            'mykioxi=myki.mykioxi:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
