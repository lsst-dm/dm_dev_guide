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

.. _add_callable_cli_command_to_your_package:

Add a Callable CLI Command To Your Package
==========================================

If your callable command is implemented as described in :ref:`argparse-script-topic-type` with a single function loading from the package implementing the script, you can define the script in the `standard Python package approach using <https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#creating-executable-scripts>`_ ``pyproject.toml``.
For example, this:

.. code-block:: toml

   [project.scripts]
   exampleScript = "lsst.example.scripts.exampleScript:main"

will result in a executable file appearing in ``bin/exampleScript`` that will import ``main`` from ``lsst.example.scripts.exampleScript`` and call it.
This is the recommended way to define callable commands and all newly-written scripts should be defined this way.

If your script is monolithic and includes the implementation directly in the callable script and you cannot reorganize the code, you must instead write the command to a ``bin.src`` directory at the top level.
The directory should contain:

1. ``SConscript`` with contents:

   .. code-block:: py

       # -*- python -*-
       from lsst.sconsUtils import scripts
       scripts.BasicSConscript.shebang()

2. A file for each command that has the name of the CLI command the user will call.
   This file should have a Python shebang (``#!``) in the first line.

It is possible for a package to define some scripts in ``pyproject.toml`` and some scripts in ``bin.src`` but it is an error if a script is defined in both places.
