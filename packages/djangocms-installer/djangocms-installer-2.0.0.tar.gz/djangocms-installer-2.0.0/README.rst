====================
django CMS Installer
====================

|Gitter| |PyPiVersion| |PyVersion| |GAStatus| |TestCoverage| |CodeClimate| |License|

Command to easily bootstrap django CMS projects

* Free software: BSD license

************
Features
************

``djangocms-installer`` is a console wizard to help bootstrapping a django CMS
project.

Refer to `django CMS Tutorial`_ on how to properly setup your first django CMS project.

.. warning:: Version 2.0 dropped support for Python 2.7, 3.5, django CMS < 3.7 and Django < 2.2.
             More 1.2.x versions may be released after 1.2 is out in case important bugfixes will be needed.

************
Usage
************

To create your first django CMS project run::

    djangocms my_project

That's all!

This command will:

* Create a Django project
* Install django CMS and its core plugins
* Create and populate the database
* Install default templates

Just run ``manage.py runserver``, go to http://localhost:8000 , login with user *admin* (same password)
and enjoy your first django CMS project.

More at `django CMS Tutorial`_ and `installer usage page`_

**************
Documentation
**************

For detailed information see https://djangocms-installer.readthedocs.io

************************************************
Preliminary checks and system libraries
************************************************

While this wizard try to handle most of the things for you, it doesn't check for
all the proper native (non python) libraries to be installed.
Before running this, please check you have the proper header and libraries
installed and available for packages to be installed.

Libraries you would want to check:

* libjpeg (for JPEG support in ``Pillow``)
* zlib (for PNG support in ``Pillow``)
* postgresql (for ``psycopg2``)
* libmysqlclient (for ``Mysql``)
* python-dev (for compilation and linking)

For additional information, check https://djangocms-installer.readthedocs.io/en/latest/libraries.html

******************
Supported versions
******************

The current supported version matrix is the following:

+----------------+--------------+--------------+---------------+
|                |  Django 2.2  | Django 3.0   | Django 3.1    |
+----------------+--------------+--------------+---------------+
| django CMS 3.7 | Supported    | Supported    | Not supported |
+----------------+--------------+--------------+---------------+
| django CMS 3.8 | Supported    | Supported    | Supported     |
+----------------+--------------+--------------+---------------+

See `version 1.2`_ for older Django / django CMS versions support

Any beta and develop version of Django and django CMS, by its very nature,
it's not supported, while it still may work.

``djangocms-installer`` tries to support beta versions of django CMS when they
are be considered sufficiently stable by the upstream project.

*******
Warning
*******

``djangocms-installer`` assumes that ``django-admin.py`` is installed in the same directory
as python executable, which is the standard virtualenv layout. Other installation layouts
might work, but are not officially supported.


***************
Windows support
***************

The installer is tested on Windows 10 with Python version 3.8.6 installed using
official MSI packages available at http://python.org.

Please check that the ``.py`` extension is associated correctly with Python interpreter::

    c:\> assoc .py
    .py=Python.File

    c:\>ftype Python.File
    Python.File="C:\Windows\py.exe" "%1" %*


.. _version 1.2: https://github.com/nephila/djangocms-installer/tree/release/1.2.x#supported-versions
.. _django CMS Tutorial: https://django-cms.readthedocs.io/en/latest/introduction/index.html
.. _installer usage page: http://djangocms-installer.readthedocs.io/en/latest/usage.html


.. |Gitter| image:: https://img.shields.io/badge/GITTER-join%20chat-brightgreen.svg?style=flat-square
    :target: https://gitter.im/nephila/applications
    :alt: Join the Gitter chat

.. |PyPiVersion| image:: https://img.shields.io/pypi/v/djangocms-installer.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-installer
    :alt: Latest PyPI version

.. |PyVersion| image:: https://img.shields.io/pypi/pyversions/djangocms-installer.svg?style=flat-square
    :target: https://pypi.python.org/pypi/djangocms-installer
    :alt: Python versions

.. |GAStatus| image:: https://github.com/nephila/djangocms-installer/workflows/Tox%20tests/badge.svg
    :target: https://github.com/nephila/django-app-helper
    :alt: Latest CI build status

.. |TestCoverage| image:: https://img.shields.io/coveralls/nephila/djangocms-installer/master.svg?style=flat-square
    :target: https://coveralls.io/r/nephila/djangocms-installer?branch=master
    :alt: Test coverage

.. |License| image:: https://img.shields.io/github/license/nephila/djangocms-installer.svg?style=flat-square
   :target: https://pypi.python.org/pypi/djangocms-installer/
    :alt: License

.. |CodeClimate| image:: https://codeclimate.com/github/nephila/djangocms-installer/badges/gpa.svg?style=flat-square
   :target: https://codeclimate.com/github/nephila/djangocms-installer
   :alt: Code Climate
