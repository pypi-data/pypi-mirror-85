from setuptools import setup
from kobra import __version__

with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="kobra",
    version=__version__,
    author="Daniel Zakharov",
    author_email="daniel734@bk.ru",
    description="Wrapper for twine & python setup.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="kobra tool",
    url="https://github.com/jDan735/kobra",
    license="MIT",
    packages=["kobra"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3",
    entry_points={
        "console_scripts": [
            "kobra=kobra.__main__:main"
        ]
    }
)
