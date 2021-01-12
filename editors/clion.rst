#####################################################
Using CLion for LSST Development
#####################################################

This page will help you configure `CLion <https://www.jetbrains.com/clion//>`_ to be consistent with LSST's coding standards and development practices.

Creating a Compilation Database
===============================

Installing Bear
---------------

`Bear <https://github.com/rizsotto/Bear/>`_ version 2.4.3 can be used to create a compilation database
from a scons run.

.. note::
    Bear version 3 and up have more complex external dependencies.


.. _clion-bear:

Running bear with scons
-----------------------
.. code-block:: sh

    bear scons [other options targets]

Importing to CLion
------------------
This will create ``compile_commands.json``, which can be opened
with CLion to edit, analyze and (re-)compile individual files with CLion.
``compile_commands.json`` does not provide any link information so executables and libraries cannot be built.
To allow a complete build the above shell command can be wrapped into a Makefile and imported to CLion.

.. code-block:: text

    all:
        bear scons
    clean:
        scons -c
    .PHONY: all clean

