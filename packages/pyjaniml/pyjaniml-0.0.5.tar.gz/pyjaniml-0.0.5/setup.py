import sys
from setuptools import setup
from pathlib import Path


ROOT = str(Path(__file__).resolve().parent)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from pyjaniml.utils import get_version


with open("readme.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pyjaniml",
    version=get_version(file_name="release_info", version_string="RELEASE_VERSION"),
    description="classes for janiml handling",
    author="Jannik Schwab",
    author_email="j.schwab@micro-biolytics.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mbio/pyjaniml",
    download_url="https://gitlab.com/mbio/pyjaniml/-/archive/master/pyjaniml-master.tar.gz",
    keywords=["AniML", "json"],
    packages=["pyjaniml"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "marshmallow",
    ],
    zip_safe=False,
    python_requires=">=3.6",
    include_package_data=True
)
