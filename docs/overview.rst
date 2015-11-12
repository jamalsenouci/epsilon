Overview
=================================

Yummy is a package to simplify Market Mix Modelling in Python

Yummy wraps up three main components data analysis, data modelling and data visualisation.

It is intended for use in the Jupyter notebook

.. code-block:: python
   >>> import yummy as ym
   >>> yo = ym.read_csv('https://raw.githubusercontent.com/kept-io/r-datasets/master/datasets/quantreg/engel.csv')
   >>> yo.data.corr()
   >>> yo.model.dep = 'income'
   >>> yo.model.add = 'foodexp'
   >>> yo.model.ols()


Tutorial
--------
For new users, and/or for an overview of Yummy’s basic functionality, please see the Overview and Tutorial. The rest of the documentation will assume you’re at least passingly familiar with the material contained within.

Features
--------

* Transformations - Lag, Decay, Power, Atan

* Linear Regression Modelling - OLS, GLS, RLS

* Simultaneous Equations Modelling - VAR

* Flexible Plotting Functionality - Residual Plots, Contribution Charts, Line Charts 

Further Reading
---------------

The Python programming language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At it's core yummy is built in Python.
Python is a powerful programming language that actually makes sense. Equally important, Python is free, well-supported, and people enjoy using it.

Knowledge of Python is not essential and in fact the purpose of this project is to reduce the complexity of using python for modelling. However if you are looking to develop it then you will want to know how to write basic programs in Python. Among the many guides to Python, we recommend this python documentation: http://python.readthedocs.org/en/latest/

The Anaconda Distribution
~~~~~~~~~~~~~~~~~~~~~~~~~
The best way to get started with python is by downloading the anaconda distribution which downloads many useful libraries with it.
Read more about it here: http://conda.pydata.org/docs/index.html or download it here: https://www.continuum.io/downloads/

The Jupyter Notebook
~~~~~~~~~~~~~~~~~~~~
The editor that we use is called the jupyter notebook (previously IPython Notebook). It is both human readable and executable to allow for a fully documented workflow. It's always good to know how to use your gui so read more here: https://jupyter.readthedocs.org/en/latest/

Pandas
~~~~~~
Yummy's Data object builds heavily on pandas. A library that provides an efficient dataframe and data analysis functionality. Anything you can do with pandas dataframe you can also do with a yummy Data object.
Read more about that here: http://pandas.pydata.org/pandas-docs/version/0.17.0/tutorials.html

Bokeh
~~~~~
Yummy's plotting functionality is implemented using the bokeh library. A great library for interactive visualisations.
A gallery of charts with source code can be found here: http://bokeh.pydata.org/en/latest/docs/gallery.html

License
-------

The project is licensed under the BSD license.
