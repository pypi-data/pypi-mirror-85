import os
import sys

import setuptools

VERSION = open(os.path.join("plissken", "VERSION")).read().strip()


requirements = ["click>7.0.0", "colander==1.7.0", "redbaron>=0.9.2", "jinja2 >= 2"]

dev_requirements = [
    "future",
    "pytest==3.8.0",
    "pytest-cov==2.6.0",
    "sphinx==1.8.0",
    "sphinx-rtd-theme==0.4.1",
    "angreal>=0.7.0",
    "mypy>=0.660",
    "lxml==4.3.0",
    "black==19.10b0",
    "pre-commit==2.2.0",
]


setuptools.setup(
    name="plissken",
    description="",
    long_description="""""",
    url="https://gitlab.com/dylanbstorey/plissken",
    author="dylanbstorey",
    author_email="dylan.storey@gmail.com",
    license="GPLv3",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    zip_safe=False,
    version=VERSION,
    entry_points={"console_scripts": ["plissken=plissken.cli:main"]},
    python_requires=">=3",
    include_package_data=True,
    extras_require={"dev": dev_requirements},
)
