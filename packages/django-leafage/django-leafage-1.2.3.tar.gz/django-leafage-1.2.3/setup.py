
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="django-leafage",
    version="1.2.3",
    description="Simple and Easiest paginator for Django.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/nilesh-kr-dubey/django-leafage",
    author="Nilesh Kumar Dubey",
    author_email="nileshdubeyindia@gmail.com",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    packages=['leafage'],
    install_requires=[
        "Django >= 2.0",
    ],
    include_package_data=True,
)
