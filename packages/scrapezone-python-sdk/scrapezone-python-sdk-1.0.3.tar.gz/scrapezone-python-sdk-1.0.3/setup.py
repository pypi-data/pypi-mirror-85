import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="scrapezone-python-sdk",
    version="1.0.3",
    description="Official client SDK of Scrapezone",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Scrapezone/scrapezone-python-sdk",
    author="Scrapezone",
    author_email="admin@scrapezone.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["python-decouple"],
    entry_points={
        "console_scripts": [
            "scrapezone-client=client:__init__",
        ]
    },
)
