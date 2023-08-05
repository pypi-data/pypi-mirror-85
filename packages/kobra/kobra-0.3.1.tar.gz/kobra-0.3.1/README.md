# 🐍 Kobra
Wrapper for `twine` &amp; `python setup.py`. The name of this module is not an error but a combination of the words king and cobra.
## 💾 Install
Installing the project by using pip:
```
pip install kobra
```
If you have \*nix such a system (Android, Mac OS, Free BSD, Linux) you may not have the last python in your terminal, so use:
```
pip3 install kobra
```  
## ⚙️ Functions
Part of the functionality is copying from `python setup.py`.
### 💾 Install
Installing the module from source code:
```
kobra
```
or:
```
kobra install
```
### 🧑‍💻 Develop
A command for developers to use the module folder as the main:
```
kobra develop
```
It is desirable to use when changing locales and configs of your module, which are in separate files.
### 📦 Publish
With this command, you can change the version of your module, create a build with `python setup.py sdist` and release to pypi.org:
```
kobra publish
```
For the command to work in your module there must be a file `__init__.py`, for example the following:
```python
__version__ = "0.2.1"
```
You can also use the version from `__init__.py` in your `setup.py`:
```python
from setuptools import setup
from <modulename> import __version__

setup(
    ...
    version=__version__
    ...
)
```
