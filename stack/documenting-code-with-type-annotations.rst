.. _stack-documentation-code-with-type-annotations:

################################
Documenting code with type hints
################################

Many DM packages (especially the middleware suite) use type hints for static analysis, which often duplicates the type information included in docstrings.
Documentation built with `Documenteer 2.x`_ can often leave this information out, because the `sphinx-autodoc-typehints`_ extension (included automatically) will parse the annotations and include type information in the docs automatically.

.. note::
   `pipelines.lsst.io`_ is currently still built with Documenteer 1.x, but is expected to transition soon.
   While some :ref:`package doc builds <build-package-docs>` have already been upgraded in anticipation of this transition, their documentation content needs to remain compatible with Documenteer 1.x for now.

Function arguments
------------------

To document the parameters to a function or method declared with type hints,
use regular numpydoc style without the colon or the type information that follows it::

   def run_thing(self, x: int, *args: int, name: str = "", **kwargs: str) -> None:
       """Run the thing.

       Parameters
       ----------
       x
           X coordinate.
       *args
           Some other coordinates.
       name
           The name of the thing.
       **kwargs
           Names of other things.
       """

Note that ``, optional`` is also unnecessary, as are defaults; default values are automatically pulled from the real function signature.

Function return values
----------------------

Return types work automatically when they are not documented at all::

   def return_it() -> str:
       """Return the thing."""
       return ""

This is a reasonable approach when there is nothing else to document about the returned object.
When the returned object does merit additional documentation, the type does unfortunately need to be written out (duplicating the annotation), but the returned object should not be named::

   def return_it() -> str:
       """Return the thing.

       Returns
       -------
       str
           The thing.
       """
       return ""

A simple return type does not need backticks to create a link, but backticks may be needed for more complex types (e.g. generics)::

   from collections.abc import Sequence

   def return_stuff() -> Sequence[str]:
       """Return some stuff.

       Returns
       -------
       `~collections.abc.Sequence` [`str`]
           The stuff.
       """
       return []

.. note::
   As always, types in docstrings do *not* respect imports in the file, and instead are resolved using the `Sphinx target-resolution rules`_.
   See :ref:`rst-python-link` for details.

Functions that return multiple values via a tuple should just have multiple
entries::

   def return_pair() -> tuple[str, int]:
       """Return a pair.

       Returns
       -------
       str
           The name.
       int
           The ID.
       """
       return ("", 0)

Properties and attributes
-------------------------

Annotations on properties and attributes are not applied to documentation automatically.
Their docstrings should continue to include the types parenthetically::

   class Thing:
       """A thing."""

       @property
       def name(self) -> str:
           """Name of the thing (`str`)."""
           return ""

       value: int = 0
       """Value of the thing (`int`)."""

.. note::
   Attributes without default values (or some sort of ``= RHS``) are not
   included in documentation *at all*, except for those on `~dataclasses.dataclass` types.
   Important instance attributes that cannot have a class-level default value should be made into properties so they can be documented.


.. _`Documenteer 2.x`: https://documenteer.lsst.io
.. _`sphinx-autodoc-typehints`: https://pypi.org/project/sphinx-autodoc-typehints/
.. _`pipelines.lsst.io`: https://pipelines.lsst.io
.. _`Sphinx target-resolution rules`: <https://www.sphinx-doc.org/en/master/usage/domains/python.html#target-resolution>`
