##############################################
SublimeText Configuration for LSST Development
##############################################

This page will help you configure `SublimeText <https://www.sublimetext.com/>`_ to be consistent with LSST's coding standards and development practices.
We recommend using `SublimeText 3 <https://www.sublimetext.com/3>`_, and installing `Package Control <https://packagecontrol.io/installation>`_ to manage the many useful SublimeText packages that are available.
See the `Package Control help <https://packagecontrol.io/docs/usage>`_ for usage, including the command to open the Command Palette on your system.
Play with the available color schemes until you find one you prefer: there are many to choose from.

.. _sublime_settings:

Settings
========

Here is a suggested settings file that will configure Sublime to match most LSST coding styles, plus some that are personal preference but show some of the settings that can be configured.
Particularly important are ``"detect_indentation": false,`` and ``"translate_tabs_to_spaces": true,``, which will keep your python and C++ code from gaining tabs.
The ``"rulers"`` setting doesn't affect actual indentation, but provides guides to help your own line length formatting.

.. code-block:: json

    {
        "bold_folder_labels": true,
        "caret_style": "phase",
        "detect_indentation": false,
        "draw_white_space": "selection",
        "enable_hexadecimal_encoding": false,
        "ensure_newline_at_eof_on_save": true,
        "file_exclude_patterns":
        [
            "*.a",
            "*.class",
            "*.db",
            "*.dll",
            "*.dylib",
            "*.exe",
            "*.idb",
            "*.lib",
            "*.ncb",
            "*.o",
            "*.obj",
            "*.os",
            "*.pdb",
            "*.psd",
            "*.pyc",
            "*.pyo",
            "*.sdf",
            "*.so",
            "*.suo",
            ".DS_Store",
        ],
        "index_exclude_patterns":
        [
        "*.dox",
        "*.html",
        "*.log",
        "*.xml"
        ],
        "folder_exclude_patterns":
        [
            ".git",
            ".hg",
            "__pycache__",
            ".sconf_temp",
            ".svn",
        ],
        "font face": "inconsolata-g",
        "font_options":
        [
            "subpixel_antialias"
        ],
        "font_size": 11,
        "highlight_modified_tabs": true,
        "indent_to_bracket": true,
        "open_files_in_new_window": true,
        "rulers":
        [
            79,
            110
        ],
        "translate_tabs_to_spaces": true,
        "wide_caret": true
    }

.. _sublime-general:

General
=======

To easily open files in SublimeText from the command-line, there is a ``subl`` `command-line helper <http://docs.sublimetext.info/en/latest/command_line/command_line.html>`_.

Some packages (installable via Package Control) that may help your development include,

* ``Git Gutter`` to put marks next to the line numbers that identify added/modified/removed lines since the last Git commit.
* ``OmniMarkupPreviewer`` to allow live-view of formatted reStructuredText, Markdown, and so on, in a web browser.

.. _sublime-cpp:

C++
===

The  :ref:`clang-format <using_clang_format>` plugin can help you automatically keep your C++ in line with the :doc:`/cpp/style`.
Once you have clang-format configured on your system, install the Sublime package with the Package Manager: `Clang Format <https://packagecontrol.io/packages/Clang%20Format>`_.

There are two required settings to make Clang Format find the binary and configuration file: ``"binary"`` and ``"style": "File"``.
On Ubuntu, ``binary`` should be ``clang-format-5.0``, while on macOS it should be ``/usr/local/bin/clang-format`` if you installed via `Homebrew <https://brew.sh>`_.
In addition, you configure your Clang Format (``clang-format.sublime-settings``) to automatically format on save.

.. code-block:: json

    {
        "binary": "clang-format-5.0",
        "format_on_save": true,
        "style": "File"
    }

You can also set C++ syntax-specific settings to override the general settings above.
Syntax-specific settings are defined by opening a file in the desired language and selecting ``Preferences -> Settings - Syntax-Specific``.
For example, to have only one ruler at the C++ boundary:

.. code-block:: json

    {
        "rulers": [110]
    }

These settings override both user and default settings for the C++ syntax.

.. _sublime-python:

Python
======

The built-in python syntax highlighting works well, but here are some potentially useful customizations:

.. _sublime-python-flake8:

SublimeLinter-flake8
--------------------

LSST :ref:`uses flake8 <style-guide-py-flake8>` to check that our python code conforms to our :doc:`/python/style`.
You can get SublimeText to check your python code inline and mark lines that do not follow our style with the `SublimeLinter <http://www.sublimelinter.com/en/latest/>`_ package.
Install ``SublimeLinter`` and ``SublimeLinter-flake8`` via Package Control (note: packages that are already installed won't show up in Package Control's "Install Package" list).
Use the following configuration to conform to LSST's python style, to mark failing lines, and to provide a summary of failures on save that will let you go directly to those lines.

Install ``flake8`` in the python that you will use for lsst development (typically your copy LSST-installed miniconda).
Set the ``executable`` parameter of ``SublimeLinter-flake8`` to the path to that ``flake8``.
Here is an example configuration for ``SublimeLinter`` and ``flake8``:

.. code-block:: text

    // SublimeLinter Settings - User
    {
        "linters": {
            "flake8": {
                "executable": "<your_miniconda_root_here>/miniconda/envs/lsst-scipipe/bin/flake8",
                "args": [
                    // from https://developer.lsst.io/python/testing.html#enabling-additional-pytest-options-flake8
                    "--max-line-length", "110",
                    "--ignore", "E133,E226,E228,N802,N803,N806",
                ],
            },
        },
        "show_panel_on_save": "view"
    }

Alternately, instead of configuring line length and the ignore list in SublimeText, you can configure it globally by creating a ``~/.config/flake8`` file:

.. code-block:: text

    [flake8]
    # from https://developer.lsst.io/python/testing.html#enabling-additional-pytest-options-flake8
    ignore = E133, E226, E228, N802, N803, N806
    max-line-length = 110

Note that there are SublimeLinter plugins for other languages (e.g. RestructuredText, yaml, javascript) as well.

.. _sublime-python-whitespace:

Whitespace
----------

The LSST python style guide follows PEP8, meaning 4-spaces, no TABs. The settings file given above will help you maintain this: SublimeText defaults to 4-stops Tabs.

To help find extra end-of-line spaces, install the ``Trailing Spaces`` Package.
An example configuration for it:

.. code-block:: json

    {
        "trailing_spaces_file_max_size": 100000,
        "trailing_spaces_highlight_color": "invalid",
        "trailing_spaces_include_current_line": false,
        "trailing_spaces_include_empty_lines": true
    }
