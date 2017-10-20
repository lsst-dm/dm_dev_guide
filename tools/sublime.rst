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
            "*.db"
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

* ``Git Gutter`` to put marks next to the line numbers that identify added/modified/removed lines since the last git commit.
* ``OmniMarkupPreviewer`` to allow live-view of formatted RestructuredText, MarkDown, etc. in a web browser.

.. _sublime-cpp:

C++
===

The  :ref:`clang-format <using_clang_format>` plugin can help you automatically keep your C++ in line with the DM coding style.
Once you have clang-format configured on your sytem, install the Sublime package with the Package Manager: `Clang Format <https://packagecontrol.io/packages/Clang%20Format>`_.

There are two required settings to make Clang Format find the binary and configuration file: ``"binary"`` and ``"style": "File"``.
On Ubuntu, ``binary`` should be ``clang-format-5.0``, while on macOS it should be ``/usr/local/bin/clang-format`` if you installed via homebrew.
In addition, you configure your Clang Format (``clang-format.sublime-settings``) to automatically format on save.

.. code-block:: json

    {
        "binary": "clang-format-5.0",
        "format_on_save": true,
        "style": "File"
    }

You can also set C++ syntax-specific settings to override the general settings above.
Syntax-specific settings are defined by opening a file in the desired language and selecting `Preferences->Settings - Syntax-Specific`.
For example, to have only one ruler at the C++ boundary:

.. code-block:: json

    // These settings override both User and Default settings for the C++ syntax
    {
        "rulers": [110]
    }

.. _sublime-python:

Python
======

The built-in python syntax highlighting works well, but here are some potentially useful customizations:

.. _sublime-python-flake8:

SublimeLinter-flake8
--------------------

LSST uses ``flake8`` to check that our python code conforms to our :ref:`style guide <style-guide-py-version>`.
You can get SublimeText to check your python code inline and mark lines that do not follow our style with the `SublimeLinter <http://www.sublimelinter.com/en/latest/>`_ package.
Install ``SublimeLinter`` and ``SublimeLinter-flake8`` via Package Control.
Use the following configuration to conform to LSST's python style, to mark failing lines, and to provide a summary of failures on save that will let you go directly to those lines.


You may have to `configure your PATH <http://www.sublimelinter.com/en/latest/usage.html#how-linter-executables-are-located>`_ to allow SublimeText to find the ``flake8`` executable.


Note that there are SublimeLinter plugins for other languages (e.g. RestructuredText, yaml, javascript) as well.

.. code-block:: json

    {
        "user": {
            "debug": false,
            "delay": 0.25,
            "error_color": "D02000",
            "gutter_theme": "Packages/SublimeLinter/gutter-themes/Default/Default.gutter-theme",
            "gutter_theme_excludes": [],
            "lint_mode": "background",
            "linters": {
                "flake8": {
                    "@disable": false,
                    "args": [],
                    "builtins": "",
                    "excludes": [],
                    "executable": "",
                    "ignore": "E133,E226,E228,E251,N802,N803,N806,W391",
                    "jobs": "1",
                    "max-complexity": -1,
                    "max-line-length": 110,
                    "select": "",
                    "show-code": false
                },
            },
            "mark_style": "outline",
            "no_column_highlights_line": false,
            "passive_warnings": false,
            "paths": {
                "linux": [],
                "osx": [],
                "windows": []
            },
            "python_paths": {
                "linux": [],
                "osx": [
                    ""
                ],
                "windows": []
            },
            "rc_search_limit": 3,
            "shell_timeout": 10,
            "show_errors_on_save": true,
            "show_marks_in_minimap": true,
            "syntax_map": {
                "html (django)": "html",
                "html (rails)": "html",
                "html 5": "html",
                "php": "html",
                "python django": "python"
            },
            "tooltip_fontsize": "1rem",
            "tooltip_theme": "Packages/SublimeLinter/tooltip-themes/Default/Default.tooltip-theme",
            "tooltip_theme_excludes": [],
            "tooltips": false,
            "warning_color": "DDB700",
            "wrap_find": true
        }
    }


 ``Python PEP8 Autoformat`` lets one bulk reformat a number of python files to match a style.
 Use these settings to match LSST's python style when auto formatting:

.. code-block:: json

    {
        // list codes for fixes; used by --ignore and --select
        "list-fixes": true,
        // do not fix these errors / warnings (e.g. [ "E501" , "E4" , "W"])
        // LSST style;
        "ignore": ["E133", "E226", "E228", "E251", "N802", "N803", "W391"],
        // Maximum line length
        "max-line-length": 110
    }

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
