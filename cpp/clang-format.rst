.. _using_clang_format:

#######################################
Using clang-format for LSST Development
#######################################

The easiest way to comply with the :ref:`LSST code layout rules <style-guide-cpp-6-1>` is to use `clang-format <http://clang.llvm.org/docs/ClangFormat.html>`_.
We require clang-format version 5.0, for formatting consistency (earlier versions may format some lines subtly differently).

Linux
=====

Ubuntu users can install this tool through the Ubuntu package manager.
Version 5.0 is not available in the default Xenial or Zesty repositories.
You can get it from the `llvm apt repository <http://apt.llvm.org/>`_, using the 5.0 repository (qualification branch).
If you've already installed ``clang-format-3.8`` (Ubuntu's default version), uninstall it before proceeding.
Follow these commands to add the appropriate apt source line for your Ubuntu version and install it using either the Xenial (16.04):

.. code-block:: bash

    echo "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-5.0 main" | sudo tee /etc/apt/sources.list.d/llvm.list
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add -
    sudo apt update
    sudo apt install clang-format-5.0

or Zesty (17.04) commands:

.. code-block:: bash

    echo "deb http://apt.llvm.org/zesty/ llvm-toolchain-zesty-5.0 main" | sudo tee /etc/apt/sources.list.d/llvm.list
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add -
    sudo apt update
    sudo apt install clang-format-5.0

This will install the ``clang-format-5.0`` binary, but will not symlink it to `clang-format`.
To create a system-managed symlink ("alternative"), use the following command:

.. code-block:: bash

    sudo update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-5.0 1

macOS
=====

On macOS, install clang-format through `Homebrew <http://brew.sh>`_:

.. code-block:: bash

    brew install clang-format

For more platforms see `here <http://releases.llvm.org/download.html>`_.

General
=======

Place the following configuration file, named ``.clang-format``, in your top-level source directory. For example, if you keep your lsst-related code in ``~/lsst/``, put the file in that directory.

.. code-block:: yaml

    ---
    Language: Cpp
    BasedOnStyle: Google
    ColumnLimit: 110
    IndentWidth: 4
    AccessModifierOffset: -4
    SortIncludes: false # reordering may break existing code
    ConstructorInitializerIndentWidth: 8
    ContinuationIndentWidth: 8
    ...
    # newline here

To format one file, run: ``clang-format -i -style=file mycode.cc`` and it will automatically find and use the format style file above.

See the `clang-format configuration documentation <http://clang.llvm.org/docs/ClangFormatStyleOptions.html>`_ for the meaning of these options.

Integration with :ref:`SublimeText <sublime-cpp>` , :ref:`Emacs <clang_format_emacs_integration>` and :ref:`Vim <clang_format_vim_integration>` is also available.
