.. _user-doc-style-lsst:

#########################
LSST-specific style guide
#########################

The :doc:`LSST user documentation style guide </user-docs/index>` is built upon the `Google Developer Style Guide`_.
This page lists our exceptions and modifications to those guidelines.

Use the imperative mood for Python and C++ function and method summary sentences
--------------------------------------------------------------------------------

For LSST DM Python and C++, you should use the **imperative mood** to write the summary sentence:

   Get the value.

The imperative mood is conventional in scientific Python software (Numpy, SciPy, and Astropy, among others).
In turn, our C++ standard follows the Python convention since our use of the two languages is often intertwined.
See also:

- :ref:`Python summary sentence standard <py-docstring-short-summary>`
- :ref:`C++ summary sentence standard <cpp-doxygen-short-summary>`

.. note::

   This recommendation for LSST DM differs from the Google Developer Style Guide, which recommends `using the present tense for function and method summaries <https://developers.google.com/style/api-reference-comments#methods>`__.
   For example:

       Gets the value.

   If you are documenting a completely different technology, such as HTTP API endpoints, using the present tense is a good idea.

.. _`Google Developer Style Guide`: https://developers.google.com/style/
