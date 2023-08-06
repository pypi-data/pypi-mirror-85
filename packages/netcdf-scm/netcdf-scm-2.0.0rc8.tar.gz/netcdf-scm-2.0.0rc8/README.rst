.. image:: https://gitlab.com/netcdf-scm/netcdf-scm/raw/master/docs/source/_static/logo.png
   :height: 50px
   :width: 100px
   :alt: Logo


netCDF-SCM
==========

+--------+-------------------+-------------+-----------+--------+-----------------+
| Basics | |Python Versions| | |Platforms| | |License| | |Docs| | |Conda install| |
+--------+-------------------+-------------+-----------+--------+-----------------+

+-----------+--------------+----------+
| Citations | |JOSS paper| | |Zenodo| |
+-----------+--------------+----------+

+-------------------+----------------+-----------+
| Repository health | |Build Status| | |Codecov| |
+-------------------+----------------+-----------+

+-----------------+------------+--------+
| Latest releases | |Anaconda| | |PyPI| |
+-----------------+------------+--------+

.. sec-begin-index

netCDF-SCM is a Python package for processing netCDF files.
It focusses on metrics which are relevant to simple climate models and is built on top of the Iris_ package.

.. _Iris: https://github.com/SciTools/iris

.. sec-end-index

License
-------

.. sec-begin-license

netCDF-SCM is free software under a BSD 3-Clause License, see `LICENSE <https://github.com/znicholls/netcdf-scm/blob/master/LICENSE>`_.
If you make any use of netCDF-SCM, please cite `The Journal of Open Source Software (JOSS) <http://joss.theoj.org/>`_ paper [insert reference here when written...] as well as the relevant `Zenodo release <https://zenodo.org/search?page=1&size=20&q=netcdf-scm>`_.

.. sec-end-license

.. sec-begin-installation

Installation
------------

The easiest way to install netCDF-SCM is with `conda <https://conda.io/miniconda.html>`_

::

    # if you're using a conda environment, make sure you're in it
    conda install -c conda-forge netcdf-scm

It is also possible to install it with `pip <https://pypi.org/project/pip/>`_

::

  # if you're using a virtual environment, make sure you're in it
  pip install netcdf-scm

However installing with pip requires installing all of Iris_'s dependencies yourself which is not trivial.
As far as we know, Iris_ cannot be installed with pip alone.

.. _Iris: https://github.com/SciTools/iris

.. sec-end-installation

Documentation
-------------

Documentation can be found at our `documentation pages <https://netcdf-scm.readthedocs.io/en/latest/>`_ (we are thankful to `Read the Docs <https://readthedocs.org/>`_ for hosting us).

Contributing
------------

Please see the `Development section of the docs <https://netcdf-scm.readthedocs.io/en/latest/development.html>`_.

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/netcdf-scm.svg
    :target: https://pypi.org/project/netcdf-scm/
.. |Platforms| image:: https://anaconda.org/conda-forge/netcdf-scm/badges/platforms.svg
    :target: https://anaconda.org/conda-forge/netcdf-scm
.. |License| image:: https://img.shields.io/badge/license-BSD_3-blue
    :target: https://gitlab.com/netcdf-scm/netcdf-scm/blob/master/LICENSE
.. |Docs| image:: https://readthedocs.org/projects/netcdf-scm/badge/?version=latest
    :target: https://netcdf-scm.readthedocs.io/en/latest/
.. |Conda install| image:: https://anaconda.org/conda-forge/netcdf-scm/badges/installer/conda.svg
    :target: https://conda.anaconda.org/conda-forge
.. |JOSS Paper| image:: https://joss.theoj.org/papers/paper-code/status.svg
    :target: https://joss.theoj.org/papers/paper-code
.. |Zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3902224.svg
    :target: https://doi.org/10.5281/zenodo.3902224
.. |Build Status| image:: https://gitlab.com/netcdf-scm/netcdf-scm/badges/master/pipeline.svg
    :target: https://gitlab.com/netcdf-scm/netcdf-scm
.. |Codecov| image:: https://gitlab.com/netcdf-scm/netcdf-scm/badges/master/coverage.svg
    :target: https://gitlab.com/netcdf-scm/netcdf-scm/commits/master
.. |Anaconda| image:: https://anaconda.org/conda-forge/netcdf-scm/badges/version.svg
    :target: https://anaconda.org/conda-forge/netcdf-scm
.. |PyPI| image:: https://img.shields.io/pypi/v/netcdf-scm.svg
    :target: https://pypi.org/project/netcdf-scm/

.. [Morin et al. 2012]: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002598
