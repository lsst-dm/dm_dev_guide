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

Flake8 installation
^^^^^^^^^^^^^^^^^^^

Linters are installable with :command:`pip`:

.. code-block:: bash

   pip install flake8
   pip install pep8-naming

Flake8 command line invocation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   flake8 --ignore=E133,E226,E228,N802,N803 --max-line-length=110 {{python_dir}}

where ``{{python_dir}}`` is a directory with Python source files.

Flake8 configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^

LSST DM Packages may also include a :file:`setup.cfg` file with `PEP 8`_ exceptions:

.. code-block:: ini

	[flake8]
	max-line-length = 110
	ignore = E133, E226, E228, E251, N802, N803

:command:`flake8` can be invoked without arguments when this configuration is present.

Summary of PEP 8 exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

These error codes can be **ignored** by flake8_ when checking DM code against PEP 8 specifications:

E133
   Closing bracket is missing indentation.

E226
   Missing whitespace around arithmetic operator.

E228
   Missing whitespace around bitwise or shift operator.

E251
   Unexpected spaces around keyword / parameter equals.

N802
   Function name should be lowercase.

N803
   Argument name should be lowercase.

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

   autopep8 {{python_dir}} --in-place --recursive \
       --ignore E133,E226,E228,N802,N803 --ma-line-length 110

where ``{{python_dir}}`` is a directory with Python source files.

:command:`autopep8` changes must always be validated before committing.

Style changes must be encapsulated in a distinct commit (see :ref:`git-commit-organization-logical-units` in :doc:`Workflow document <../processes/workflow>`).

.. note::

   :command:`autopep8` only fixes PEP 8 issues and does not address other guildelines listed here.

.. _autopep8: https://pypi.python.org/pypi/autopep8

.. _style-guide-py-naming:

2. Naming Conventions
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

.. _style-guide-py-naming-functions:

Module methods (free functions) SHOULD be camelCase with leading lowercase
--------------------------------------------------------------------------

`Opposes PEP 8 <https://www.python.org/dev/peps/pep-0008/#id45>`__.

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

.. _style-guide-py-inheritance:

3. Designing for Inheritance
============================

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

.. _style-guide-py-files:

4. Source Files & Modules
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

.. note:: Delete mention of test suites?

.. _style-guide-py-string-handling:

5. String Handling
==================

.. _style-guide-py-string-5-1:

String methods SHOULD be used instead of the string module
----------------------------------------------------------

Use `string methods <https://docs.python.org/2/library/stdtypes.html#string-methods>`_ instead of the :py:mod:`string` module.
String methods are always much faster and share the same API with unicode strings.

.. _style-guide-py-string-5-2:

``.startswith()`` and ``.endswith()`` SHOULD be used to check for prefixes or suffixes
--------------------------------------------------------------------------------------

Use :py:meth:`str.startswith()` and :py:meth:`str.endswith()` instead of string slicing to check for prefixes or suffixes; they are cleaner and less error prone.

.. _style-guide-py-string-5-3:

String literals SHOULD NOT rely on trailing whitespace
------------------------------------------------------

Don't write string literals that rely on significant trailing whitespace.
Such trailing whitespace is visually indistinguishable and some editors (or more recently, :file:`reindent.py`) will trim them.

.. _style-guide-py-comparisons:

6. Comparisons
==============

.. _style-guide-py-6-1:

``is`` and ``is not`` SHOULD only be used if determining if two variables point to same object
----------------------------------------------------------------------------------------------

Avoid comparing with ``is`` and ``is not`` unless you really mean it.
Use ``is`` or ``is not`` only for the very rare case that you need to know that two variables point to the exact same object.
Usually you only care whether two objects have the same value, in which case use ``==`` or ``!=``.

.. _style-guide-py-6-2:

``is`` and ``is not`` SHOULD be used when comparing to ``None``
---------------------------------------------------------------

There are two reasons:

1. ``is None`` works with NumPy arrays, whereas ``== None`` does not;
2. ``is None`` is idiomatic.

This is also consistent with :pep:`8` which states:

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

.. _style-guide-py-6-3:

A conditional test of a boolean value SHOULD not explicitly test against ``True`` or ``False``
----------------------------------------------------------------------------------------------

Don't compare boolean values to ``True`` or ``False`` using ``==`` (unless it matters, e.g. for tri-state logic).

Yes:

.. code-block:: py

   if greeting:

No:

.. code-block:: py

   if greeting == True:
       pass

   if greeting is True:
       pass

.. _style-guide-py-pitfalls:

7. Programming Pitfalls
=======================

.. _style-guide-py-7-1:

``if x`` SHOULD NOT be used when you mean ``if x != None``
----------------------------------------------------------

Beware of writing ``if x`` when you mean ``if x != None``.
This often comes up when testing whether a variable or argument that defaults to ``None`` was set to some other value.
The other value might have a type (such as a container) that could be ``False`` in a boolean context!

.. _style-guide-py-7-2:

A mutable object MUST NOT be used as default in arg list
--------------------------------------------------------

Never use a mutable object as default value in a function or method argument list.
The problem is that the default value may itself change, leading to subtle bugs.
This problem bites many new Python programmers, though usually only once.
To avoid the problem use something like the following: 

.. code-block:: py

   def proclist(alist=None):
   if alist == None:
   alist = []

   # if you can tolerate a tuple; tuples are immutable
   def proclist(alist=()):
       pass

Rather than the more obvious but dangerously wrong: 

.. code-block:: py

   def proclist(alist=[]):
       pass

.. _style-guide-py-7-3:

Object type comparisons SHOULD always use ``isinstance()``
----------------------------------------------------------

Object type comparisons should always use :py:func:`isinstance()` instead of comparing types directly. 

Yes:

.. code-block:: py

   if isinstance(obj, int):
       pass

.. code-block:: py

   if type(obj) is type(1):
       pass

When checking if an object is a string, keep in mind that it might be a unicode string too! Starting with Python 2.3, `str` and `unicode` have a common base class, `basestring`, so you can do: 

.. code-block:: py

   if ``isinstance(obj, basestring)``:

.. _style-guide-py-7-4:

In function calls ``*`` and SHOULD be used instead of ``apply``
---------------------------------------------------------------

In old versions of Python, to call a function with an argument list and/or keyword dictionary you had to write ``apply(func, args, keyargs)``.
Now you can write ``func(*args, keyargs)``, which is faster and clearer.

.. _style-guide-py-recommendations:

8. Programming Recommendations
==============================

Try to make your Python code idiomatic (*pythonic*).
Consider the following, slightly adapted from Tim Peters' `The Zen of Python <http://www.python.org/dev/peps/pep-0020>`_:

| Beautiful is better than ugly. 
| Explicit is better than implicit. 
| Simple is better than complex. 
| Complex is better than complicated. 
| Flat is better than nested. 
| Sparse is better than dense. 
| Readability counts. 
| Special cases aren't special enough to break the rules. 
| Although practicality beats purity. 
| Errors should never pass silently. 
| Unless explicitly silenced. 
| In the face of ambiguity, refuse the temptation to guess. 
| There should be one---and preferably only one---obvious way to do it. 
| If the implementation is hard to explain, it's a bad idea. 
| If the implementation is easy to explain, it may be a good idea.

.. _style-guide-py-8-1:

Idiomatic modern Python SHOULD be used
--------------------------------------

The Python language has evolved with time.
Learn the new features of Python and use them where appropriate to make your code simpler and more readable.
For example:

- Use iterators, generators (classes that act like iterators) and generator expressions (expressions that act like iterators) to iterate over large data sets efficiently.
  (New in Python 2.2, except generator expressions were added in 2.4 and generators were slightly enhanced in Python 2.5.)

- Use the ``with`` statement to simplify resource allocation.
  (New in Python 2.5.)
  For example to be sure a file will be closed when you are done with it: 
  
  .. code-block:: py

     with open('/etc/passwd', 'r') as f:
         for line in f:
             pass

The LSST environment currently supports Python 2.7.x.
Do not use features that are not available in these versions of Python.

.. _style-guide-py-8-2:

Python 2.5 improved Exception Handling SHOULD be used
-----------------------------------------------------

To catch all errors but let :py:exc:`~exceptions.SystemExit` and :py:exc:`~exceptions.KeyboardInterrupt` through, use:

.. code-block:: py

   except Exception, e:
       pass

The exception hierarchy in Python 2.5 was improved, eliminating the need to use this: 

.. code-block:: py

   except (SystemExit, KeyboardInterrupt):
       raise
       except Exception, e:
           pass

.. _style-guide-py-8-3:

``raise ValueError('message')`` SHOULD be used instead of the deprecated form
-----------------------------------------------------------------------------

When raising an exception, use ``raise ValueError('message')`` instead of the older, deprecated form ``raise ValueError, 'message'``.

.. _style-guide-py-suggested-modules:

9. Suggested Modules
====================

.. _style-guide-py-9-1:

The ``subprocess`` module SHOULD be used to spawn processes
-----------------------------------------------------------

Use the :py:mod:`subprocess` module to spawn processes.
This supersedes and unifies :py:func:`os.system`, ``os.spawn``, :py:func:`os.popen`, etc..
New in Python 2.3.

.. _style-guide-py-9-2:

``lambda`` SHOULD NOT be used
-----------------------------

Avoid the use of ``lambda``.
You can almost always write clearer code by using a named function or using the :py:mod:`functools` module to wrap a function.

.. _style-guide-py-9-3:

The ``set`` type SHOULD be used for unordered collections
---------------------------------------------------------

Use the :py:class`set` type for unordered collections of objects.
New in Python 2.4 (though available via the ``Set`` module in Python 2.3).

.. _style-guide-py-9-4:

The ``argparse`` module SHOULD be used for command-line scripts 
---------------------------------------------------------------

Use the :py:mod:`argparse` module for command-line scripts.

.. _style-guide-py-9-5:

Pychecker or pylint SHOULD be used to check your code
-----------------------------------------------------

Check your code with `pychecker <http://pychecker.sourceforge.net>`_ or `pylint <http://www.pylint.org>`_.

.. _style-guide-py-py3:

10. Python 3 Idioms
===================

It is possible to write much of the Python code in a way that will run well under both Python 2.7 and Python 3.x, without harming readability (and in some cases, improving it).
There are other cases where code can be written in a way that helps the 2to3_ code converter produce more efficient code.

.. _2to3: https://docs.python.org/2/library/2to3.html

.. _style-guide-py-10-1:

Use ``from __future__ import division``
---------------------------------------

This means ``/`` is floating-point division and ``//`` is truncated integer division, regardless of the type of numbers being divided.
This gives more predictable behavior than the old operators, avoiding a common source of obscure bugs.
It also makes intent of the code more obvious.

.. _style-guide-py-10-2:

Use ``from __future__ import absolute_import``
----------------------------------------------

In addition, import local modules using relative imports (e.g. ``from . import foo`` or ``from .foo import bar``).
This results in clearer code and avoids shadowing global modules with local modules.
It also makes 2to3_ conversion more reliable.

.. _style-guide-py-10-3:

Use ``itervalues()`` and ``iteritems()`` instead of ``values()`` and ``items()``
--------------------------------------------------------------------------------

For iterating over dictionary values and items use the above idiom unless you truly need a list.
This generates more efficient code today and helps 2to3_ generate more efficient code in the future.
For more information see http://python3porting.com/preparing.html#optional-use-the-iterator-methods-on-dictionaries.

.. _style-guide-py-10-4:

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

.. _style-guide-py-10-5:

Replace ``file`` with ``open``
------------------------------

This is preferred and ``file`` is gone in Python 3.

.. _style-guide-py-10-6:

Use ``as`` when catching an exception
-------------------------------------

For example, use ``except Exception as e`` or ``except (LookupError, TypeError) as e``.
The new syntax is clearer, especially when catching multiple exception classes, and the old syntax does not work in Python 3.

.. _style-guide-py-10-7:

Use from ``__future__ import print_function``
---------------------------------------------

Minor, but provides forward compatibility.
This will affect very little code since we rarely use print.

.. _style-guide-py-10-8:

Use ``next(myIter)`` instead of ``myIter.next()``
-------------------------------------------------

This is preferred, and the special method ``next`` has been renamed to ``__next__`` in Python 3.

For more information see  http://python3porting.com/toc.html, among several useful references.

.. _style-guide-py-layout:

11. Layout
==========

.. _style-guide-py-11-1:

Basic indentation MUST be 4 spaces
----------------------------------

Use 4 spaces per indentation level.

This width provides a good balance between readability and excessive indentation.
Using spaces instead of tabs assures that the code may be edited with all common editors and displayed with all common displays without special configuration.

For an old code package that you don't wish to alter too far, you may use its existing indentation method with one exception, no tabs.

.. _style-guide-py-11-2:

Use of special character TAB is PROHIBITED
------------------------------------------

Existing code that mixes tabs and spaces must be converted to use 4 spaces per indentation level.

To check a file you may invoke the Python command line interpreter with the ``-t/-tt`` option, it issues warnings/errors about code that illegally mixes tabs and spaces.

.. _style-guide-py-11-3:

Line Length MUST be less than or equal to 110 columns
-----------------------------------------------------

Limit all lines to a maximum of 110 characters.
This conforms to the :doc:`cpp_style_guide` (see :ref:`4-6 <style-guide-cpp-4-6>`).

.. _style-guide-py-11-4:

Python's implied continuation inside parens, brackets and braces SHOULD be used for wrapped lines
-------------------------------------------------------------------------------------------------

The preferred way of wrapping long lines is by using Python's implied line continuation inside parentheses, brackets and braces.
If necessary, you can add an extra pair of parentheses around an expression, but sometimes using a backslash looks better.
Make sure to indent the continued line appropriately. Some examples:

.. code-block:: py

    class Rectangle(Blob):
        """Documentation for Rectangle.
        """
        def __init__(self, width, height,
                     color='black', emphasis=None, highlight=0):
            if width == 0 and height == 0 and
               color == 'red' and emphasis == 'strong' or
               highlight > 100:
                raise ValueError("sorry, you lose")
            if width == 0 and height == 0 and (color == 'red' or
                                               emphasis is None):
                raise ValueError("I don't think so")
            Blob.__init__(self, width, height,
                          color, emphasis, highlight)

.. _style-guide-py-11-5:

Blank Lines SHOULD be used to enhance readability
-------------------------------------------------

Use blank lines to make your code readable.
The following are recommendations:

- Separate top-level function and class definitions with two blank lines.

- Separate method definitions inside a class by a single blank line.

- Do not use a blank line on either side of a doc string.

- Use blank lines in functions, sparingly, to indicate logical sections.

- Extra blank lines may be used (sparingly) to separate groups of related functions.

- Blank lines may be omitted between a bunch of related one-liners (e.g. a set of dummy implementations).

.. _style-guide-py-11-6:

A package SHOULD be imported on one line
----------------------------------------

Each package should be imported on one line.
For example, this is preferred: 

.. code-block:: py

   import os
   import sys
   from subprocess import Popen, PIPE

Whereas this is not: 

.. code-block:: py

    # two packages imported on one line
    import sys, os
    # one package imported on two lines
    from subprocess import Popen
    from subprocess import PIPE

.. _style-guide-py-11-7:

Consistency with the DM C++ Coding Guide namespaces SHOULD be followed
----------------------------------------------------------------------

Consistency with the LSST C++ Coding Standards namespaces exists.

**Good:**

- ``from lsst.foo.bar import myFunction`` is analogous to ``using lsst::foo::bar::myFunction``

- ``import lsst.foo.bar as fooBar`` is analogous to ``namespace fooBar = lsst::foo::bar``

**Disallowed** in both Coding Standards (except in __init__.py library initialization context):

- ``from lsst.foo.bar import *`` is analogous to ``using namespace lsst::foo::bar``

.. _style-guide-py-whitespace:

12. Whitespace
==============

.. _style-guide-py-12-1:

Extraneous Whitespace SHOULD be avoided
---------------------------------------

Avoid extraneous whitespace in the following situations:

- immediately inside parentheses, brackets or braces:

  Yes: ``spam(ham[1], {eggs: 2})``

  No: ``spam( ham[ 1 ], { eggs: 2 } )``

- immediately before a comma, semicolon, or colon: 

  Yes: ``if x == 4: print x, y; x, y = y, x``

  No: ``if x == 4 : print x , y ; x , y = y , x``

- immediately before the open parenthesis that starts the argument list of a function call:

  Yes: ``spam(1)``

  No:  ``spam (1)``

- immediately before the open parenthesis that starts an indexing or slicing: 

  Yes: ``dict['key'] = list[index]``

  No:  ``dict ['key'] = list [index]``

- More than one space around an assignment (or other) operator to align it with another.
  Make an exception if alignment makes the data significantly clearer (e.g. complex lookup tables).

  Thus: 

  .. code-block:: py

     x = 1
     y = 2
     long_variable = 3

  Not this:

  .. code-block:: py

     x             = 1
     y             = 2
     long_variable = 3

.. _style-guide-py-12-2:

The minimum number of parenthesis needed for correctness and readability SHOULD be used
---------------------------------------------------------------------------------------

Yes:

.. code-block:: py

   a = b(self.config.nSigmaToGrow*sigma + 0.5)

Less readable:

.. code-block:: py

   a = b((self.config.nSigmaToGrow*sigma) + 0.5)
 
.. _style-guide-py-12-3:

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
- modulus (``%``).

The one exception is assigning values to multiple keyword arguments on a single line, where spaces around "=" obscure the separation between the separate arguments. 
Thus this: 

.. code-block:: py

   i = i + 1
   submitted += 1
   x = x*2 - 1
   hypot2 = x*x + y*y
   c = (a + b)*(a - b)
   funcA(
       karg1 = value1,
       karg2 = value2,
       karg3 = value3,
   )
   funcB(x, y, z, karg1=value1, karg2=value2, karg3=value3)

Not this: 

.. code-block:: py

   i=i+1
   submitted +=1
   x = x * 2 - 1
   hypot2 = x * x + y * y
   c = (a+b) * (a-b)
   funcA(
       karg1=value1,
       karg2=value2,
       karg3=value3,
   )
   aFunction(x, y, z, karg1 = value1, karg2 = value2, karg3 = value3)
 
.. _style-guide-py-12-4:

Spaces MUST NOT be used around ``=`` for Default Parameter
----------------------------------------------------------

Don't use spaces around the ``=`` sign when used to indicate a default parameter value.

Thus this:

.. code-block:: py

   def complex(real, imag=0.0):
       pass

but not this:

.. code-block:: py

   def complex(real, imag = 0.0):
       pass

.. _style-guide-py-comments:

13. Comments
============

.. _style-guide-py-13-1:

Comments MUST always remain up-to-date with code changes
--------------------------------------------------------

Comments that contradict the code are worse than no comments.
Always make a priority of keeping the comments up-to-date when the code changes!

.. _style-guide-py-13-2:

Comments SHOULD be complete sentences
-------------------------------------

Comments should be complete sentences.
If a comment is a phrase or sentence, its first word should be capitalized, unless it is an identifier that begins with a lower case letter (never alter the case of identifiers!).

If a comment is short, the period at the end can be omitted.
Block comments generally consist of one or more paragraphs built out of complete sentences, and each sentence should end in a period.

You need not use two spaces after a sentence-ending period.

When writing English, *Strunk and White* apply.

.. _style-guide-py-13-3:

Block comments SHOULD reference the code following them and SHOULD be indented to the same level
------------------------------------------------------------------------------------------------

Block comments generally apply to some (or all) code that follows them, and are indented to the same level as that code.
Each line of a block comment starts with a ``#`` and a single space (unless it is indented text inside the comment).

Paragraphs inside a block comment are separated by a line containing a single #.

.. _style-guide-py-13-4:

Inline Comments MAY be sparingly used
-------------------------------------

Use inline comments sparingly.
Inline comments are unnecessary and in fact distracting if they state the obvious.

Don't do this: 

.. code-block:: py

   x = x + 1      # Increment x

But sometimes, this is useful: 

.. code-block:: py

   x = x + 1      # Compensate for border

.. _style-guide-py-13-5:

Inline comments SHOULD be separated by at least two spaces from the statement
-----------------------------------------------------------------------------

An inline comment is a comment on the same line as a statement.
Inline comments should be separated by at least two spaces from the statement.
They should start with a ``#`` (i.e., sharp sign and a single space).

.. _style-guide-py-docstrings:

14. Documentation Strings
=========================

Read the `DM Documentation Standards <https://dev.lsstcorp.org/trac/wiki/DocumentationStandards>`_ for the definitive formatting guidelines for DM python source files.

Read :pep:`257` for the pythonic discussion of docstrings.
This is your main resource for information on writing doc strings.
Here are a few minor points and emendations:

.. _style-guide-py-14-1:

Docstrings SHOULD be written for all public modules, functions, classes, and methods
------------------------------------------------------------------------------------

Write docstrings for all public modules, functions, classes, and methods.

Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does.
This comment should appear after the ``def`` line.

.. _style-guide-py-14-2:

Docstrings SHOULD start with a 1-line imperative summary ending in a period
---------------------------------------------------------------------------

Start the doc string with a one-line summary, a phrase ending in a period.
Prescribe the function or method's effect as a command ("Do this", "Return that"), not as a description; e.g. don't write "Returns the pathname ...".

.. _style-guide-py-14-3:

Docstrings for functions, classes, and methods SHOULD include argument descriptions, return value, error conditions
-------------------------------------------------------------------------------------------------------------------

After the docstring's summary line, if more information is wanted (as it usually is), include it after a blank line.
This usually should include a description of the arguments, return value and important error conditions.

If you mention arguments or other variables, always use their correct case.

Docstrings should not be preceded or followed by a blank line.

.. _style-guide-py-14-4:

Docstrings SHOULD be begin with ``"""`` and terminate with ``"""`` on its own line
----------------------------------------------------------------------------------

Delimit doc strings with ``"""`` (three double quotes). You may use ``u"""`` for unicode but it is usually preferable to stick to ASCII.
The terminating """ should be on its own line, even for one-line doc strings (this is a minor departure from :pep:`257`).

.. code-block:: py

   """Return a foobang
    
   Optional plotz says to frobnicate the bizbaz first.
   """
