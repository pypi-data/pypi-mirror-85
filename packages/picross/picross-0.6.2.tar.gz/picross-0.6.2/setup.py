# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["picross", "picross.gui"]

package_data = {"": ["*"]}

install_requires = [
    "appdirs>=1.4.4,<2.0.0",
    "curio>=1.2,<2.0",
    "toml>=0.10.1,<0.11.0",
    "cryptography>=3.0.0,<4.0.0",
    "python-dateutil>=2.7.0,<3.0.0",
]

entry_points = {"console_scripts": ["picross = picross.__main__:run"]}

readme = open("README.md").read()

setup_kwargs = {
    "name": "picross",
    "version": "0.6.2",
    "description": "Python/Tk GUI browser for Gemini",
    "long_description": readme,
    "long_description_content_type": "text/markdown",
    "author": "Frederick Yin",
    "author_email": "fkfd@macaw.me",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://git.sr.ht/~fkfd/picross",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.7,<4.0",
}


setup(**setup_kwargs)
