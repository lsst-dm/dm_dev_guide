###############################################
Writing and structuring documentation for users
###############################################

Great documentation provides users with timely and readily consumable information to help them learn, understand, and do.
This page provides guidance on how to write and organize user documentation in ways that maximize its usability. 

The four basic types of user documentation
==========================================

When you're sitting down to write documentation, first think about what *type* of documentation content you are creating.
There are four basic types, as explained by the `Divio Documentation system`_.
Each type has its own specific purpose and content conventions:

- **Conceptual guides**.
  This type of documentation explains what a system is, what it does, and how it works.
  Conceptual guides introduce users to vocabulary and concepts.
  As always, keep your audience in mind.
  A conceptual guide is often written differently for a user than a developer or maintainer.
  Example: `About pull request reviews <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews>`__ from GitHub.

- **How-to guides**.
  This type of documentation helps a user accomplish a specific task.
  How-to guides generally feature numbered lists with specific steps to carry out.
  Since they are meant to be easy to consume, how-to guides assume the reader is qualified and link out to conceptual and reference documentation for the broad picture and the specifics.
  Example: `Creating a pull request <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request>`__ from GitHub.

- **Tutorials**.
  This type of documentation is often intended for users that are new to a product or a specific feature of a product.
  The idea is to lead the user through a realistic exercise that introduces concepts and best practices for using the product.
  Example `Creating CI tests with the Checks API <https://docs.github.com/en/developers/apps/guides/creating-ci-tests-with-the-checks-api>`__ from GitHub.

- **Reference documentation**.
  This type of documentation is a comprehensive tabulation of the aspects of a product, much like a dictionary is a reference for words in a language.
  A common type of reference is API documentation. Reference documentation strictly adheres to formatting guidelines to ensure consistency, which in turn makes a reference easier to use.

A documentation set for a product consists of all four types, and all four types work together.
A tutorial alone is cumbersome for returning users to re-consume for a specific detail.
A reference section alone doesn't provide sufficient context.
Conceptual guides provide strategy but not tactics (and vise-versa for how-tos).

In a given page of documentation you'll typically be writing in only one of these types (and in cases where multiple types occupy the same page, the different types of documentation are separated in different sections).
Each type of documentation supports the others through hyperlinks.

To learn more about writing great conceptual, how-to, tutorial, and reference documentation, see the `Divio Documentation system`_ site.

Organizing documentation in topics
==================================

The organization of documentation is a critical aspect of its usability.
We deliver documentation to our users primarily through websites, and that medium strongly informs the organization of our documentation with a practice known as **topic-based writing** (popularized by Mark Baker in `Every Page is Page One`_).

A *topic* generally corresponds to a webpage, which in turn corresponds to a source file in the project (typically reStructuredText, Markdown, or Jupyter Notebook file). 
Each topic has a number of qualities, and knowing these guidelines will help you organization your documentation.

A topic has a type
------------------

Every documentation topic (or *webpage,* to use common terminology) has a type.
In the previous section you learned about the four basic topic types: conceptual, how-to, tutorial, and reference documentation.
Each topic should follow the format of one of those types.
In larger documentation sets,  there might be specific sub-types.
For example, the topic type for documenting a command-line script, or for documenting a Python class, method, or function with Numpydoc-formatted docstring.
Topic types are essentially templates and guidelines that ensure a collection of documentation topics about similar things are all presented similarly.

It's a good idea to create new topic types when there's a need.
In DM, we often create a file template for topic types in the `lsst/templates repository <https://github.com/lsst/templates>`__ and document it in places like this Developer Guide so that other developers can easily follow the topic type.

A topic has a specific purpose and limited scope
------------------------------------------------

Each topic in a documentation set has a purpose that is distinct from all the others.
When topics have explicit scope, it's easier for a user to navigate the documentation set and understand what page to look at.
It's also easier to write and maintain documentation written this way since content isn't duplicated or spread across multiple sources.

When writing a topic, use the first paragraph of content to establish the purpose and scope of the page to the user.
If you need more guidance for yourself and other writers, you might also write a source comment at the top of the page.
While writing the page, if you need to reference information that's outside the scope of the page, use hyperlinks liberally to those other topics (and create those topics, if needed).
You may also find that, like software code, you may need to occasionally refactor topics if their original scopes turned out to be incorrect.

Another aspect of scope is *audience.*
A topic for users is often distinct from a topic for developers or maintainers.

A topic is self-contained
-------------------------

A topic is generally a single webpage.
You can expect the user to land on a webpage through any number of different routes, including arbitrary internet searches and links from different documentation pages or sites.
Therefore each topic needs to work as an entry point to the documentation. You can't assume that a reader will consume a documentation site like a book, from one page to the next.

The first paragraph of the topic is critical for establishing context (as it also is for scope).
By spelling out the purpose and scope of the page early on, the user can understand instantly if they've landed on the right page.
Include links in the first paragraph to related pages (perhaps to conceptual guides, how-to pages, reference documents) to help a user continue their information foraging.

Summary of a generic structure for a topic
------------------------------------------

Regardless of what topic type you're writing, most topics have a common structure to help readers find and consume content.
Here are some guidelines to consider when writing any documentation topic.

Webpage title
^^^^^^^^^^^^^

The title should be be concise, but provide provide accurate description of the topic.
Consider whether your title would work well both the among the contents listing of the documentation site and in isolation on a search engine results page.
If the topic is part of a collection of topics (like a collection of how-to topics), consider parallelism in the titles.

Context paragraph
^^^^^^^^^^^^^^^^^

The first paragraph of a topic is used to establish a topic's scope and context.
Consider these ingredients for the first paragraph or two of your topic:

- State plainly what the topic is about.
- State what the reader will learn or become able to accomplish by reading the page.
- Include links to prerequisite or related topics.

Your readers will use this first paragraph to determine if the page is relevant to their current task.
The links you provide can help a user efficiently move on to a more appropriate topic if necessary.

Content
^^^^^^^

How your write the content depends on the topic type (for example, a conceptual document, a tutorial, or a how-to guide).
Regardless, keep in mind our :doc:`Content style guide <index>` for crafting and structuring your words.
The next section on this page, :ref:`designing-content-for-users`, also provides guidelines for structuring content in a way that's easier to read.

"Further reading" section
^^^^^^^^^^^^^^^^^^^^^^^^^

Close your topic with a section that gives your reader some suggestions of what documentation pages (both internal and external) to read next.
This section is often titled "Further reader," or "Additional resources," or "Next steps."

.. _designing-content-for-users:

Designing content for users
===========================

The design of your content greatly impacts its usability.
Documentation is consumed on the web by busy people.
It's rare for a person to carefully read a documentation page from start-to-finish.
Instead, we're generally scanning pages: first trying to determine if the page is relevant to the task at hand, and second to find the specific information within the page.
Therefore, our goals as documentation writers is to make our content as scannable as possible.

Headers help for scanning
-------------------------

Start by using headers liberally.
Headers are sign posts in content, and they're the first things we scan.
The hierarchy of headers also gives readers strong clues about the structure of a document, and can make large topics more approachable.

Short paragraphs are easier to consume
--------------------------------------

When we're scanning a document, the first part of the first sentence of each paragraph is generally what we're look paying attention to.
Therefore, keeping paragraphs shorter provides more surface area for scanning.
Shorter paragraphs also indicate conciseness, which is a great quality in technical writing.

Use lists, diagrams and code samples
------------------------------------

Lists, diagrams, and code samples are excellent ways to help a user engage with your content.
Often we'll look at diagrams and code samples first, and then look to surrounding text for explanation if necessary.

Learn more
==========

- The `Google Developer Style Guide`_ has excellent guidelines for writing clear and concise documentation.
  It's also the basis for Rubin's own :doc:`content style guide <index>`.

- Take a critical look at the documentation for projects and services that you use to learn how their documentation is structured and written.
  Tech companies like `GitHub <https://docs.github.com>`_ invest greatly in their documentation and they're excellent examples to learn from.

- The `Divio documentation system`_ website is the basis for the ideas behind tutorial, how-to guides, conceptual and reference documentation topic types.
  Their website expands on the ideas presented here.

- `Every Page is Page One`_ by Mark Baker is an excellent text on topic-based writing.

- Learn about established topic types for Rubin documentation, such as :ref:`Pipelines documentation topic types <package-topic-types>` and Rubin `templates <https://github.com/lsst/templates>`__.

.. _`Divio Documentation system`: https://documentation.divio.com
.. _`Every Page is Page One`: http://xmlpress.net/publications/eppo/
.. _`Google Developer Style Guide`: https://developers.google.com/style/
