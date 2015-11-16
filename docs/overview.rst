Overview
=================================

Yummy is a package to simplify Market Mix Modelling in Python.
Yummy wraps up three main components data analysis, data modelling and data visualisation.
It is intended for use in the Jupyter notebook

.. code-block:: python
   >>> import yummy as ym
   >>> yo = ym.read_csv('https://raw.githubusercontent.com/kept-io/r-datasets/master/datasets/quantreg/engel.csv')
   >>> yo.data.corr()
   >>> yo.model.dep = 'income'
   >>> yo.model.add = 'foodexp'
   >>> yo.model.ols()


Where to Start
--------------
For new users please work carefully through the tutorial. The rest of the documentation will assume you’re at least passingly familiar with the material contained within.

Features
--------

* Transformations - Lag, Decay, Power, Atan

* Linear Regression Modelling - OLS, GLS, RLS

* Simultaneous Equations Modelling - VAR

* Flexible Plotting Functionality - Residual Plots, Contribution Charts, Line Charts 


License
-------

The project is licensed under the BSD license.
