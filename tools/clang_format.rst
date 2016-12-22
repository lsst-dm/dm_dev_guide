.. _using_clang_format:

#######################################
Using clang-format for LSST Development
#######################################

The easiest way to comply with the :ref:`LSST code layout rules <style-guide-cpp-6-1>` is to use `clang-format <http://clang.llvm.org/docs/ClangFormat.html>`_.

You can install this tool through the Ubuntu package manager:

.. code-block:: bash

    sudo apt-get install clang-format

or through `Homebrew <http://brew.sh>`_ (on macOS):

.. code-block:: bash

    brew install clang-format

For more platforms see `here <http://releases.llvm.org/download.html>`_.

Place the following configuration file, named ``.clang-format``, in your top-level source directory:

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

Then run it with: ``clang-format -i -style=file mycode.cc``.

See the `clang-format configuration documentation <http://clang.llvm.org/docs/ClangFormatStyleOptions.html>`_ for the meaning of these options.

Integration with :ref:`Emacs <clang_format_emacs_integration>` and :ref:`Vim <clang_format_vim_integration>` is also available.

