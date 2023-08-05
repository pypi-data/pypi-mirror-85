import os
from setuptools import setup

setup(
    name = "body_crop",
    version = "0.9",
    author = "Michael Blahay",
    author_email = "mblahay@gmail.com",
    description = ("Tool for cropping files"),
    license = "MIT",
    keywords = "body_crop",
    url = "https://github.com/mblahay/body",
    packages=['body_crop'],
    long_description='Tool for cropping the contents for files.',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
)
