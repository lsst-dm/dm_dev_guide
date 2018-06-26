.. _generic-guide-topic:

########################
Generic guide topic type
########################

The generic guide topic type is the template to use when writing guides that are not covered by more specific topic types.

.. note::

   As topic types are introduced for how-to guides, tutorials, conceptual overviews, tasks, and so on, we should migrate topics written with the generic guide topic type to those more specific topic types.

.. _generic-guide-topic-filename:

File name and location
======================

Topics are reStructuredText files with an ``rst`` extension.

If the topic is associated with a module, the topic’s file is located in the :ref:`module documentation directory <docdir-module-doc-directories>`.
For example:

.. code-block:: text

   doc/lsst.example/my-topic.rst

If the topic is associated with a package, the topic’s file is located in the :ref:`package documentation directory <docdir-package-doc-directory>`.
For example:

.. code-block:: text

   doc/example/my-topic.rst

In general, you shouldn’t create additional subdirectories to organize these files so that URLs are clean and simple.

Use these guidelines for naming the file:

- Name the file by adapting the title into a short phrase.

- Connect words with a single hyphen (``-``) character.
  You may only use periods (``.``) and underscores (``_``) when the file name includes an API that naturally contains periods and underscores.

- Use lowercase, except for API names that naturally include uppercase characters.

.. _generic-guide-topic-preamble:

Preamble
========

If a topic is located in a :ref:`module documentation directory <docdir-module-doc-directories>`, you should add a ``py:currentmodule`` directive at the top of the file.
For example, if the module’s name is ``lsst.example``, the directive is written as:

.. code-block:: rst

   .. py:currentmodule:: lsst.example

This allows you to reference APIs relative to that base namespace.
For example these two Python API cross-references are equivalent:

.. code-block:: rst

   `MyClass` and `lsst.example.MyClass`.

If a topic is located in a :ref:`package documentation directory <docdir-package-doc-directory>`, you generally shouldn’t use the ``py:currentmodule`` directive.

.. _generic-guide-topic-title:

Title
=====

Title the topic according to these guidelines:

- Use sentence case.
  The first word is capitalized and following words are not, unless they are proper nouns or API names with capital letters.

- Ensure that the title is descriptive so that the readers know what to expect from the page's content.
  Titles are used in page lists (``toctree``\ s) and inline links (``doc`` and ``ref`` roles), so the title needs to stand on its own.
  Don't rely on document hierarchy or the previous/next pages to provide any context to the title.
  If the topic is about an API, be sure to name that API in the title.

- If there are several related topics, using a similar style and structure for naming each of those topics.

.. _generic-guide-topic-context:

Context paragraph
=================

Directly after the title, include one or two paragraphs that establishes the topic and its context.
You should describe what the reader will learn from the page.
You can also link to related topics.

Readers will use this context paragraph to navigate through the documentation.
A usable context paragraph will help the reader quickly establish whether the topic is relevant to their task, and if not, to navigate to other closely-related topics.

.. _generic-guide-topic-sections:

Sections
========

Use sections liberally to make the page easier to skim.
Remember that few people read a page from top to bottom.
Section headlines provide entry points into the content.

Readers also use section headlines to assess whether the page includes content relevant to their task.
Design your sections and headers so that readers don’t accidentally skip over your page.

Use sentence case for all section headlines.
In general, you should add cross-reference targets to all your section headlines.
See :ref:`rst-sectioning` for example of sections with cross-reference targets.

Don’t create hierarchies that are deeper than two levels (that is, subsections but not sub-subsections), if possible.
Flatter hierarchies are easier for a reader to keep track of and navigate.

.. _generic-guide-topic-further-reading:

Further reading section
=======================

At the bottom of the page, consider adding a section called “Further reading.”
In this section, you can add a list of links to other pages that are related to the current page.
Generally you can use the ``doc`` role to create a link to a page that automatically populates the linked page’s title.
For example:

.. code-block:: rst

   Further reading
   ===============

   - :doc:`page-a`
   - :doc:`page-b`
   - :doc:`/modules/lsst.pipe.base/absolute-link`
