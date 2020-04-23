##############################
Python Command Line Interfaces
##############################

Command line interfaces in Python may be implemented using the ``argparse`` module or using `Click`_.

.. _Click: https://click.palletsprojects.com

.. _cli-using-click:

Command Line Interfaces using Click
===================================

Click is a Python package for creating command line interfaces in a composable way. It supports:

* arbitrary nesting of commands
* automatic help page generation
* lazy loading of subcommands at runtime

`Click`_ has good `documentation`_ including a `quickstart`_ guide.

.. _documentation: https://click.palletsprojects.com/en/7.x/#documentation
.. _quickstart: https://click.palletsprojects.com/en/7.x/quickstart/

Callable CLI Command
--------------------

To create a callable command e.g. ``$ butler ...``, at the top level of your package create a folder
called ``bin.src``, it should contain two files:

1. ``SConscript`` with contents:

.. code-block:: py

    # -*- python -*-
    from lsst.sconsUtils import scripts
    scripts.BasicSConscript.shebang()

2. A file that has the name of the CLI command the user will call. This file should contain as little
   implementation as possible, it should import an implementation file and call a function in it. For example:

.. code-block:: py

    import sys
    from lsst.daf.butler.cli.butler import main

    if __name__ == '__main__':
        sys.exit(main())

All implementation should be placed in a folder called ``cli`` ("command line interface") under
``<package name>/python/lsst/package/name/cli``, and the implementation of the command should go in a file
in ``cli``, e.g. ``cli/butler.py``.





* CLI utilities should go a in a file ``cli/utils.py``.



.. _click-commands:

Click Command
-------------

`Commands`_ are like the subcommand ``pull`` in ``git pull``. They are implemented as functions, and declared
by decorating the function with ``@click.command``

.. _Commands: https://click.palletsprojects.com/en/7.x/commands/

.. code-block:: py
   :name: command-example

    @click.command
    def pull():
        ...

`Commands`_ that can be executed by the top-level script should go in a ``cmd`` folder inside ``cli``, e.g.
``python/lsst/package/name/cli/cmd/my_command.py``.

.. _click-options:

Click Options
-------------

Options are like the ``-a`` and the ``-m <msg>`` in ``git commit -a -m <msg>``. They are declared by adding
decorators to Command functions.

.. code-block:: py
   :name: option-example

    @click.command
    @click.option(-a, --all, is_flag=True)
    @click.option(-m, --message)
    def commit(all, message):
        ...

.. _click-shared-options:

Shared Options
~~~~~~~~~~~~~~

Options can be shared and should be used to improve consistency and reduce code duplication. To maximize
reusability, shared Options should be placed in a package that is as high in the dependcy tree as is
reasonable for that option. By convention the option should go in its own file at
``python/lsst/package/name/cli/opt/<option_name>.py``.

Two common ways to create a shared option are:

1. Use a function to return an option decorator with preset values:

.. code-block:: py
   :name: simple-shared-option

    def all_option(f):
        return click.option("-a", "--all",
                            is_flag=True,
                            help="Tell the command to automatically stage files that have been modified and "
                            "deleted, but new files you have not told Git about are not affected."'")(f)

2. Use a class to accept values to pass to the click option:

.. code-block:: py
   :name: shared-option-with-parameters

    class message_option:  # noqa: N801
        def __init__(self, help=None):
            self.help = "help if help is not None else "Use the given <msg> as the commit message. If "
                        "multiple -m options are given, their values are concatenated as separate paragraphs."

        def __call__(self, f):
            return click.option("-m", "--message",
                                help=self.help)(f)

These optons can be used like so:

.. code-block:: py

    from ..opt import all_option, message_option

    @click.command
    @all_option
    @message_option(help="My help message.")
    def commit(message):
        ...


Why noqa: N801?
"""""""""""""""

The `PEP8 section on class names`_ says class names should use the CapWords convention, but for a decorator
this is unexpected. Consider the above example using CapsWords:

.. _PEP8 section on class names: https://www.python.org/dev/peps/pep-0008/#class-names

.. code-block:: py

    @click.command
    @all_option
    @MessageOption(help="My help message.")
    def commit(message):
        ...

Using lowercase and underscores instead of CapWords results in more consistent decorator naming.


Click Arguments
---------------

Arguments are unnamed parameters like ``my_branch`` in ``git checkout my_branch``.


Shared Arguments
~~~~~~~~~~~~~~~~

Arguments can be shared, similar to options, and by convention should go in separate files under ``arg``, like
``python/lsst/package/name/cli/arg/<arg_name>.py``.


Naming
------

Use hypens for the cli invocation. Use underscores for the implementation. TODO flesh out.


## Section for Butler scripts ##

Commands are imported by the top-level butler script.


``daf_butler`` has a top-level script that imports commands. TODO explain ``DAF_BUTLER_PLUGINS`` and to put the path
to the ``cmd`` folder, and to make those commands available by the ``__init__.__all__`` in that folder.

## WTD for non-Click scripts? ## (b/c I don't know anything about them)


