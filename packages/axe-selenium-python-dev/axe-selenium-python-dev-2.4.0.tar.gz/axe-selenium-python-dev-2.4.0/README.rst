axe-selenium-python-dev
=======================

axe-selenium-python-dev was forked from https://github.com/mozilla-services/axe-selenium-python 
on date 29/10/2020 all credits to them, there was no official pypi distribution available
which supports axe-core 3.3.2 so took the opportunity to create this to support others like us 

This version of axe-selenium-python-dev supports all changes in repo 
https://github.com/mozilla-services/axe-selenium-python before date 29/10/2020

**This version of axe-selenium-python-dev is using axe-core@3.3.2.**

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/mozilla-services/axe-selenium-python/blob/master/LICENSE.txt
   :alt: License
.. image:: https://img.shields.io/pypi/v/axe-selenium-python-dev.svg
   :target: https://pypi.org/project/axe-selenium-python-dev/
   :alt: PyPI

Requirements
------------

You will need the following prerequisites in order to use axe-selenium-python:

- selenium >= 3.0.0
- Python 2.7 or 3.6
- The appropriate driver for the browser you intend to use, downloaded and added to your path, e.g. geckodriver for Firefox:

  - `geckodriver <https://github.com/mozilla/geckodriver/releases>`_ downloaded and `added to your PATH <https://stackoverflow.com/questions/40208051/selenium-using-python-geckodriver-executable-needs-to-be-in-path#answer-40208762>`_

Installation
------------

To install axe-selenium-python-dev:

.. code-block:: bash

  $ pip install axe-selenium-python-dev


Usage
------

.. code-block:: python

  from selenium import webdriver
  from axe_selenium_python import Axe

  def test_google():
      driver = webdriver.Firefox()
      driver.get("http://www.google.com")
      axe = Axe(driver)
      # Inject axe-core javascript into page.
      axe.inject()
      # Run axe accessibility checks.
      results = axe.run()
      # Write results to file
      axe.write_results(results, 'a11y.json')
      driver.close()
      # Assert no violations are found
      assert len(results["violations"]) == 0, axe.report(results["violations"])

The method ``axe.run()`` accepts two parameters: ``context`` and ``options``.

For more information on ``context`` and ``options``, view the `aXe documentation here <https://github.com/dequelabs/axe-core/blob/master/doc/API.md#parameters-axerun>`_.

Resources
---------

- `Issue Tracker <http://github.com/mozilla-services/axe-selenium-python/issues>`_
- `Code <http://github.com/mozilla-services/axe-selenium-python/>`_
- `pytest-axe <http://github.com/mozilla-services/pytest-axe/>`_

CHANGELOG
^^^^^^^^^^^^^^

version 2.4.0
*************

- Remove unused build modules


version 2.3.0
*************

- Axe-core node modules min file updated from 2.3.1 to 3.3.2 


version 2.2.0
*************

- Axe-core node modules 3.3.2 path updated

version 2.1.0
*************

- Axe-core node modules 3.3.2 path updated

version 2.0.0
*************

- Axe-core node modules 3.3.2 updated

version 1.2.0
*************

- Updated to install node modules

version 1.1.1
*************

- Updated readme

version 1.1.0
*************

- Created package.json file to maintain axe-core dependency

version 1.0.0
*************

- Forked https://github.com/mozilla-services/axe-selenium-python updated code and initial pypi deploy
