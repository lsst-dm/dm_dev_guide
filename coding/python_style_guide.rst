#####################
DM Python Style Guide
#####################

This is the version 6.0 of the DM Python Coding Standard.
The :doc:`intro` provides the overarching Coding Standards policy applicable to all DM code.

Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
To request changes to these standards, please file an :ref:`RFC <decision-making-rfc>`.

.. contents::
   :depth: 4

.. _style-guide-py-intro:

1. PEP 8 is the Baseline Coding Style
=====================================

Data Management's Python coding style is based the `PEP 8 Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ with modifications specified in this document.

`PEP 8`_ is used throughout the Python community, and should feel familiar to Python developers.
DM's deviations to `PEP 8`_ are motivated by consistency with the :doc:`cpp_style_guide`.
Additional guidelines are included in this document to address specific requirements of the Data Management System.

.. _PEP 8: http://www.python.org/dev/peps/pep-0008/

.. _style-guide-py-flake8:

Code MAY be validated with flake8
---------------------------------

The flake8_ tool may be used to validate Python source code against the portion of PEP 8 adopted by Data Management.
In addition, flake8_ statically checks Python for code errors.
The separate `pep8-naming`_ plugin validates names according to the DM Python coding style.

.. note::
   
   Flake8 only validates code against PEP 8 specifications, but does not check the full coding standard listed here.

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

   flake8 --ignore=E133,E226,E228,N802,N803 --max-line-length=110 .

This command lints all Python files in the current directory.
Alternatively, individual files can be specified in place of ``.``.

The ignored error codes are :ref:`explained below <style-guide-py-ignored-errors>`.

.. _style-guide-py-flake8-config:

Flake8 configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^

LSST DM Packages may also include a :file:`setup.cfg` file with :pep:`8` exceptions:

.. code-block:: ini

	[flake8]
	max-line-length = 110
	ignore = E133, E226, E228, N802, N803

:command:`flake8` can be invoked without arguments when this configuration is present.

.. _style-guide-py-ignored-errors:

Summary of PEP 8 exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

These error codes can be **ignored** by flake8_ when checking DM code against :pep:`8` specifications:

E133
   Closing bracket is missing indentation.
   This `pycodestyle error`_ (via flake8_) is not part of :pep:`8`.

E226
   Missing whitespace around arithmetic operator.
   See :ref:`style-guide-py-operator-whitespace`.

E228
   Missing whitespace around bitwise or shift operator.
   See :ref:`style-guide-py-operator-whitespace`.

E251
   Unexpected spaces around keyword / parameter equals.
   See :ref:`style-guide-py-multiline-assignment-whitespace`.

N802
   Function name should be lowercase.
   See :ref:`style-guide-py-naming`.

N803
   Argument name should be lowercase.
   See :ref:`style-guide-py-naming`.

.. _pycodestyle error: http://pep8.readthedocs.io/en/latest/intro.html#error-codes

.. _style-guide-py-noqa:

Lines that intentionally deviate from DM's PEP 8 MUST include a ``noqa`` comment
--------------------------------------------------------------------------------

Lines of code may intentionally deviate from our application of PEP 8 (see above) because of limitations in flake8_.
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

.. _style-guide-py-autopep8:

autopep8 MAY be used to fix PEP 8 compliance
--------------------------------------------

Many PEP 8 issues in existing code can be fixed with `autopep8`_:

.. code-block:: bash

   autopep8 . --in-place --recursive \
       --ignore E133,E226,E228,N251,N802,N803 --max-line-length 110

The ``.`` specifies the current directory.
Together with ``--recursive``, the full tree of Python files will be processed by :command:`autopep8`.
Alternatively, a single file can be specified in place of ``.``.

:command:`autopep8` changes must always be validated before committing.

Style changes must be encapsulated in a distinct commit (see :ref:`git-commit-organization-logical-units` in :doc:`Workflow document <../processes/workflow>`).

.. note::

   :command:`autopep8` only fixes PEP 8 issues and does not address other guildelines listed here.

.. _autopep8: https://pypi.python.org/pypi/autopep8

.. _style-guide-py-layout:

2. Layout
=========

.. _style-guide-py-line-length:

Line Length MUST be less than or equal to 110 columns
-----------------------------------------------------

Limit all lines to a maximum of 110 characters.
This conforms to the :doc:`cpp_style_guide` (see :ref:`4-6 <style-guide-cpp-4-6>`).

This differs from the `PEP 8 recommendation of 79 characters <https://www.python.org/dev/peps/pep-0008/#id19>`_.

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
           if width == 0 and height == 0 and \
                  color == 'red' and emphasis == 'strong' or \
                  highlight > 100:
               raise ValueError("sorry, you lose")
   
           # Preferred: continuation with parentheses
           if width == 0 and height == 0 and (color == 'red' or
                                              emphasis is None):
               raise ValueError("I don't think so")
   
           Blob.__init__(self, width, height,
                         color, emphasis, highlight)

Be aware that the continued line must be distinguished from the following lines through indentation.
For example, this will generate an E129 error:

.. code-block:: py

   if (width == 0 and
       height == 0):
       pass

Instead, the continued line should be indented:

.. code-block:: py

   if (width == 0 and
           height == 0):
       pass

.. _style-guide-py-docstring-blank-lines:

Blank lines SHOULD NOT be added before or after a docstring
-----------------------------------------------------------

Do not use a blank line on either side of a docstring.

.. _style-guide-py-cpp-consistency:

Consistency with the DM C++ Coding Guide namespaces SHOULD be followed
----------------------------------------------------------------------

Consistency with the LSST C++ Coding Standards namespaces exists.

**Good:**

- ``from lsst.foo.bar import myFunction`` is analogous to ``using lsst::foo::bar::myFunction``

- ``import lsst.foo.bar as fooBar`` is analogous to ``namespace fooBar = lsst::foo::bar``

**Disallowed** in both Coding Standards (except in :file:`__init__.py` library initialization context):

- ``from lsst.foo.bar import *`` is analogous to ``using namespace lsst::foo::bar``

.. _style-guide-py-whitespace:

3. Whitespace
=============

Follow the `PEP 8 whitespace style guidelines <https://www.python.org/dev/peps/pep-0008/#id26>`_, with the following adjustments.

.. _style-guide-py-minimal-parens:

The minimum number of parenthesis needed for correctness and readability SHOULD be used
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

This deviates from PEP 8, which `allows whitespace around these arithmetic operators if they appear alone <https://www.python.org/dev/peps/pep-0008/#id28>`__.
Error codes: E226 and E228.

.. _style-guide-py-multiline-assignment-whitespace:

Keyword assignment operators SHOULD be surrounded by a space when statements appear on multiple lines
-----------------------------------------------------------------------------------------------------

However, if keyword assignments occur on a single line, where should be no additional spaces.

Thus this: 

.. code-block:: py

   # whitespace around multi-line assignment
   funcA(
       karg1 = value1,
       karg2 = value2,
       karg3 = value3,
   )

   # no whitespace around single-line assigment
   funcB(x, y, z, karg1=value1, karg2=value2, karg3=value3)

Not this: 

.. code-block:: py

   funcA(
       karg1=value1,
       karg2=value2,
       karg3=value3,
   )

   aFunction(x, y, z, karg1 = value1, karg2 = value2, karg3 = value3)

`Opposes PEP 8 <https://www.python.org/dev/peps/pep-0008/#id28>`__.
Error code: N251.

.. _style-guide-py-comments:

4. Comments
===========

Source code comments should follow `PEP 8's recommendations <https://www.python.org/dev/peps/pep-0008/#id29>`__ with the following additional requirements.

.. _style-guide-py-comment-consistency:

Comments MUST always remain up-to-date with code changes
--------------------------------------------------------

Comments that contradict the code are worse than no comments.
Always make a priority of keeping the comments up-to-date when the code changes!

.. _style-guide-py-comment-sentence-spaces:

Sentences in comments SHOULD NOT be separated by double spaces
--------------------------------------------------------------

Following PEP 8, comments should be complete sentences.

However, sentences **should not** be separated by two spaces; a single space is sufficient.

`This differs from PEP 8 <https://www.python.org/dev/peps/pep-0008/#id29>`__.

.. _style-guide-py-block-comment-indentation:

Block comments SHOULD reference the code following them and SHOULD be indented to the same level
------------------------------------------------------------------------------------------------

Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code.
Each line of a block comment starts with a ``#`` and a single space (unless it is indented text inside the comment).

Paragraphs inside a block comment are separated by a line containing a single ``#``.

.. _style-guide-py-docstrings:

5. Documentation Strings (docstrings)
=====================================

Use **Numpydoc** to format the content of all docstrings.
The page :doc:`../docs/py_docs` authoritatively describes this format.
Its guidelines should be treated as an extension of this Python style guide.

See also the :doc:`../docs/rst_styleguide` and the :ref:`rst-formatting-guidelines` section in particular for guidelines on reStructuredText in general.

.. _style-guide-py-docstring-public-api:

Docstrings SHOULD be written for all public modules, functions, classes, and methods
------------------------------------------------------------------------------------

Write docstrings for all public modules, functions, classes, and methods.
See :doc:`../docs/py_docs`.

Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does.
This comment should appear after the ``def`` line.

.. _style-guide-py-naming:

6. Naming Conventions
=====================

We follow `PEP 8ʼs naming conventions <https://www.python.org/dev/peps/pep-0008/#naming-conventions>`_, with exceptions listed here.
The naming conventions for LSST Python and C++ source have been defined to be as similar as the respective languages allow.

In general:

- class names are ``CamelCase`` with leading uppercase,
- module variables used as module global constants are ``UPPERCASE_WITH_UNDERSCORES``,
- all other names are ``camelCase`` with leading lowercase.

Names may be decorated with leading and/or trailing underscores.

.. _style-guide-py-2-2:

User defined names SHOULD NOT shadow python built-in functions
--------------------------------------------------------------

Names which shadow a python built-in function may cause confusion for readers of the code.
Creating a more specific identifier is suggested to avoid collisions.
In the case of *filter*, ``filterName`` may be appropriate; for *filter objects*, something like ``filterObj`` might be appropriate.

.. _style-guide-py-naming-attributes:

Class Attribute Names SHOULD be camelCase with leading lowercase
----------------------------------------------------------------

`Opposes PEP 8 <https://www.python.org/dev/peps/pep-0008/#id45>`__.
Error codes: N802 and N803.

.. _style-guide-py-naming-functions:

Module methods (free functions) SHOULD be camelCase with leading lowercase
--------------------------------------------------------------------------

`Opposes PEP 8 <https://www.python.org/dev/peps/pep-0008/#id45>`__.
Error code: N802.

.. _style-guide-py-naming-class-modules:

Modules which contain class definitions SHOULD be named after the class name
----------------------------------------------------------------------------

Modules which contain class definitions should be named after the class name (one module per class).

.. _style-guide-py-naming-ext-modules:

When a Python module wraps a C/C++ extension module, the C/C++ module SHOULD be named <module>Lib
-------------------------------------------------------------------------------------------------

When an extension module written in C or C++ has an accompanying Python module that provides a higher level (e.g. more object oriented) interface, the C/C++ module should append ``Lib`` to the module's name (e.g. ``socketLib``).

.. _style-guide-py-naming-ambiguous:

Names l (lowercase: el), O (uppercase: oh), I (uppercase: eye) MUST be avoided
------------------------------------------------------------------------------

Never use these characters as single character variable names:

- ``l`` (lowercase letter el),
- ``O`` (uppercase letter oh), or
- ``I`` (uppercase letter eye).

In some fonts, these characters are indistinguishable from the numerals one and zero.
When tempted to use ``l``, use ``L`` instead.

.. _style-guide-py-files:

7. Source Files & Modules
=========================

.. _style-guide-py-file-name:

A Python source file name SHOULD be camelCase-with-leading-lowercase and ending in '.py'
----------------------------------------------------------------------------------------

A module containing a single class should be a ``camelCase``-with-leading-lowercase transliteration of the class's name.

The name of a test case should be descriptive without the need for a trailing numeral to distinguish one test case from another. 

.. TODO consider refactoring tests into their own section

.. _style-guide-py-file-encoding:

ASCII Encoding MUST be used for new code
----------------------------------------

Always use ASCII for new python code.

- **Do not** include a coding comment (as described in  :pep:`263`) for ASCII files.

- Existing code using Latin-1 encoding (a.k.a. ISO-8859-1) is acceptable so long as it has a proper coding comment. All other code must be converted to ASCII or Latin-1 except for 3rd party packages used "as is."

.. _style-guide-py-file-order:

Standard code order SHOULD be followed
--------------------------------------

Within a module, follow the order: 

1. Shebang line, ``#! /usr/bin/env python`` (only for executable scripts)
2. Module-level comments (such as the `license statement <https://github.com/lsst/templates/blob/master/CopyrightHeader.py>`__)
3. Module-level docstring
4. Imports
5. ``__all__`` statement, if any
6. Private module variables (names start with underscore)
7. Private module functions and classes (names start with underscore)
8. Public module variables
9. Public functions and classes
10. Optional test suites

.. FIXME JSick: Delete mention of test suites?

.. _style-guide-py-classes:

8. Classes
==========

Always decide whether a class's methods and instance variables (collectively: "attributes") should be public or non-public.
If in doubt, choose non-public; it's easier to make it public later than to make a public attribute non-public.

Public attributes are those that you expect unrelated clients of your class to use, with your commitment to avoid backward incompatible changes.
Non-public attributes are those that are not intended to be used by third parties; you make no guarantees that non-public attributes won't change or even be removed.

We don't use the term "private" here, since no attribute is really private in Python (without a generally unnecessary amount of work).
Another category of attributes are those that are part of the "subclass API" (often called "protected" in other languages).
Some classes are designed to be inherited from, either to extend or modify aspects of the class's behavior.
When designing such a class, take care to make explicit decisions about which attributes are public, which are part of the subclass API, and which are truly only to be used by your base class.

For simple public data attributes, it is best to expose just the attribute name, without complicated accessor/mutator methods.
Keep in mind that Python provides an easy path to future enhancement, should you find that a simple data attribute needs to grow functional behavior.
In that case, use properties to hide functional implementation behind simple data attribute access syntax.

- Note 1: Properties only work on new-style classes.

- Note 2: Try to keep the functional behavior side-effect free, although side-effects such as caching are generally fine.

- Note 3: Avoid using properties for computationally expensive operations; the attribute notation makes the caller believe that access is (relatively) cheap.

.. _style-guide-py-super:

``super`` SHOULD NOT be used unless the author really understands the implications (e.g. in a well-understood multiple inheritance hierarchy).
----------------------------------------------------------------------------------------------------------------------------------------------

Python provides ``super`` so that each parent class' method is only called once (see https://www.python.org/download/releases/2.3/mro/).
The problem is, if you're going to use super at all, then all parent classes in the chain (also called the Method Resolution Order") need to use super otherwise the chain gets interrupted. 
Other subtleties have been noted in https://fuhm.net/super-harmful/:

- Never call super with anything but the exact arguments you received, unless you really know what you're doing.
- When you use it on methods whose acceptable arguments can be altered on a subclass via addition of more optional arguments, always accept ``*args, **kw``, and call ``super`` like ``super(MyClass, self).currentmethod(alltheargsideclared, *args, **kwargs)``.
  If you don't do this, forbid addition of optional arguments in subclasses.
- Never use positional arguments in ``__init__`` or ``__new__``.
  Always use keyword args, and always call them as keywords, and always pass all keywords on to ``super``.


.. _style-guide-py-comparisons:

9. Comparisons
==============

.. _style-guide-py-comp-is:

``is`` and ``is not`` SHOULD only be used if determining if two variables point to same object
----------------------------------------------------------------------------------------------

Use ``is`` or ``is not`` only for the case that you need to know that two variables point to the exact same object.

To test equality in *value*, use ``==`` or ``!=`` instead.

.. _style-guide-py-comp-none:

``is`` and ``is not`` SHOULD be used when comparing to ``None``
---------------------------------------------------------------

There are two reasons:

1. ``is None`` works with NumPy arrays, whereas ``== None`` does not;
2. ``is None`` is idiomatic.

This is also consistent with :pep:`8`, which `states <https://www.python.org/dev/peps/pep-0008/#id49>`__:

   Comparisons to singletons like ``None`` should always be done with ``is`` or ``is not``, never the equality operators.

For sequences, (`str`, `list`, `tuple`), use the fact that empty sequences are ``False``. 

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

Idiomatic Python also reduces technical debt, particularly by easing the migration from Python 2.7 to Python 3.
Codes should be written in a way that helps the futurize_ code converter produce more efficient code.
For more information see the online book `Supporting Python 3 <http://python3porting.com/toc.html>`_ by Lennart Regebro.

.. _futurize: http://python-future.org/futurize.html

.. _style-guide-py-pitfalls-mutables:

A mutable object MUST NOT be used as a keyword argument default
---------------------------------------------------------------

Never use a mutable object as default value for a keyword argument in a function or method.

When used a mutable is used as a default keyword argument, the default *can* change from one call to another leading to unexpected behavior.
This issue can be avoided by only using immutable types as default.

For example, rather than provide a default empty list:

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

.. _style-guide-py-open:

Use ``open`` instead of ``file``
--------------------------------

``file`` is gone in Python 3.

.. _style-guide-py-subprocess:

The ``subprocess`` module SHOULD be used to spawn processes
-----------------------------------------------------------

Use the :py:mod:`subprocess` module to spawn processes.

.. _style-guide-py-lambda:

``lambda`` SHOULD NOT be used
-----------------------------

Avoid the use of `lambda <https://docs.python.org/3/reference/expressions.html#lambda>`__.
You can almost always write clearer code by using a named function or using the :py:mod:`functools` module to wrap a function.

.. _style-guide-py-set:

The ``set`` type SHOULD be used for unordered collections
---------------------------------------------------------

Use the :py:class:`set` type for unordered collections of objects.

.. _style-guide-py-argparse:

The ``argparse`` module SHOULD be used for command-line scripts 
---------------------------------------------------------------

Use the :py:mod:`argparse` module for command-line scripts.

Command line tasks for pipelines should use :lclass:`lsst.pipe.base.ArgumentParser` instead.

.. _style-guide-py-future-division:

Use ``from __future__ import division``
---------------------------------------

This means ``/`` is floating-point division and ``//`` is truncated integer division, regardless of the type of numbers being divided.
This gives more predictable behavior than the old operators, avoiding a common source of obscure bugs.
It also makes intent of the code more obvious.

.. _style-guide-py-future-absolute-import:

Use ``from __future__ import absolute_import``
----------------------------------------------

In addition, import local modules using relative imports (e.g. ``from . import foo`` or ``from .foo import bar``).
This results in clearer code and avoids shadowing global modules with local modules.

.. _style-guide-py-exception-as:

Use ``as`` when catching an exception
-------------------------------------

For example, use ``except Exception as e`` or ``except (LookupError, TypeError) as e``.
The new syntax is clearer, especially when catching multiple exception classes, and required in Python 3.

.. _style-guide-py-generators:

Iterators and generators SHOULD be used to iterate over large data sets efficiently
-----------------------------------------------------------------------------------

Use iterators, generators (classes that act like iterators) and generator expressions (expressions that act like iterators) to iterate over large data sets efficiently.

.. _style-guide-py-future-itervalues:

Use ``itervalues()`` and ``iteritems()`` instead of ``values()`` and ``items()``
--------------------------------------------------------------------------------

For iterating over dictionary values and items use the above idiom unless you truly need a list.

This pattern does not apply to code that has already been ported to Python 3 with futurize_
For more information see http://python-future.org/compatible_idioms.html#iterating-through-dict-keys-values-items.

.. _style-guide-py-dict-keys:

Avoid ``dict.keys()`` and ``dict.iterkeys()``
---------------------------------------------

For iterating over keys, iterate over the dictionary itself, e.g.:

.. code-block:: py

   for x in mydict:
       pass
   
To test for inclusion use ``in``:

.. code-block:: py

    if key in myDict:
        pass
    
This is preferred over ``keys()`` and ``iterkeys()`` and avoids the issues mentioned in the previous item.

.. _style-guide-py-print:

Use from ``__future__ import print_function``
---------------------------------------------

The :py:func:`print()` function is required in Python 3.

In general, DM code should be use logging instead of ``print`` statements.

.. _style-guide-py-next:

Use ``next(myIter)`` instead of ``myIter.next()``
-------------------------------------------------

The special method ``next`` has been renamed to ``__next__`` in Python 3.
This allows iterators to be advanced with the :py:func:`next` built-in function in both Python 2.7 and Python 3.
