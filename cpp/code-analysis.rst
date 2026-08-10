###########################
Static Analysis of C++ code
###########################

`CodeChecker <https://codechecker.readthedocs.io>`_,
`clang static analyzer <https://clang-analyzer.llvm.org>`_  and
`clang-tidy <https://clang.llvm.org/extra/clang-tidy>`_ can be
used to detect potential C++ problems enforce C++ coding standards.

==============================
Install tools from conda-forge
==============================

``CodeChecker`` depends on ``clang-tools`` and the clang compiler for static analysis.
To install the compilers and tools into an LSST Science Pipelines conda stack for Linux x86_64

.. code-block:: bash

   mamba install -c conda-forge clang clangxx clang-tools

To install ``CodeChecker``

.. code-block:: bash

   mamba install -c CodeChecker

================================
Running ``clang-tidy`` on builds
================================

``CodeChecker`` intercepts calls to the compiler executables, builds a compilation database and runs
analyses on the source code. 
To run ``CodeChecker`` in an lsstsw build environment

.. code-block:: bash

   C=gcc CXX=g++ CC_BIN=CodeChecker CodeChecker check -j4 --build "rebuild lsst_distrib" --analyzers clang-tidy -o results

``--analyzers clang-tidy`` limits the analysis to ``clang-tidy`` checks and disables ``clang static analysis``, which
is very CPU intensive.

The build command can be replaced as needed. For example, to run on ``scons`` builds

.. code-block:: bash

   C=gcc CXX=g++ CC_BIN=CodeChecker CodeChecker check -j4 --build "scons -j4 --analyzers clang-tidy" -o results

The standard output format of ``CodeChecker`` is ``plist``.
To produce a html report of the analysis results

.. code-block:: bash

   CodeChecker parse --trim-path-prefix $(pwd) -e html results -o results/html

Adding ``--trim-path-prefix`` avoids absolute references in the html output.
The result can be browsed with

.. code-block:: bash

   firefox html/index.html
