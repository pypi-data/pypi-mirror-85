uncertainties
=============

.. image:: https://readthedocs.org/projects/uncertainties-python-package/badge/?version=latest
   :target: http://uncertainties-python-package.readthedocs.io/en/latest/?badge=latest
.. image:: https://img.shields.io/pypi/v/uncertainties.svg
   :target: https://pypi.org/project/uncertainties/
.. image:: https://pepy.tech/badge/uncertainties/week
   :target: https://pepy.tech/badge/uncertainties/week
.. image:: https://codecov.io/gh/lebigot/uncertainties/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/lebigot/uncertainties/
.. image:: https://travis-ci.org/lebigot/uncertainties.svg?branch=master
   :target: https://travis-ci.org/lebigot/uncertainties
.. image:: https://ci.appveyor.com/api/projects/status/j5238244myqx0a0r?svg=true
   :target: https://ci.appveyor.com/project/lebigot/uncertainties

   
This is the ``uncertainties`` Python package, which performs **transparent
calculations with uncertainties** (aka "error propagation"):

    >>> from uncertainties import ufloat
    >>> from uncertainties.umath import *  # sin(), etc.
    >>> x = ufloat(1, 0.1)  # x = 1+/-0.1
    >>> print 2*x
    2.00+/-0.20
    >>> sin(2*x)  # In a Python shell, "print" is optional
    0.9092974268256817+/-0.08322936730942848

This package also automatically calculates derivatives:

    >>> (2*x+1000).derivatives[x]
    2.0

The main documentation is available at
http://uncertainties-python-package.readthedocs.io/.

Git branches
------------

The ``release`` branch is the latest stable release. It should pass the tests.


``master*`` branches in the Github repository are bleeding-edge, and do not
necessarily pass the tests. The ``master`` branch is the latest, relatively
stable versions (while other ``master*`` branches are more experimental).

Other branches might be present in the GitHub repository, but they are
typically temporary and represent work in progress that does not necessarily run
properly yet.

License
-------

This package and its documentation are released under the `Revised BSD
License <LICENSE.txt>`_.
