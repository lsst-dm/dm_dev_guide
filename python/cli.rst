##############################
Python Command Line Interfaces
##############################

Command line interfaces (CLI) in Python may be implemented using the `argparse`_ module or using `Click`_.

.. _argparse: https://docs.python.org/3/library/argparse.html

.. _Click: https://click.palletsprojects.com


.. _cli-using-click:

Command Line Interfaces using Click
===================================

Click is a Python package for creating command line interfaces in a composable way.
It uses a declarative syntax that makes it easy to create CLI commands and easy and to understand them later.
However to use Click, the Click package must be installed.

Read more in the `Click quickstart`_ guide and `Click documentation`_.

.. _Click documentation: https://click.palletsprojects.com/en/7.x/#documentation
.. _Click quickstart: https://click.palletsprojects.com/en/7.x/quickstart/

Command Line Interfaces using argparse
======================================

Argparse is included in the python standard library and so does not require any additional packages.
It uses an imparative syntax.

Read more in the `argparse documentation`_.

.. _argparse documentation: https://docs.python.org/3/library/argparse.html

Add a Callable CLI Command To Your Package
==========================================

To create a callable command at the top level of your package create a folder called ``bin.src``.
It should contain two files:

1. ``SConscript`` with contents:

   .. code-block:: py

       # -*- python -*-
       from lsst.sconsUtils import scripts
       scripts.BasicSConscript.shebang()

2. A file that has the name of the CLI command the user will call.
   This file should contain as little implementation as possible.
   The ideal simplest case is to import an implementation function and call it.
   This makes the implementation testable and reusable.

