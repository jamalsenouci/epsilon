.. Yummy documentation master file, created by
   sphinx-quickstart on Wed Jul 15 06:29:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Yummy documentation
=================================

Yummy is a package to simplify Market Mix Modelling in Python

Yummy wraps up three main components data analysis, data modelling and data visualisation.

It is intended for use in the IPython notebook

.. code-block:: python
   >>> import yummy as ym
   >>> yo = ym.read_csv('https://raw.githubusercontent.com/kept-io/r-datasets/master/datasets/quantreg/engel.csv')
   >>> yo.data.corr()
   >>> yo.model.dep = 'income'
   >>> yo.model.add = 'foodexp'


Tutorial
--------
For new users, and/or for an overview of Yummy’s basic functionality, please see the Overview and Tutorial. The rest of the documentation will assume you’re at least passingly familiar with the material contained within.

Features
--------

Transformations - Lag, Decay, Power, Atan

Linear Regression Modelling - OLS, GLS




License
-------

The project is licensed under the GPL license.


Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

