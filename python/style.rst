#####################
DM Python Style Guide
#####################

This is the version 6.0 of the DM Python Coding Standard.
The :doc:`/coding/intro` provides the overarching Coding Standards policy applicable to all DM code.

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these standards, please file an :doc:`RFC </communications/rfc>`.

.. contents::
   :depth: 4

.. _style-guide-py-version:

0. Python Version
=================

.. _style-guide-py-version-py3:

All DM Python code MUST work with our standard environment
----------------------------------------------------------

All the Python code written by LSST Data Management must run under the version of Python provided in our :ref:`standard environment <platforms-environment>`.
Any feature available in that version of Python may be used.
There is no requirement to support Python 2 or earlier Python 3 versions.

.. _style-guide-py-pep8-baseline:

1. PEP 8 is the Baseline Coding Style
=====================================

Data Management's Python Coding Style is based on the `PEP 8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ with modifications specified in this document.

:pep:`8` is used throughout the Python community and should feel familiar to Python developers.
DM's deviations from :pep:`8` are primarily motivated by consistency with the :doc:`/cpp/style`.
Additional guidelines are included in this document to address specific requirements of the Data Management System.

.. _style-guide-py-ignored-errors:

Exceptions to PEP 8
-------------------

The following table summarizes all :pep:`8` guidelines that are **not followed** by the DM Python Style Guide.
These exceptions are organized by error codes that may be ignored by the flake8_ linter (see :ref:`style-guide-py-flake8`).

E133
   Closing bracket is missing indentation.
   This `pycodestyle error`_ (via flake8_) is not part of :pep:`8`.

E226
   Missing whitespace around arithmetic operator.
   See :ref:`style-guide-py-operator-whitespace`.

E228
   Missing whitespace around bitwise or shift operator.
   See :ref:`style-guide-py-operator-whitespace`.

Maximum line length
   See :ref:`style-guide-py-line-length`.

The style checker in ``pycodestyle`` also provides warnings that can be used to request a specific style that is ambiguous in :pep:`8`.
These codes should be ignored to choose the LSST preferred style:

W503
   Line break before binary operator.
   Disabling this enables W504 that checks that line breaks occur before binary operators.
   See :ref:`style-guide-py-binary-operator-line-break`.

Additionally, packages listed in :ref:`style-guide-py-sci-pi-naming` should disable the following rules:

N802
   Function name should be lowercase.
   See :ref:`style-guide-py-sci-pi-naming`.

N803
   Argument name should be lowercase.
   See :ref:`style-guide-py-sci-pi-naming`.

N806
   Variable in function should be lowercase.
   See :ref:`style-guide-py-sci-pi-naming`.

N812
   Lowercase imported as non lowercase.
   See :ref:`style-guide-py-sci-pi-naming`.

N813
   Camelcase imported as lowercase.
   See :ref:`style-guide-py-sci-pi-naming`.

N815
   MixedCase variable in class scope.
   See :ref:`style-guide-py-sci-pi-naming`.

N816
   MixedCase variable in global scope.
   See :ref:`style-guide-py-sci-pi-naming`.

.. _pycodestyle error: http://pep8.readthedocs.io/en/latest/intro.html#error-codes

.. _style-guide-py-flake8:

Code MAY be validated with flake8
---------------------------------

The flake8_ tool may be used to validate Python source code against the portion of :pep:`8` adopted by Data Management.
Additionally, flake8_ statically checks Python for code errors.
The separate `pep8-naming`_ plugin validates names according to the DM Python Style Guide.

.. note::

   Flake8 validates code against PEP 8 specifications and also allows some configuration for line lengths and cases where PEP8 allows some ambiguity but where we require consistency.
   This style guide includes additional guidelines that *are not* automatically linted.

.. _flake8: https://flake8.readthedocs.io
.. _pep8-naming: http://pypi.python.org/pypi/pep8-naming

.. _style-guide-py-flake8-install:

Flake8 installation
^^^^^^^^^^^^^^^^^^^

Linters are installable with :command:`pip`:

.. code-block:: bash

   pip install flake8
   pip install pep8-naming

.. _style-guide-py-flake8-invoke:

Flake8 command line invocation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   flake8 --ignore=E133,E226,E228 --max-line-length=110 --max-doc-length=79 .

This command lints all Python files in the current directory.
Alternatively, individual files can be specified in place of ``.``.

The ignored error codes are :ref:`explained above <style-guide-py-ignored-errors>`.
N802, N803, N806, N812, N813, N815, and N816 can be added to this list for some packages.

.. _style-guide-py-flake8-config:

Flake8 configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`flake8` can be invoked without arguments when a configuration file is present.
This configuration, included in a :file:`setup.cfg` file at the root of code repositories, is consistent with the style guide:

.. code-block:: ini

   [flake8]
   max-line-length = 110
   max-doc-length = 79
   ignore = E133, E226, E228, N802, N803, N806, N812, N813, N815, N816, W503
   exclude =
     bin,
     doc,
     **/*/__init__.py,
     **/*/version.py,
     tests/.tests

The ``exclude`` field lists paths that are not usefully linted by :command:`flake8` in DM Stack repositories.
Auto-generated Python should not be linted (including :file:`bin/` for Stack packages with :file:`bin.src/` directories).
We also discourage linting :file:`__init__.py` modules due to the abundance of :pep:`8` exceptions typically involved.

.. _style-guide-py-noqa:

Lines that intentionally deviate from DM's PEP 8 MUST include a ``noqa`` comment
--------------------------------------------------------------------------------

Lines of code may intentionally deviate from our application of PEP 8 because of limitations in flake8_.
In such cases, authors must append a ``# noqa`` comment to the line that includes the specific error code being ignored.
`See the flake8 documentation for details <https://flake8.readthedocs.io/en/latest/user/ignoring-errors.html#in-line-ignoring-errors>`__ .
This prevents the line from triggering false flake8_ warnings to other developers, while also linting unexpected errors.

For example, to import a module without using it (to build a namespace, as in a :file:`__init__.py`):

.. code-block:: py

   from .module import AClass  # noqa: F401

.. seealso::

   - `flake8 error codes <https://flake8.readthedocs.io/en/latest/user/error-codes.html>`_
   - `pycodestyle error codes <https://pycodestyle.readthedocs.io/en/latest/intro.html#error-codes>`_
   - `pep8-naming error codes <https://github.com/PyCQA/pep8-naming#plugin-for-flake8>`_

.. _style-guide-py-black:

Black MAY be used to fix PEP 8 compliance
-----------------------------------------

Many :pep:`8` issues in existing code can be fixed with :ref:`black<formatting-python-code>`.
If ``black`` is used for a repository the codebase should continue to use it to ensure consistency.

.. note::

   When using ``black`` there is no control over the whitespace around operators.
   The benefits of consistency from using ``black`` outweigh the reasons for using a :ref:`bespoke rule <style-guide-py-operator-whitespace>` and therefore the :ref:`PEP-8 exceptions noted elsewhere <style-guide-py-ignored-errors>` (E133, E226, and E228) can be removed.

.. _style-guide-py-autopep8:

autopep8 MAY be used to fix PEP 8 compliance
--------------------------------------------

Many :pep:`8` issues in existing code can be fixed with `autopep8`_ version 1.2 or newer:

.. code-block:: bash

   autopep8 . --in-place --recursive \
       --ignore E133,E226,E228,N802,N803,N806,W503 --max-line-length 110

The ``.`` specifies the current directory.
Together with ``--recursive``, the full tree of Python files will be processed by :command:`autopep8`.
Alternatively, a single file can be specified in place of ``.``.

:command:`autopep8`\ ʼs changes must always be validated before committing.

Style changes must be encapsulated in a distinct commit (see :ref:`git-commit-organization-logical-units`).

.. note::

   :command:`autopep8` only fixes PEP 8 issues and does not address other guidelines listed here.

.. _autopep8: https://pypi.python.org/pypi/autopep8

.. _style-guide-py-layout:

2. Layout
=========

.. seealso::

   :doc:`numpydoc` provides guidelines for the :ref:`layout of docstrings <py-docstring-basics>`.

.. _style-guide-license:

Each Python file MUST contain the standard license preamble
-----------------------------------------------------------

A copyright and license block using `the standard text <https://github.com/lsst/templates/tree/main/file_templates/stack_license_preamble_py>`_ MUST be included at the top of each file.
This can be written as a Python comment.

.. remote-code-block:: https://raw.githubusercontent.com/lsst/templates/main/file_templates/stack_license_preamble_py/template.py.jinja
   :language: jinja

Replace ``{{ cookiecutter.package_name }}`` with the package's name.

.. _style-guide-py-line-length:

Line Length MUST be less than or equal to 110 columns
-----------------------------------------------------

Limit all lines to a maximum of 110 characters.
This conforms to the :doc:`/cpp/style` (see :ref:`4-6 <style-guide-cpp-4-6>`).

This differs from the `PEP 8 recommendation of 79 characters <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_.

Note that indentation spaces are counted in this line length.
This allows editors to be set with fixed line limits.
If you find that indentation spaces are consuming a significant fraction of your code line, consider refactoring the code.

.. _style-guide-py-docstring-line-length:

Docstring and comment line length MUST be less than or equal to 79 columns
--------------------------------------------------------------------------

Limit all docstring and comment lines to a maximum of 79 characters.

This differs from the `PEP 8 recommendation of 72 characters <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_ and the `numpydoc recommendation of 75 characters <https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_ but maintains readability and compatibility with default terminal widths while providing the maximum space.

As for code lines, indentation spaces are counted in this line length to allow editors to be set with fixed line limits.

.. _style-guide-py-implied-continuation:

Python's implied continuation inside parens, brackets and braces SHOULD be used for wrapped lines
-------------------------------------------------------------------------------------------------

The preferred way of wrapping long lines is by using Python's implied line continuation inside parentheses, brackets and braces.

If necessary, you can add an extra pair of parentheses around an expression, but sometimes using a backslash looks better.
In this example, continuation is naturally implied within the ``__init__`` method argument lists, while both ``\`` and parentheses-based continuations are used in the ``if`` statements.

.. code-block:: py

   class Rectangle(Blob):
       """Documentation for Rectangle.
       """
       def __init__(self, width, height,
                    color='black', emphasis=None, highlight=0):

           # Discouraged: continuation with '\'
           if width == 0 and height == 0 \
                  and color == 'red' and emphasis == 'strong' \
                  or highlight > 100:
               raise ValueError("sorry, you lose")

           # Preferred: continuation with parentheses
           if width == 0 and height == 0 and (color == 'red'
                                              or emphasis is None):
               raise ValueError("I don't think so")

           Blob.__init__(self, width, height,
                         color, emphasis, highlight)

Be aware that the continued line must be distinguished from the following lines through indentation.
For example, this will generate an E129 error:

.. code-block:: py

   if (width == 0
       and height == 0):
       pass

Instead, the continued line should be indented:

.. code-block:: py

   if (width == 0
           and height == 0):
       pass

.. _style-guide-py-cpp-consistency:

Consistency with the DM C++ Coding Guide namespaces SHOULD be followed
----------------------------------------------------------------------

Consistency with the LSST C++ Coding Standards namespaces exists.

**Good:**

- ``from lsst.foo.bar import myFunction`` is analogous to ``using lsst::foo::bar::myFunction``

- ``import lsst.foo.bar as fooBar`` is analogous to ``namespace fooBar = lsst::foo::bar``

**Disallowed** in both Coding Standards (except in :file:`__init__.py` library initialization contexts):

- ``from lsst.foo.bar import *`` is analogous to ``using namespace lsst::foo::bar``

.. _style-guide-py-whitespace:

3. Whitespace
=============

Follow the `PEP 8 whitespace style guidelines <https://www.python.org/dev/peps/pep-0008/#whitespace-in-expressions-and-statements>`_, with the following adjustments.

.. _style-guide-py-minimal-parens:

The minimum number of parentheses needed for correctness and readability SHOULD be used
---------------------------------------------------------------------------------------

Yes:

.. code-block:: py

   a = b(self.config.nSigmaToGrow*sigma + 0.5)

Less readable:

.. code-block:: py

   a = b((self.config.nSigmaToGrow*sigma) + 0.5)

.. _style-guide-py-operator-whitespace:

Binary operators SHOULD be surrounded by a single space except for [``*``, ``/``, ``**``, ``//``, ``%``\ ]
----------------------------------------------------------------------------------------------------------

Always surround these binary operators with a single space on either side; this helps the user see where one token ends and another begins:

- assignment (``=``),
- augmented assignment (``+=``, ``-=``, etc.),
- comparisons (``==``, ``<``, ``>``, ``!=``, ``<>``, ``<=``, ``>=``, ``in``, ``not in``, ``is``, ``is not``),
- Booleans (``and``, ``or``, ``not``).

Use spaces around these arithmetic operators:

- addition (``+``),
- subtraction (``-``)

Never surround these binary arithmetic operators with whitespace:

- multiplication (``*``),
- division (``/``),
- exponentiation (``**``),
- floor division (``//``),
- modulus (``%``). Note that a single space **must always** surround ``%`` when used for string formatting.

For example:

.. code-block:: py

   i = i + 1
   submitted += 1
   x = x*2 - 1
   hypot2 = x*x + y*y
   c = (a + b)*(a - b)
   print('Hello %s' % 'world!')

This deviates from PEP 8, which `allows whitespace around these arithmetic operators if they appear alone <https://www.python.org/dev/peps/pep-0008/#other-recommendations>`__.
Error codes: E226 and E228.

.. _style-guide-py-binary-operator-line-break:

Wrap lines before binary operators
----------------------------------

`PEP 8 suggests <https://www.python.org/dev/peps/pep-0008/#should-a-line-break-before-or-after-a-binary-operator>`_ that lines should be broken before binary operators but allows after.
For consistency with modern Python conventions and tools such as `black`_, and languages such as SQL, we choose before.

.. _black: https://github.com/psf/black

This requires that W503 be disabled in pycodestyle.

.. _style-guide-py-comments:

4. Comments
===========

Source code comments should follow `PEP 8's recommendations <https://www.python.org/dev/peps/pep-0008/#comments>`__ with the following additional requirements.

.. _style-guide-py-comment-consistency:

Comments MUST always remain up-to-date with code changes
--------------------------------------------------------

Comments that contradict the code are worse than no comments.
Always make a priority of keeping the comments up-to-date when the code changes!

.. _style-guide-py-comment-sentence-spaces:

Sentences in comments SHOULD NOT be separated by double spaces
--------------------------------------------------------------

Following :pep:`8`, comments should be complete sentences.

However, sentences **should not** be separated by two spaces; a single space is sufficient.

`This differs from PEP 8 <https://www.python.org/dev/peps/pep-0008/#comments>`__.

.. _style-guide-py-block-comment-indentation:

Block comments SHOULD reference the code following them and SHOULD be indented to the same level
------------------------------------------------------------------------------------------------

Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code.
Each line of a block comment starts with a ``#`` and a single space (unless it is indented text inside the comment).

Paragraphs inside a block comment are separated by a line containing a single ``#``.

To-do comments SHOULD include a Jira issue key
----------------------------------------------

If the commented code is a workaround for a known issue, this rule makes it easier to find and remove the workaround once the issue has been resolved.
If the commented code itself is the problem, this rule ensures the issue will be reported on Jira, making it more likely to be fixed in a timely manner.

.. code-block:: py

   # TODO: workaround for DM-6789

.. code-block:: py

   # TODO: DM-12345 is triggered by this line

.. _style-guide-py-docstrings:

5. Documentation Strings (docstrings)
=====================================

Use **Numpydoc** to format the content of all docstrings.
The page :doc:`numpydoc` authoritatively describes this format.
Its guidelines should be treated as an extension of this Python Style Guide.

.. seealso::

   The :doc:`/restructuredtext/style`---and the :ref:`rst-formatting-guidelines` section in particular---provide guidelines on reStructuredText in general.

.. _style-guide-py-docstring-public-api:

Docstrings SHOULD be written for all public modules, functions, classes, and methods
------------------------------------------------------------------------------------

Write docstrings for all public modules, functions, classes, and methods.
See :doc:`numpydoc`.

Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does.
This comment should appear after the ``def`` line.

.. _style-guide-py-naming:

6. Naming Conventions
=====================

We follow `PEP 8ʼs naming conventions <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_, with exceptions listed here.
C++ source code included within a Python package SHOULD follow the naming conventions of the Python package for APIs that are to be visible to Python users.

All LSST Python source code is consistent with :pep:`8` naming in the following ways:

- class names are ``CamelCase`` with leading uppercase,
- module variables used as module global constants are ``UPPERCASE_WITH_UNDERSCORES``,

Some packages, for historical reasons, do not fully adhere to :pep:`8`.
These packages, and the associated naming conventions, are described in :ref:`style-guide-py-sci-pi-naming`.
Naming style SHOULD be consistent within a top-level package built by Jenkins, or within a distinct service, and it is RECOMMENDED that :pep:`8` naming convention be adopted, whilst understanding that it may be difficult to modify existing packages.
Consistency within a package is mandatory.
Within these stated constraints new packages SHOULD use :pep:`8` naming conventions.

Names may be decorated with leading and/or trailing underscores.

.. _style-guide-py-sci-pi-naming:

Naming Conventions for Science Pipelines
----------------------------------------

For historical reasons, Science Pipelines code (nominally, all packages included in the ``lsst_apps`` metapackage, as well as ``meas_*``, ``pipe_*``, and ``obs_*`` and all dependencies), does not completely adhere to :pep:`8`-style.

:pep:`8` style is used in the following cases:

- class names are ``CamelCase`` with leading uppercase,
- module variables used as module global constants are ``UPPERCASE_WITH_UNDERSCORES``,

but all other names are traditionally ``camelCase`` with leading lowercase, and local (class, file, module) consistency in naming is important.
In particular:

.. _style-guide-py-naming-attributes:
.. _style-guide-py-naming-functions:

- Class Attribute Names MAY be camelCase with leading lowercase (Error code: N803).
- Module methods (free functions) MAY be camelCase with leading lowercase (Error code: N802)
- Compound variable names MAY be camelCase with leading lowercase (Error code: N806).

Recognizing that this style is becoming less common in Python at large, new Science Pipelines code MAY also be be written in full :pep:`8` style, according to the following guidelines:

- :pep:`8` style ("snake_case") public names are preferred in "primarily new" code, such as new modules and classes that do not primarily implement an existing camelCase interface.
  "snake_case" local variables names are similarly preferred in new functions, even functions with a camelCase public API.
  The strict definition of "primarily new code" is case by case and left to developer judgement.

- camelCase is still permitted in new code, and is preferred when adding public methods, arguments, and attributes to existing classes with an established camelCase API, or making modifications to existing functions with camelCase local variables.

- Under no circumstances should the Python side of a pybind11-wrapped C++ function use a different naming convention than the C++ function.  C++ naming conventions and the guidelines for applying them in new/old code are no different from those of Python, but it is never permitted to just change things at the pybind11 level; either both C++ and Python or neither should be changed.

Changing existing names from camelCase to snake_case is generally discouraged as unnecessary churn, and should only be done in highly localized code (e.g. individual function bodies) that already being extensively modified.
Name changes to public interfaces are of course API changes, and must go through the usual RFC and deprecation procedure.

.. _style-guide-py-naming-class-modules:

Modules which contain class definitions SHOULD be named after the class name
----------------------------------------------------------------------------

Modules which contain class definitions should be named after the class name (one module per class).

.. _style-guide-py-2-2:

User defined names SHOULD NOT shadow python built-in functions
--------------------------------------------------------------

Names which shadow a python built-in function may cause confusion for readers of the code.
Creating a more specific identifier is suggested to avoid collisions.
For example, in the case of *filter*, ``filter_name`` may be appropriate; for *filter objects*, something like ``filter_obj`` might be appropriate.

.. _style-guide-py-naming-ambiguous:

Names l (lowercase: el), O (uppercase: oh), I (uppercase: eye) MUST be avoided
------------------------------------------------------------------------------

Never use these characters as single character variable names:

- ``l`` (lowercase letter el),
- ``O`` (uppercase letter oh), or
- ``I`` (uppercase letter eye).

In some fonts, these characters are indistinguishable from the numerals one and zero.
When tempted to use ``l``, use ``L`` instead.

.. note::

  This matches the `PEP 8 standard <https://www.python.org/dev/peps/pep-0008/#names-to-avoid>`_ but is repeated here for emphasis.

.. _style-guide-py-naming-metaclasses:

Always use ``cls`` for the first argument to metaclass instance methods
-----------------------------------------------------------------------

For regular classes ``self`` is used, but for class methods and hence also for metaclass instance
methods, ``cls`` should be used instead.

.. note::

    This is consistent with the naming conventions in PEP 8 as indicated explicitly
    by `upstream <https://mail.python.org/pipermail/python-dev/2018-January/151986.html>`_.

.. _style-guide-py-naming-import:

Import statements SHOULD follow a standard pattern
--------------------------------------------------

You may choose either to write module import statements so that they import the fully-qualified module name:

.. code-block:: py

   import lsst.foo.bar

or you may use ``as`` to assign a short name to the module:

.. code-block:: py

   import lsst.foo.bar as fooBar

Short names are typically formed by dropping ``lsst.`` and combining the rest of the name using camel-case.
They should be consistent between Python and C++ (see :ref:`C++ Style Guide rule 5-42 <style-guide-cpp-5-42>`).

When working with an established part of the codebase — editing an existing file, or working within an existing package — the import style should be consistent with the existing code.

.. _style-guide-py-files:

7. Source Files & Modules
=========================

.. _style-guide-py-file-name:

A Python source file name SHOULD be camelCase-with-leading-lowercase or snake_case, and end in '.py'
----------------------------------------------------------------------------------------------------

A module containing a single class should be a ``camelCase``-with-leading-lowercase transliteration of the class's name (if the code within primarily adheres to the older, camelCase version of :ref:`Science Pipelines naming conventions <style-guide-py-sci-pi-naming>`) or a snake_case version of the class's name (if the code within primarily adheres to the full :pep:`8` naming conventions).

Test files must have the form ``test_{description}.py`` for compatibility with Pytest.
The name of a test case should be descriptive without the need for a trailing numeral to distinguish one test case from another.

This rule does not apply to executable script files, for which both no extension and a '.py' extension are acceptable.
Script files should always be minimal (ideally a single non-import statement), and delegate any actual logic to importable code.
This maximizes usability from other Python code (including test code) and makes it much easier to include script interfaces in documentation.
It also means the impact of having no extension on tools that rely on the file extension should be negligible.
Legacy scripts that do contain signficant logic should have a '.py' script to support this tooling.

.. TODO consider refactoring tests into their own section

.. _style-guide-py-file-encoding:

ASCII Encoding MUST be used for new code
----------------------------------------

Always use ASCII for new Python code.

- **Do not** include a coding comment (as described in  :pep:`263`) for ASCII files.

- Existing code using Latin-1 encoding (a.k.a. ISO-8859-1) is acceptable so long as it has a proper coding comment. All other code must be converted to ASCII or Latin-1 except for 3rd party packages used "as is."

.. _style-guide-py-file-order:

Standard code order SHOULD be followed
--------------------------------------

Within a module, follow the order:

#. Shebang line, ``#! /usr/bin/env python`` (only for executable scripts)
#. Module-level comments (such as the `license statement <https://github.com/lsst/templates/tree/main/file_templates/stack_license_py>`__)
#. Module-level docstring
#. ``__all__ = [...]`` statement, if present
#. Imports
#. Private module variables (names start with underscore)
#. Private module functions and classes (names start with underscore)
#. Public module variables
#. Public functions and classes

.. _style-guide-py-classes:

8. Classes
==========

.. seealso:: `Designing for Inheritance <https://www.python.org/dev/peps/pep-0008/#designing-for-inheritance>`__ in :pep:`8` describes naming conventions related to public and private class APIs.

.. _style-guide-py-super:

``super`` MAY be used to call parent class methods
--------------------------------------------------

If you are overriding a method from a parent class, use `super` to call the parent class's method.
For example:

.. code-block:: py

    class B(object):
        def method(self, arg):
            self.foo = arg

    class C(B):
        def method(self, arg):
            super().method(arg)
            do_something()

    C().method(arg)

Using `super` ensures a consistent Method Resolution Order, and prevents inherited methods from being called multiple times.
In Python 3, `super` does not require naming the class that it is part of, making its use simpler and removing a maintenance issue.

super() and Multiple Inheritance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the presence of multiple inheritance (two or more parents, e.g. ``class C(A, B)``), the trickiest issue with the use of `super` is that the class author generally doesn't know a priori which overridden method will be called in what order.
In particular, this means that the calling signature (arguments) for all versions of a method must be compatible.
As a result, there are a few argument-related caveats about the use of `super` in multiple inheritance hierarchies:

* Only pass `super` the exact arguments you received.
* When you use it on methods whose acceptable arguments can be altered on a subclass via addition of more optional arguments, always accept ``*args``, ``**kwargs``, and call `super` like ``super().currentmethod(arg1, arg2, ..., *args, **kwargs)``. If you don’t do this, document that addition of optional arguments in subclasses is forbidden.
* Do not use positional arguments in ``__init__`` or ``__new__``.  Instead, use keyword args in the declarations, always call them using keywords, and always pass all keywords on, e.g. ``super().__init__(**kwargs)``.

To use `super` with multiple inheritance, all base classes in Python's Method Resolution Order need to use `super`; otherwise the calling chain gets interrupted.
If your class may be used in multiple inheritance, ensure that all relevant classes use `super` including documenting requirements for subclasses.

For more details, see the `super documentation <super>`, the `astropy coding guide <http://docs.astropy.org/en/stable/development/codeguide.html#super-vs-direct-calling>`__, and `this article from Raymond Hettinger <https://rhettinger.wordpress.com/2011/05/26/super-considered-super/>`__.

.. _style-guide-py-comparisons:

9. Comparisons
==============

.. _style-guide-py-comp-is:

``is`` and ``is not`` SHOULD only be used for determining if two variables point to same object
-----------------------------------------------------------------------------------------------

Use ``is`` or ``is not`` only for the case that you need to know that two variables point to the exact same object.

To test for equality in *value*, use ``==`` or ``!=`` instead.

.. _style-guide-py-comp-none:

``is`` and ``is not`` SHOULD be used when comparing to ``None``
---------------------------------------------------------------

There are two reasons:

1. ``is None`` works with NumPy arrays, whereas ``== None`` does not;
2. ``is None`` is idiomatic.

This is also consistent with :pep:`8`, which `states <https://www.python.org/dev/peps/pep-0008/#programming-recommendations>`__:

   Comparisons to singletons like ``None`` should always be done with ``is`` or ``is not``, never the equality operators.

For sequences, (``str``, ``list``, ``tuple``), use the fact that empty sequences are ``False``.

Yes:

.. code-block:: py

   if not seq:
       pass

   if seq:
       pass

No:

.. code-block:: py

   if len(seq):
       pass

   if not len(seq):
       pass

.. _style-guide-py-idioms:

10. Idiomatic Python
====================

Strive to write idiomatic Python.
Writing Python with accepted patterns makes your code easier for others to understand and often prevents bugs.

`Fluent Python <http://shop.oreilly.com/product/0636920032519.do>`_ by Luciano Ramalho is an excellent guide to writing idiomatic Python.

Idiomatic Python also reduces technical debt.
For more information see the online book `Supporting Python 3 <http://python3porting.com/toc.html>`_ by Lennart Regebro.

.. _style-guide-py-pitfalls-mutables:

A mutable object MUST NOT be used as a keyword argument default
---------------------------------------------------------------

Never use a mutable object as default value for a keyword argument in a function or method.

When used a mutable is used as a default keyword argument, the default *can* change from one call to another leading to unexpected behavior.
This issue can be avoided by only using immutable types as defaults.

For example, rather than provide an empty list as a default:

.. code-block:: py

   def proclist(alist=[]):
       pass

this function should create a new list in its internal scope:

.. code-block:: py

   def proclist(alist=None):
       if alist is None:
           alist = []

.. _style-guide-py-context-managers:

Context managers (``with``) SHOULD be used for resource allocation
------------------------------------------------------------------

Use the ``with`` statement to simplify resource allocation.

For example to be sure a file will be closed when you are done with it:

.. code-block:: py

   with open('/etc/passwd', 'r') as f:
       for line in f:
           pass

.. _style-guide-py-dict-keys:

Avoid ``dict.keys()`` when iterating over keys or checking membership
---------------------------------------------------------------------

For iterating over keys, iterate over the dictionary itself, e.g.:

.. code-block:: py

   for x in mydict:
       pass

To test for inclusion use ``in``:

.. code-block:: py

    if key in myDict:
        pass

This is preferred over `~dict.keys`. Use `~dict.keys` when storing the keys for later access:

.. code-block:: py

    k = list(mydict.keys())

where ``list`` ensures that a view or iterator is not being retained.

.. _style-guide-py-subprocess:

The ``subprocess`` module SHOULD be used to spawn processes
-----------------------------------------------------------

Use the `subprocess` module to spawn processes.

.. _style-guide-py-lambda:

``lambda`` SHOULD NOT be used
-----------------------------

Avoid the use of `lambda <https://docs.python.org/3/reference/expressions.html#lambda>`__.
You can almost always write clearer code by using a named function or using the `functools` module to wrap a function.

.. _style-guide-py-set:

The ``set`` type SHOULD be used for unordered collections
---------------------------------------------------------

Use the `set` type for unordered collections of objects.

.. _style-guide-py-argparse:

The ``argparse`` module SHOULD be used for command-line scripts
---------------------------------------------------------------

Use the `argparse` module for command-line scripts.

Command line tasks for pipelines should use :lclass:`lsst.pipe.base.ArgumentParser` instead.

.. _style-guide-py-generators:

Iterators and generators SHOULD be used to iterate over large data sets efficiently
-----------------------------------------------------------------------------------

Use iterators, generators (classes that act like iterators) and generator expressions (expressions that act like iterators) to iterate over large data sets efficiently.

.. _style-guide-py-disabled-code:

``if False:`` and ``if True:`` SHOULD NOT be used
-------------------------------------------------

Code must not be placed inside ``if False:`` or ``if True:`` blocks, nor left commented out.
Instead, debugging code and alternative implementations must be placed inside a "named" ``if`` statement.
Such blocks should have a comment describing why they are disabled.
They may have a comment describing the conditions under which said code can be removed (like the completion of a ticket or a particular date).
For example, for code that will likely be removed in the future, once testing is completed:

.. code-block:: py

    # Delete old_thing() and the below "if" statement once all unittests are finished (DM-123456).
    use_old_method = False
    if use_old_method:
        old_thing()
    else:
        new_thing()

It is often beneficial to lift such debugging flags into the method's keyword arguments to allow users to decide which branch to run. For example:

.. code-block:: py

    def foo(x, debug_plots=False):
        do_thing()
        if debug_plots:
            plot_thing()

or, using ``lsstDebug``, which can be controlled as part of a command line task:

.. code-block:: py

    import lsstDebug
    def foo(x):
        do_thing()
        if lsstDebug.Info(__name__).debug_plots:
            plot_thing()

.. _style-guide-py-deprecation:

The ``deprecated`` decorator SHOULD be used to deprecate code
-------------------------------------------------------------

For more on deprecating code, see :doc:`/stack/deprecating-interfaces`.

.. _style-guide-py-properties:

Properties SHOULD be used when they behave like regular instance attributes
---------------------------------------------------------------------------

Properties SHOULD be added to Python objects to provide syntactic sugar for a getter (and possibly setter) when all of the following conditions are true:

 - The getter method must return the same type the setter method accepts, or the types must have very similar interfaces (e.g. because they are part of the same class hierarchy, or they share an important common interface, such as a Python Sequence).

 - Either the returned object must be immutable or modifying it must modify the object on which the property is defined in the expected way. Note that it may be useful to have a getter return an immutable object (e.g. ``tuple`` instead of ``list``) to meet this criterion. This prevents confusing behavior in which ``a.b.c = v`` could be a silent no-op.

 - The getter (and setter, if it exists) must be computationally trivial; either the direct return of an internal object or an extremely simple calculation (e.g. the width of a bounding box from its starting and ending x coordinates). In general, getter methods that begin with something other than "get" should not have associated properties.

Some examples:

 - ``Image.getBBox()`` SHOULD NOT have an associated property, because the returned object (``Box2I``) is mutable, but modifying it does not modify the bounding box of the ``Image``.

 - ``Psf.computeShape()`` SHOULD NOT have an associated property, because the getter is not computationally trivial - as suggested by the method name.

 - ``Image.getArray()`` SHOULD have an associated property, because the returned object is a view that can be modified to modify the original image.

 - ``Exposure.getWcs()`` SHOULD have an associated property, because the returned object is a data member of the ``Exposure`` that is returned via ``shared_ptr`` in C++, which allows modifications to the ``Wcs`` to automatically affect the ``Exposure``.

Note that C++ getters that return STL container types cannot have properties in Python unless the usual pybind11 conversion (which typically yields ``list``, ``dict``, or ``set`` objects) is augmented with a conversion to an immutable type (such as ``tuple`` or ``frozenset``), because these conversions otherwise always yield mutable objects that do not modify the parent.

The existing getters and setters MUST NOT be removed when defining a property.

.. _style-guide-py-exceptions:

Python exceptions SHOULD be raised and checked in Python code
-------------------------------------------------------------

When raising an exception in Python code, consideration should be given to `defining a module-specific exception`_ for increased precision.
Such an exception SHOULD inherit from an appropriate standard Python exception, unless it also needs to be thrown from C++ code, in which case it MUST be defined using the LSST-specific ``pex_exceptions`` library.
If a module-specific exception is not used, then the appropriate standard Python exception SHOULD be raised.

.. _defining a module-specific exception: https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

When writing an ``except`` clause, the exception type caught SHOULD be, in order of preference, a module-specific exception (either Python or C++), a standard Python exception, or a generic ``pex_exceptions`` exception for which there is no corresponding Python exception.
In particular, most generic ``pex_exceptions`` exceptions should be caught as their standard Python counterparts.
For example, catch ``lsst.pex.exceptions.OverflowError`` as the Python ``OverflowError``, but catch ``lsst.pex.exceptions.LengthError`` as such.
