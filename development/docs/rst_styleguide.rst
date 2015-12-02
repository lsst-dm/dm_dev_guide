############################
ReStructuredText Style Guide
############################

This page describes how reStructuredText (reST) is written for DM documentation.
The first sections are example-based introduction to reST markup, while the :ref:`last section documents formatting conventions <rst-formatting-guidelines>`.

For more exhaustive guides to writing reStructuredText, see Sphinx's `reStructuredText Primer <http://sphinx-doc.org/rest.html#explicit-markup>`_ and the `docutils Quick reStructuredText guide <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_.

See the pages on :doc:`writing documentation for packages <package_docs>` and :doc:`Python docstrings <py_docs>` for specific reST usage in those contexts.

.. _rst-intro-sample:

Sample
======

.. literalinclude:: rst_sample.rst
   :language: rst

:doc:`See this sample rendered <rst_sample>`.

.. _rst-inline-styles:

Inline Text Styling
===================

Italics: ``*italic text*`` → *italic text*.

Bold: ``**bold text**`` → **bold text**.

Monospace: ````monospace text```` → ``monospace text``.
When referring to code objects, it's better to use different markup that links to the object's API documentation.
This is described below in the :ref:`rst-code-link` section.

To render inline math, use the ``math`` role: ``:math:`\sqrt{16}``` → :math:`\sqrt{16}`.

Inline styles can't be nested.
For example, you *can't* write ``*see :ref:`this page <label>`*``.

Inline markup also needs to be surrounded by white space, though trailing punctuation is fine.
You can get around this with an *escaped space* that is otherwise invisible,
For example ``one\ *word*`` renders as one\ *word*.

.. _rst-lists:

Lists
=====

Unordered lists can be written as

.. code-block:: rst

   - First item

     Second paragraph for first item, needs to be consistently indented.
   - Second item

   - You can put spaces between items, or not.

   - Hierarchical lists are also possible

     - Put a blank space before the sub-list
     - And indent the sub-list consistently

   - Last item.

which renders as:

   - First item
   
     Second paragraph for first item, needs to be consistently indented.
   - Second item
   
   - You can put spaces between items, or not.
   
   - Hierarchical lists are also possible

     - Put a blank space before the sub-list
     - And indent the sub-list consistently
   
   - Last item.

Enumerated lists can be written similarly:

.. code-block:: rst

   1. First thing
   2. Second thing
   
   or automatically enumerated,

   #. First thing
   #. Second thing

which renders as:

   1. First thing
   2. Second thing
   
   or automatically enumerated,
   
   #. First thing
   #. Second thing

.. _rst-sectioning:

Sections
========

We create section hierarchies as follows:

.. literalinclude:: rst_section_sample.rst
   :language: rst

:doc:`See this sample rendered <rst_section_sample>`.

This specific sequence of section markup styles is not mandated by the reST specification, but we encourage you to use it for consistency across all reST documents.

Note that sections in Python docstrings are a special case. First, :ref:`we do not place a blank space between a section header and the object lists below <py-doc-docstring-rst>`.
Second, :ref:`Python docstrings can only use subsection and subsubsection-level headings <py-doc-section-levels>`.

.. _rst-linking:

Linking
=======

.. _rst-external-links:

External Links
--------------

Links to external web pages can be made two ways.
The first, recommended, way is

.. code-block:: rst

   When writing Python, it's a good idea to use the `PEP8 style guide`_.

   .. _PEP8 style guide: https://www.python.org/dev/peps/pep-0008/

The link reference should be provided directly following the paragraph to make it easier for editors to ensure the text in backticks matches the link reference line.
Despite this fragility, this style is good since it makes the reST itself more readable.

The second method is to put the URL inline:

.. code-block:: rst

   When writing Python, it's a good idea to use the
   `PEP8 style guide <https://www.python.org/dev/peps/pep-0008/>`_.

You may decide to use either method, taking readability into consideration.

.. _rst-internal-links:

Internal Links to Labels
------------------------

Any content block can be labeled.
For example, to give a section the label ``making-labels``, we write:

.. code-block:: rst

   .. _making-labels:

   Making Labels
   -------------

   Labels are an empty directive that appear directly before any block, such
   as a section, image, table, or code block.
   Labels start with an underscore, and words in labels are separated by
   hyphens.
   Labels are a **global namespace**, so make them as specific as possible.

Then you can link to any labeled block with the ``:ref:`` role.

.. code-block:: rst

   For internal links, :ref:`you'll need to make labels <making-labels>`.

You can also make references with ``:ref:`label-name```, and the link text will automatically be populated with the section title, or figure caption, for example.

.. _rst-doc-link:

Internal Links to other Pages
-----------------------------

To link to another page in the stack docs, use the ``doc`` role with the **relative path** to the target ``.rst`` document.

.. code-block:: rst

   See our :doc:`Styleguide <rst_styleguide>` to learn how to write reST docs.

Note how the ``.rst`` extension wasn't included.

.. _rst-code-link:

Links to Code Objects
---------------------

When describing a code object, you can also link to that object's API definition using a syntax similar to the ``ref`` role used above.


.. _rst-python-link:

Links to Python Objects
-----------------------

Objects can be referenced with these roles:

- ``:py:mod:`package.module``` references a module *or package* with namespace ``package.module``.
- ``:py:func:`pkg.mod.function``` references a Python function at namespace ``pkg.mod.function``.
  The role's text does not need to include trailing parentheses.
- ``:py:class:`pkg.mod.Class``` to reference a class ``Class`` in ``pkg.mod``.
- ``:py:meth:`pkg.mod.Class.method``` to reference a method ``method`` in class ``Class`` in ``pkg.mod``.
- ``:py:attr:`pkg.mod.Class.attribute``` to reference an attribute ``attribute`` in class ``Class`` in ``pkg.mod``.
- ``:py:data:`pkg.mod.VARIABLE``` to reference a module-level variable ``VARIABLE`` in ``pkg.mod``.
- ``:py:const:`pkg.mod.CONSTANT``` to reference a module-level *constant* ``CONSTANT`` in ``pkg.mod``.

Namespace Resolution
^^^^^^^^^^^^^^^^^^^^

In these examples, the full namespace of each Python object is specified.
In some contexts, Sphinx may be able to identify the reference object without the full namespace.
For example in class docstrings, references to methods or attributes in the same class can be made by name alone.
See the `Sphinx documentation <http://sphinx-doc.org/domains.html#cross-referencing-python-objects>`_ for more details on object resolution.

.. _rst-cpp-links:

Links to C++ Objects
--------------------

Similarly to Python object links, Sphinx supports a ``cpp`` domain for C++ code that provides the following roles:

- ``:cpp:class:``
- ``:cpp:func:``
- ``:cpp:member:``
- ``:cpp:var:``
- ``:cpp:type:``
- ``:cpp:enum:``
- ``:cpp:enumerator:``

Note that Sphinx has several limitations for linking to C++ objects:

- A specific version of an overloaded function/method cannot be specified.
- You must escape the opening angle bracket in template classes,
  e.g. ``:cpp:class:`ClassName\<T>```.
- You cannot link to template classes/functions/aliases/variables, only template instantiations.

Customizing the Link Text
-------------------------

By default the full namespace to the object will be shown as the linked text.
To show only the name of the object itself, prefix the namespace with ``~``.
For example:

.. code-block:: rst

   :py:func:`~numpy.sin`

will be rendered as `sin() <#>`_.

As with the ``ref`` role, it is also possible to provide custom link text, e.g.:

.. code-block:: rst

   :py:func:`Numpy's sine function <numpy.sin>`

Default Domains
---------------

By default, these code referencing roles require a *domain prefix* such as ``py`` or ``cpp`` to specify the language of the object being reference.

This prefix can be omitted when the domain is implicitly set, such as in a Python docstring.

In a reStructuredText document, the domain can be set via the ``default-domain`` directive.
For example, to set the default domain for a reST document to Python, use

.. code-block:: py

   .. default-domain:: py

When this is set, Python code references can be made more concise, e.g., ``:func:`numpy.sin```.

See `Sphinx's documentation on Domains`_ for more information about referencing code objects.

.. _Sphinx's documentation on Domains: http://sphinx-doc.org/domains.html

.. _rst-tables:

Tables
======

We recommend that you use the *grid* syntax for tables, since they more flexible than `simple reST tables`_.
And although not necessary, we suggest you provide a caption using the ``table`` directive, and a label prefixed with "``table-``."
For example:

.. _simple rest tables: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#simple-tables

.. literalinclude:: snippets/basic_table.rst
   :language: rst

produces:

.. include:: snippets/basic_table.rst

Note how cells can be joined by omitting the dividing line.
The ``=`` characters divide the header from table content.
Text in the header is set in bold.

You can write tables with multiple header rows, including spans across header cells:

.. literalinclude:: snippets/multi_header_table.rst
   :language: rst

produces:

.. include:: snippets/multi_header_table.rst

.. _rst-figures:

Images and Figures
==================

Plain images can be included with the ``image`` directive.
For example:

.. code-block:: rst

   .. image:: /_static/obs_decam/camera_geometry.png

Figure Directive
----------------

*Figures* can also be produced, which include captions:

.. code-block:: rst

   .. figure:: /_static/obs_decam/camera_geometry.png
      :name: fig-figure-label
      :alt: DECam focal plane layout. This text is used for for screen readers (accessibility).

      DECam focal plane layout.

Note that the ``:name:`` field takes the place of a separate `label <rst-internal-links>`_ for hyperlinking.
By convention, these labels should be prefixed with "``fig-``."

Note on Paths to Image Files
----------------------------

Images are included in the ``_static/`` directory of the git repository for this documentation project.
Sphinx requires image assets to be located in this ``_static/`` directory in order to properly copy files into the built website.
By using a prefix "``/``" we indicate that a path is relative to the root of the documentation repository.

Package documentation is hosted in ``doc/`` directories of the git repositories of individual Stack packages.
For such package documentation, image files should be placed inside a directory in ``doc/_static/`` named for the package itself.
For example ``doc/_static/obs_decam/`` for the `obs\_decam <https://github.com/lsst/obs_decam>`_ package.
This nested directory structure is needed to merge package documentation content into the root documentation build.

.. _rst-code-blocks:

Source code
===========

For blocks of code, we prefer the ``code-block`` directive.
This directive has the form

.. code-block:: rst

   .. code-block:: <language>
      :name: optional-label
      :emphasize-lines: <optional lines to highlight>

      <code>

where

- ``<language>`` can be `any token understood by Pygments`_, particularly ``py`` (python), ``cpp`` (C++), ``java`` (Java), ``js`` (JavaScript) and ``rst`` (reStructuredText). Specify ``none`` to disable highlighting.
- ``:name:`` is an explicit hyperlink label for the code block.
- ``:emphasize-lines:`` is an optional sequence of lines to highlight. This can be comma-separated, with hyphens to indicate spans.

.. _any token understood by Pygments: http://pygments.org/docs/lexers/

For example,

.. code-block:: rst

   .. code-block:: py
      :name: context-timer-example
      :emphasize-lines: 4-13,15-17

      from contextlib import ContextDecorator
      import time
      
      class timercontext(ContextDecorator):

          def __enter__(self):
              self.start = time.clock()
              return self
      
          def __exit__(self, *args):
              self.end = time.clock()
              self.interval = self.end - self.start
              print('Duration: {0:.2e} sec'.format(self.interval))

       @timercontext
       def run_slowly():
           time.delay(1.)
       
       run_slowly()
       
       with timercontext() as t:
           time.delay(1)
       
       print('Delayed for {0:.1f}'.format(t.interval))

produces

.. code-block:: py
   :name: context-timer-example
   :emphasize-lines: 4-13,15-17

   from contextlib import ContextDecorator
   import time
   
   class timercontext(ContextDecorator):

       def __enter__(self):
           self.start = time.clock()
           return self
   
       def __exit__(self, *args):
           self.end = time.clock()
           self.interval = self.end - self.start
           print('Duration: {0:.2e} sec'.format(self.interval))

    @timercontext
    def run_slowly():
        time.delay(1.)
    
    run_slowly()
    
    with timercontext() as t:
        time.delay(1)
    
    print('Delayed for {0:.1f}'.format(t.interval))

.. _rst-lightweight-code-blocks:

Lightweight syntax for Python code and sessions
-----------------------------------------------

You can markup Python code blocks using a lightweight syntax:

.. code-block:: rst

   ::

      print('hello world!')

Interactive python sections can be marked up as

>>> print('Hello world!')
Hello world!

This lightweight syntax :ref:`is used in Python docstrings <py-docstring-examples>`.

.. _rst-prompts:

Command line prompts
====================

For generic command line prompts, we use the `sphinx-prompt`_ extension so that the prompt character (e.g, ``$``) isn't selectable.
This is great for giving copy-and-paste-ready command line instructions.

.. _sphinx-prompt: https://github.com/sbrunner/sphinx-prompt

For basic bash prompts,

.. code-block:: rst

   .. prompt:: bash

      mkdir -p hello/world
      cd hello/world

produces

.. prompt:: bash

   mkdir -p hello/world
   cd hello/world

.. _rst-footnotes:

Footnotes
=========

Footnotes should be used sparingly, if at all, in LSST documentation.
Prefer inline hyperlinks to other sections.
If you *do* need footnotes, you can make them as follows:

.. code-block:: rst

   This is a line.\ [#label]_

   .. [#label] This is the footnote content.

Note that we had to provide an escaped space for the footnote mark occurring after a period.

The footnote content should occur not far from the inline footnote mark; generally provide the footnote content at the end of the section.

.. _rst-citations:

Citations
=========

Citations should be used for scholarly references; use hyperlinks for web native content.
Citations can be made as follows:

.. code-block:: rst

   The LSST Project [Ivezic2008]_ will produce 15 TB of images per night.

   .. [Ivezic2008] Ivezic et al 2008. *LSST: from Science Drivers to
                   Reference Design and Anticipated Data Products.*
                   `arxiv:0805.2366 <http://arxiv.org/abs/0805.2366>`_

Citations are distinguished from footnotes in that the label *is not* numeric or *does not* begin with a ``#``.

In the future, scholarly citations will be easier to include and more 'latex-like' with our `documenteer`_ Sphinx extensions.

.. _documenteer: https://github.com/lsst-sqre/documenteer

.. _rst-comments:

Comments in ReStructuredText
============================

Provide comments to fellow writers using ``..``,

.. code-block:: rst

   .. This is a one-line comment.

   ..
      This is the first of a multi-paragraph comment.

      The second paragraph.

Avoid using comments to keep around old or alternate versions of text; prefer using git version control instead.

.. _rst-formatting-guidelines:

RestructuredText Formatting Conventions
=======================================

Text Wrapping
-------------

When writing reST documentation in Python files, documentation lines should be kept to lengths of :ref:`75 characters or fewer <py-doc-docstring-rst>` (discounting leading indentation).

For reStructuredText documents (e.g., ``.rst`` files), reST doesn't care about line formatting.
Emacs users, for example, are free to use hard-wrap formatting lines at 72 characters if that helps you write docs.
However, whenever possible, we *encourage* you to use soft-wrapping for your text.
The has the advantage of letting others format text columns in their editors as they wish
As well, the GitHub.com code editor does have hard-wrap auto-formatting.
Those making doc edits on GitHub.com will tend to use soft-wrap by default (see '`GitHub Flow in the Browser`_').

.. _GitHub Flow in the Browser: https://help.github.com/articles/github-flow-in-the-browser/

When using soft-wrap formatting, you might **write one sentence per line** (i.e., put a line break after each sentence).
As a writer, this the advantage of making it easier to check the rhythm of your writing, including sentence lengths.
Shorter sentences are easier to read.
`One-sentence-per-line`_ is also semantically correct in the sense of git and other version control systems.

.. _One-sentence-per-line: https://xkcd.com/1285/

At LSST, we place a **single blank line** between all content blocks, such as directives, paragraphs and lists.

Indentation
-----------

ReStructuredText should be indented consistently with the context, which generally means taking visual alignment cues rather than adhering to a fixed indent width.

In directives, align to the directive's name:

.. code-block:: rst

   .. code-block:: python

      print('hello world')

In lists, align naturally with the text:

.. code-block:: rst

   - First item.

     Another paragraph for the first item.
   - Second item.

And note how that alignment adapts to numbered lists (four spaces are now required):

.. code-block:: rst

   1. First item.

      Another paragraph for the first item.
   2. Second item.

For :ref:`argument lists in Python docstrings <py-docstring-parameters>` we indent descriptions by four spaces:

.. code-block:: rst

   Parameters
   ----------
   x : float
       Particle's x-coordinate.
   y : float
       Particle's y-coordinate.

.. _rst-encoding:

Encoding and Special Characters
-------------------------------

LSST's reStructuredText source files should be encoded as UTF-8 unicode.
This means that special characters such as en (–) and em (—) dashes can just be written as such.
We do run a variant of `smartypants`_ in an attempt to convert ``--`` and ``---`` into en and em dashes, respectively, and to covert dumb quotes (``"``) into "typographic" quotes.

.. _smartypants: http://daringfireball.net/projects/smartypants/

