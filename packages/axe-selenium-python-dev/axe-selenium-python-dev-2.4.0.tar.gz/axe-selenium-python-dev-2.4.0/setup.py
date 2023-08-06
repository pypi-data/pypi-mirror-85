# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from ensurepip import version

from setuptools import find_packages, setup

with open("./README.rst") as f:
    readme = f.read()

setup(
    version="2.4.0",
    name="axe-selenium-python-dev",
    use_scm_version=False,
    setup_requires=["setuptools_scm"],
    description="Python library to integrate axe and selenium for web \
                accessibility testing.",
    long_description=open("README.rst").read(),
    url="https://github.com/EngrSushantSharma/axe-selenium-python.git",
    author="Sushant Sharma",
    author_email="engrSushantSharma@gmail.com",
    packages=find_packages(),
    package_data={
        "axe_selenium_python_dev": [
            "node_modules/axe-core/axe.min.js",
            "tests/test_page.html",
        ]
    },
    include_package_data=True,
    install_requires=["selenium>=3.0.2", "pytest>=3.0"],
    license="Mozilla Public License 2.0 (MPL 2.0)",
    keywords="axe-core selenium pytest-selenium accessibility automation mozilla",
)
