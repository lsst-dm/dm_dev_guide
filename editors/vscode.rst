#####################################################
Visual Studio Code Configuration for LSST Development
#####################################################

This page will help you configure `Visual Studio Code (VSCode) <https://code.visualstudio.com/>`_ to be consistent with LSST's coding standards and development practices.

.. _vscode_extensions:

Extensions
==========

As with most advanced editors, a lot of VSCode's functionality comes from extensions, which can be installed directly from the editor GUI.

The official (Microsoft-maintained) extensions generally have quite good documentation, and this guide does not attempt to duplicate anything that can be found there.

.. note::
    Adding an extension to VSCode does not always automatically enable it when editing files remotely.
    When you first open a remote editing window on a particular server, you should check your extensions to ensure the ones you need are installed and enabled there.


Extensions useful specifically for LSST development
---------------------------------------------------

`Python <https://code.visualstudio.com/docs/languages/python>`_:
    The official Python extension, from Microsoft.  See :ref:`vscode-python`.

`C/C++ <https://code.visualstudio.com/docs/languages/cpp>`_:
    The official C++ extension, from Microsoft.  See :ref:`vscode-cpp`.

`Latex Workshop <https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>`_:
    Useful for writing Latex docs.

`restructuredText <https://docs.restructuredtext.net/>`_:
    Useful for writing Sphinx docs.

`Remote Development, Remote - SSH <https://code.visualstudio.com/docs/remote/ssh>`_:
    Provides support for editing, browsing, and debugging code on a remote server from a local editor, over SSH.

`Trailing Spaces <https://marketplace.visualstudio.com/items?itemName=shardulm94.trailing-spaces>`_:
    Highlights and/or deletes trailing spaces, which Flake8 will otherwise complain about.

`Python Indent <https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent>`_:
    As of this writing, VSCode's automatic indentation for Python isn't very good.
    This extension makes it a lot better - still not as good as (at least) Emacs or Sublime, but good enough that the difference is rarely noticeable.


General extension recommendations from LSST developers
------------------------------------------------------

`Bracket Pair Colorizer <https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer>`_:
    Keep track of parentheses/bracket/brace pairs using colors.

`Clipboard Ring <https://marketplace.visualstudio.com/items?itemName=SirTobi.code-clip-ring>`_:
    Remembers the last few things you've copy/pasted; a very limited version of what (at least) Emacs does.

`Git Graph <https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph>`_:
    An in-editor, easy-to-read version of ``git log --graph``.

`Git Lens <https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens>`_:
    In-editor ``git blame`` annotation and more.

`Rewrap <https://marketplace.visualstudio.com/items?itemName=stkb.rewrap>`_
    Hard-wrapping of full paragraphs.  Unfortunately tends to be a bit aggressive in the context I want it most - wrapping elements of the Parameters section of Python docstrings - but much better than nothing, which strangely seems to be what VSCode ships with.

`Transpose <https://marketplace.visualstudio.com/items?itemName=v4run.transpose>`_:
    Swap the letters on either side of the cursor, which you may have gotten addicted to from other editors.


.. _vscode_settings:

Settings
========

Here is a suggested settings file that will configure VSCode to match most LSST coding styles and ignore common temporary files our builds produce.
This includes settings for some of the extensions recommended above.
The ``"rulers"`` setting doesn't affect actual indentation (unless you use the ``Rewrap`` extension or similar), but provides guides to help your own line length formatting.

.. code-block:: json

    {
        "editor.rulers": [
            80,
            110
        ],
        "files.exclude": {
            "**/__pycache__": true,
            "**/.coverage.*": true,
            "**/.pytest_cache": true,
            "**/.sconf_temp": true,
            "**/.sconsign.dblite": true,
            "**/.tests": true,
            "**/*.o": true,
            "**/*.os": true
        },
        "files.watcherExclude": {
            "**/__pycache__": true
        },
        "trailing-spaces.trimOnSave": true,
        "restructuredtext.linter.extraArgs": [
            "--ignore D001"
        ],
        "[restructuredtext]": {
            "editor.wordWrap": "wordWrapColumn",
        },
        "python.linting.flake8Enabled": true,
        "python.linting.pylintEnabled": false,
        "search.useGlobalIgnoreFiles": true,
        "python.dataScience.enabled": false,
        "latex-workshop.latex.external.build.command": "make",
        "[cpp]": {
            "editor.defaultFormatter": "ms-vscode.cpptools"
        }
    }

.. _vscode-python:

Python
======

The official Python extension includes linting, symbol lookup, and integrated debugging, as long as it is configured to use the right Python executable and module search path.
VSCode automatically searches for conda environments, and generally does a good job of guessing the right one.
When it guesses wrong, it's easy to change via the GUI (and presumably more permanent configuration).
Using the right conda environment (and the above configuration to use ``flake8`` instead of ``pylint``) should be enough enable in-editor linting with LSST configuration (as long as that configuration is in the package's ``setup.cfg``, as usual).

However, the best features of VSCode require providing it full information about the Python environment, which for us is usually managed by EUPS as well as conda.
One way to do this that works even with remote editing is to use something like the following script to dump EUPS-managed environment variables to a ``.env`` file in the workspace directory::

    #!/usr/bin/env python

    import os
    import argparse

    BASE_VARIABLES = ("PATH", "PYTHONPATH", "LD_LIBRARY_PATH")


    def main(filename, variables):
        variables = list(variables)
        variables.extend(var for var in os.environ
                        if (var.endswith("DIR")
                            and f"SETUP_{var[:-4]}" in os.environ))
        with open(filename, "w") as f:
            for var in variables:
                f.write(f"{var}={os.environ[var]}\n")


    if __name__ == "__main__":
        parser = argparse.ArgumentParser(
            description=("Write selected variables from the current environment "
                        "into a Visual Studio Code environemnt files.")
        )
        parser.add_argument("-f", "--filename", default=".env",
                            help="Filename to write")
        parser.add_argument("-v", "--variable", default=list(BASE_VARIABLES),
                            action="append", dest="variables",
                            help=("An additional variables to export; may be "
                                  "provided multiple times."))
        args = parser.parse_args()
        main(args.filename, args.variables)

While this unfortunately adds another step (and a bit of fragility) to typical developer workflow, the benefits are substantial:

 - Python scripts can be debugged from within the editor by opening the script file, adding ``breakpoint()`` somewhere, and starting the in-editor debugger on that file (e.g. via ``F5``).
   Local variables are automatically shown in the GUI (it's remarkable how much faster this is than asking ``pdb`` to print individual variables), and you can toggle additional breakpoints visually while looking directly at the code.

 - Directly imported symbols - and local variables/arguments with type annotations - are fully recognized; you can get docstrings, jump to definitions, and even see function signatures overlaid as you type.

Most importantly, all of this is available during remote editing; while you may need to restart the editor after you first connect to a remote directory (after you enable/install remote extensions, and then to write the ``.env`` file to the workspace directory), the rest is fairly automatic, including remote debugging of scripts.

You can also install the ``ptvsd`` tool on the server manually (it's available via ``pip``) to launch Python code from another terminal that VSCode can later attach to.
This also requires setting up some SSH tunnels (see [instructions in the VSCode Python docs](https://code.visualstudio.com/docs/python/debugging#_remote-debugging) for more information), but it can be very useful for debugging more complex or long-running Python processes.


.. _vscode-cpp:

C++
===

The official C++ extension includes support for clang-format, and it should work out of the box as long as you've installed ``clang-format`` and put a ``.clang-format`` file in a root directory of your source tree (see :ref:`using_clang_format`).
Automatically formatting on save or while editing can be enabled via the ``editor.formatOnSave`` and ``editor.formatOnType`` options, but note that these are global settings, and will apply to any language for which a formatter is configured, unless the overrides are [explicitly marked as language-specific](https://vscode.readthedocs.io/en/latest/getstarted/settings/).

As with Python, many C++ features require giving VSCode more information about the development environment - in this case, include paths - than it can typically discover automatically.
Normal editing and formatting will still work, but most tab-completion, type symbol lookup, and debug support will be missing, and the built-in linter will produce a lot of distracting squiggles and other warnings.
Unlike Python, our way of declaring include paths to ``sconsUtils`` makes fixing this quite difficult in general.
An experimental (but still unsatisfactory) solution is to use the ``tickets/DM-22074`` branch of ``sconsUtils`` to build the package *from scratch* with:

.. code-block:: sh

    scons lib python tests compile_commands.json [other options and targets]

This will create a CMake-style file that VSCode can use to find missing headers.
Rebuilds that do not add or remove files can then be done by running ``scons`` without the ``compile_commands.json`` target (with whatever targets you would normally use).
Unfortunately, any time the ``compile_commands.json`` target is included, the file will be overwritten with information about only the files being compiled in that invocation.
