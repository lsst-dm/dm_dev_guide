################################################
Managing license and copyright in Stack packages
################################################

All packages in the LSST Stack (EUPS-distributed packages installed with ``lsst_distrib`` and ``qserv_distrib``, for example) are licensed under `GPL-3.0`_ terms.
This page describes the three aspects developers need to know to properly implement the `GPL-3.0`_ license in Stack packages:

1. :ref:`The LICENSE file <stack-package-license>`
2. :ref:`The COPYRIGHT file <stack-package-copyright>`
3. :ref:`License preambles in source files <stack-package-preambles>`

For additional background information on licenses and copyright for LSST DM work, see the pages :doc:`/legal/licensing-overview` and :doc:`/legal/copyright-overview`.

.. _stack-package-license:

The LICENSE file
================

Each Stack package must have a file called :file:`LICENSE` at its root.
You can find the LICENSE file in the `stack_package template <https://github.com/lsst/templates/blob/master/project_templates/stack_package/%7B%7Bcookiecutter.package_name%7D%7D/LICENSE>`__.

Be careful not to modify the LICENSE file.

.. _stack-package-copyright:

The COPYRIGHT file
==================

Each Stack package must have a file called :file:`COPYRIGHT` at its root where we record copyright assignments.
See :ref:`copyright-file` for information on how to format the :file:`COPYRIGHT` file.

All DM developers are expected to participate in maintaining the :file:`COPYRIGHT` file on behalf of your institution.
Include additions to :file:`COPYRIGHT` files as part of your regular pull requests.

.. _stack-package-preambles:

License preambles in source files
=================================

The `GPL-3.0`_ license requires each source file to have a preamble comment containing a license statement.
This is the generic license preamble:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/master/file_templates/stack_license_preamble_txt/template.txt.jinja
   :language: jinja

Replace ``{{ cookiecutter.package_name }}`` with the repository's name (``afw``, for example).

This preamble is available as `a template <https://github.com/lsst/templates/tree/master/file_templates/stack_license_preamble_txt>`__.

Python preamble
---------------

The license preamble specifically for use in Python files is:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/master/file_templates/stack_license_preamble_py/template.py.jinja
   :language: jinja

Replace ``{{ cookiecutter.package_name }}`` with the repository's name (``afw``, for example).

See also: :ref:`style-guide-license` in the LSST DM Python Style Guide.

This preamble is available as `a template <https://github.com/lsst/templates/tree/master/file_templates/stack_license_preamble_py>`__.

C++ preamble
------------

The license preamble specifically for use in C++ source and header files is:

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/master/file_templates/stack_license_preamble_cpp/template.cc.jinja
   :language: jinja

Replace ``{{ cookiecutter.package_name }}`` with the repository's name (``afw``, for example).

This preamble is available as `a template <https://github.com/lsst/templates/tree/master/file_templates/stack_license_preamble_cpp>`__.

.. _`GPL-3.0`: https://choosealicense.com/licenses/gpl-3.0/
