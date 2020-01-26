.. pyriodic documentation master file, created by
   sphinx-quickstart on Sun Jan 26 12:10:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyriodic's documentation!
====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

`pyriodic <https://github.com/klarh/pyriodic>`_ is an in-development
library to handle a database of three-dimensional structures. It also
supports several simple manipulations of structures.

Installation
------------

Install `pyriodic` from source on github::

  pip install git+https://github.com/klarh/pyriodic.git#egg=pyriodic-structures

By default, pyriodic only ships with a few very simple structures;
other libraries can be added by installing other packages, such as
`pyriodic-aflow <https://github.com/klarh/pyriodic-aflow>`_, which
contains structures from the `AFLOW <http://aflowlib.org/>`_ project.

API Reference
=============

.. automodule:: pyriodic
   :members: Database, Structure

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
