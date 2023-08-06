ocp-modules
===========

This library provides a set of modules to assemble optimal control problems (OCPs) by generating
symbolic expressions based on `CasADi <https://web.casadi.org/>`_. The documentation is generated
via Sphinx and can be found `here <docs/build/html/index.html>`_.

Installation
------------

For Users
~~~~~~~~~
ocp-modules is (SOON) available via `pip`:

    .. code-block:: bash

        pip3 install --user ocp-modules

For Developers
~~~~~~~~~~~~~~
1. Install :code:`setuptools` and :code:`virtualenv`:

    .. code-block:: bash

        pip3 install --user setuptools virtualenv

2. Create a new virtual environment in the folder `venv` and source it:

    .. code-block:: bash

        git clone <this_repo>
        cd <this_repo>
        python3 -m virtualenv venc
        source ./venv/bin/activate

3. Install ocp-modules via symlink into the virtual environment

    .. code-block:: bash

        cd <this_repo>
        pip3 install -e .

A note regarding CasADi
~~~~~~~~~~~~~~~~~~~~~~~

Casadi can make use of proprietary solvers such as
`HSL MA57 <http://www.hsl.rl.ac.uk/catalogue/ma57.html>`_. Follow the instructions
`here <https://github.com/casadi/casadi/wiki/Obtaining-HSL>`_ to install them and modify the solver
options to use the built-in default.

Common issues with HSL solvers:

* Cannot find :code:`libhsl.so`. In this case, manually create a symlink :code:`libcoinhsl.so` ->
  :code:`libhsl.so` in :code:`/usr/lib`
* Failed to load :code:`libmetis.so`: It is hard to get a working instance of metis (the version packaged
  in Ubuntu 18.04 is not compatible). It seems to work without, but spams into stdout.

Running the examples
--------------------
Run examples via:

    .. code-block:: bash

        ./examples/<folder>/<script>.py