.. _formatting-python-code:

####################################
Formatting Python Code Automatically
####################################

The Python ecosystem provides two packages that can simplify automated code formatting and are used by some software products.
These tools are compliant with the :ref:`Rubin style guide <style-guide-py-pep8-baseline>` and can be adopted for any repository.
The main caveat is that once this tooling is adopted for a specific repository, use of the tooling must be required for all subsequent pull requests and checked using GitHub Actions.
This ensures that the code only goes through a style change for the initial adoption of the tooling.

Ordering imports
================

The `isort <https://pycqa.github.io/isort/>`_ package can be used to reorder imports in your Python code such that they are in alphabetical order and distinguish core python packages from other packages.

.. code-block:: bash

    $ isort python

Formatting Python Code
======================

We recommend the use of the `black <https://black.readthedocs.io/en/stable/index.html>`_ command for reformatting Rubin Python code once it has been decided that a repository should be converted.
Black calls itself the "uncompromising code formatter" and its entire purpose is to remove discussions of style from the debate.
You can write the code however you want in your editor but when ``black`` runs on it there is no room for debate.
For this reason configuration options are limited.
The only configuration option that is recommended is to control the line length to meet the Rubin coding style.

``black`` is not compatible with the E203 error from Flake8.
Consequently any project using ``black`` should disable E203.

Both ``black`` and ``isort`` can be configured by using a file ``pyproject.toml`` in the repository root:

.. literalinclude:: examples/pyproject.toml
  :language: toml

The only configuration sets the line length and Python version, with ``isort`` configured to be compatible with ``black``.

Installation
============

``isort`` and ``black`` are both available from conda-forge and can be installed directly into a conda environment:

.. code-block:: bash

    $ mamba install black isort

Of course they can also be installed using ``pip``.
They are not currently part of the default ``rubin-env`` conda environment.

Once installed it is possible to configure editors to automatically apply these tools on save but care must be taken that this ability is not enabled globally.

GitHub Actions
==============

When a repository is migrated to ``black`` and ``isort`` a GitHub Action should be installed.
A suitable Action ``py-formatting.yaml`` is included in the `LSST action templates repository <https://github.com/lsst/.github>`_.
It may need to be adjusted if there is no ``bin.src`` directory.

Using pre-commit
================

To prevent a situation where code is being pushed to a repository and then being flagged immediately because it has not been formatted, the `pre-commit <https://pre-commit.com>`_ command can be extremely useful.
This framework sets up a ``git`` pre-commit hook and will run checks whenever ``git commit`` is run.
If it finds a problem it will fix the code and let you try the commit again.
It can be installed directly from conda-forge.

To use ``pre-commit`` the repository must be configured by including a file called ``.pre-commit-config.yaml`` in the repository root directory.
The content describes which checks should be applied to every commit.
The one in ``daf_butler`` looks like:

.. literalinclude:: examples/pre-commit-config.yaml
  :linenos:
  :language: yaml

This example runs ``black`` and ``isort`` to check the formatting, removes trailing whitespace, lints any YAML files, and also ensures each file ends in a new line.

The checks can be enabled with:

.. code-block:: bash

    $ pre-commit install
    pre-commit installed at .git/hooks/pre-commit

``pre-commit`` installs everything it needs and ensures that the versions of the tools match the versions in the repository configuration file.
There is no need to install ``black`` or ``isort`` if you are relying on the pre-commit hook (which can be forced to run manually).
Running ``git commit`` looks something like this if there is a problem:

.. code-block:: bash

    $ git commit
    Check Yaml...........................................(no files to check)Skipped
    Fix End of Files.........................................................Passed
    Trim Trailing Whitespace.................................................Passed
    black....................................................................Failed
    - hook id: black
    - files were modified by this hook

    reformatted python/lsst/daf/butler/core/utils.py

    All done! ✨ 🍰 ✨
    1 file reformatted.

    isort (python)...........................................................Passed

In this situation the reformatted file will be present in the repository and ``git diff`` will show the change.
