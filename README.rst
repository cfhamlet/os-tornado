==========
os-tornado
==========

.. image:: https://travis-ci.org/cfhamlet/os-tornado.svg?branch=master
   :target: https://travis-ci.org/cfhamlet/os-tornado

.. image:: https://codecov.io/gh/cfhamlet/os-tornado/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/cfhamlet/os-tornado

A framework to simplify tornado daemon development 
and project orgnization.

Requirements
-------------

* Python2.7
* Works on Linux

Install
-------
  ``pip install os-tornado``

Usage
------

* Create project

  ``os-tornado startproject new_project``
  
  Will create a project structure::

    new_project/
    ├── app
    │   ├── extensions
    │   │   ├── example_extension.py
    │   │   ├── __init__.py
    │   ├── request_handlers
    │   │   ├── example_handler.py
    │   │   ├── __init__.py
    │   ├── __init__.py
    │   ├── settings.py
    └── manager.py

* Write your extensions and request handlers

  * Extension

    You can implement ``setup``, ``run``, ``cleanup`` for your need.
  
  * Request handler

    See `tornado.web — RequestHandler and Application classes <http://www.tornadoweb.org/en/stable/web.html>`_

    You can get extension inside request handler:

    ``self.application.manager.get_extenion(extension_name)``

* Configure settings (app/settings.py)

* Run server

  ``python manager runserver``


Unit Tests
----------
  ``$ tox``

License
--------
MIT licensed.