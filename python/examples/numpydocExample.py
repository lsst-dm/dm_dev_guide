#
# This file is part of dm_dev_guide.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Example Python module with Numpydoc-formatted docstrings.

This module demonstrates documentation written according to LSST DM's
guidelines for `Documenting Python APIs with Docstrings`_.

Notes
-----
Docstrings have well-specified sections. This is the Notes section. Permitted
sections are listed in `Numpydoc Sections in Docstrings`_. You can't add
arbitrary sections since they won't be parsed.

Usually we don't write extensive module docstrings. Focus the module docstring
on information that a Stack developer needs to know when working inside that
module. Module *users* typically won't see module docstrings (instead they will
read module documentation topics written in the package's ``doc/`` directory).

.. _`Documenting Python APIs with Docstrings`:
   https://developer.lsst.io/python/numpydoc.html
.. _`Numpydoc Sections in Docstrings`:
   https://developer.lsst.io/python/numpydoc.html#py-docstring-sections
"""

__all__ = ('MODULE_LEVEL_VARIABLE', 'moduleLevelFunction', 'exampleGenerator',
           'ExampleClass', 'ExampleError')

MODULE_LEVEL_VARIABLE = 12345
"""Module level variable documented inline (`int`).

The module variable's type is specified in the short summary, as shown above.
Module variables (constants) can have extended descriptions, like this
paragraph. For a complete list of sections permitted in constant docstrings see
`Documenting Constants and Class Attributes`_.

.. _`Documenting Constants and Class Attributes`:
   https://developer.lsst.io/docs/py_docs.html#py-docstring-attribute-constants-structure
"""


def moduleLevelFunction(param1, *args, param2=None, **kwargs):
    """Test that two parameters are not equal.

    This is an example of a function docstring. Function parameters are
    documented in the ``Parameters`` section. See *Notes* for the format
    specification.

    Parameters
    ----------
    param1 : `int`
        The first parameter. Note how the type is marked up with backticks.
        This marks ``int`` as an API object so that Sphinx will attempt to
        link to its reference documentation. You can do this for custom types
        as well. You'll see an example in the `Returns`_ documentation.
    *args
        Additional positional arguments. If the type is known, it can be
        included like usual. Leave out the type if it is not known.
    param2 : `str`, optional
        Optional arguments (those with defaults) always include the word
        ``optional`` after the type info. See the `Parameters`_ section
        documentation for details.
    **kwargs
        Arbitrary keyword arguments. If you do accept ``**kwargs``, make sure
        you link to documentation that describes what keywords are accepted,
        or list the keyword arguments as a definition list:

        ``key1``:
            Description of ``key1`` (`int`).
        ``key2``
            Description of ``key2`` (`str`).

    Returns
    -------
    success : `bool`
        `True` if successful, `False` otherwise.

        The return type is not optional. The ``Returns`` section may span
        multiple lines and paragraphs. Following lines should be indented to
        match the first line of the description.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

        See the `Returns`_ section documentation for details.

    Raises
    ------
    AttributeError
        Raised if <insert situation>.
    ValueError
        Raised if <insert situation>. See the `Raises`_ section documentation
        for details.

    Notes
    -----
    The Notes section is where you can write about the usage patterns and
    background for the API. The bulk of the conceptual documentation goes
    here, instead of in the extended summary. Save example code for the
    "Examples" section.

    **More about the Parameters section**

    If ``*args`` or ``**kwargs`` are accepted, they should be listed as
    ``*args`` and ``**kwargs``.

    The format for a parameter is::

        name : type
            Description.

            The description may span multiple lines. Following lines
            should be indented to match the first line of the description.

            Multiple paragraphs are supported in parameter descriptions.

    See also
    --------
    exampleGenerator
    ExampleClass

    Examples
    --------
    If possible, include an API usage example using the doctest format:

    >>> moduleLevelFunction('Hello', param2='World')
    True

    See the `Examples`_ section reference for details.

    .. _`Parameters`:
       https://developer.lsst.io/python/numpydoc.html#py-docstring-parameters
    .. _`Returns`:
       https://developer.lsst.io/python/numpydoc.html#py-docstring-returns
    .. _`Raises`:
       https://developer.lsst.io/python/numpydoc.html#py-docstring-raises
    .. _`Examples`:
       https://developer.lsst.io/python/numpydoc.html#py-docstring-examples
    """
    if param1 == param2:
        raise ValueError('param1 may not be equal to param2')
    return True


def exampleGenerator(n):
    """Generate an increasing sequence of numbers from 0 to a given limit.

    Generators have a ``Yields`` section instead of a ``Returns`` section.

    Parameters
    ----------
    n : `int`
        The upper limit of the range to generate, from 0 to ``n`` - 1.

    Yields
    ------
    number : `int`
        The next number in the range of 0 to ``n`` - 1.

    See also
    --------
    moduleLevelFunction

    Examples
    --------
    Examples should be written in doctest format, and should illustrate how to
    use the function:

    >>> print([i for i in example_generator(4)])
    [0, 1, 2, 3]
    """
    for i in range(n):
        yield i


class ExampleClass(object):
    """An example class for demonstrating docstrings for classes, methods, and
    attributes in the Numpydoc format.

    Parameters
    ----------
    param1 : `str`
        Description of ``param1``.
    param2 : `list` of `str`
        Description of ``param2``.
    param3 : `int`, optional
        Description of ``param3``.
    """

    attr1 = None
    """Description of ``attr1`` (`str`).
    """

    attr2 = None
    """Description of ``attr2`` (`list` of `str`).
    """

    attr3 = None
    """Description of ``attr3`` (`int`).
    """

    attr4 = None
    """Description of ``attr4`` (`list` of `str`).
    """

    def __init__(self, param1, param2, param3=None):
        self.attr1 = param1
        self.attr2 = param2
        self.attr3 = param3

        self.attr4 = ['attr4']

    @property
    def readonlyProperty(self):
        """Properties are documented in their getter method (`str`, read-only).
        """
        return 'readonlyProperty'

    @property
    def readwriteProperty(self):
        """Properties with both a getter and setter are documented in their
        getter method (`list` of `str`).

        If the setter method contains notable behavior, it should be mentioned
        here as well.
        """
        return self.attr4

    @readwriteProperty.setter
    def readwriteProperty(self, value):
        self.attr4 = value

    def exampleMethod(self, param1, param2):
        """Test that a situation is true.

        Parameters
        ----------
        param1 : obj
            The first parameter.
        param2 : obj
            The second parameter.

        Returns
        -------
        success : `bool`
            `True` if successful, `False` otherwise.

        Notes
        -----
        Class methods are similar to regular functions. Always use the
        imperative mood when writing the one-sentence summary of a method or
        function.

        Do not include the ``self`` parameter in the ``Parameters`` section.
        """
        return True

    def __special__(self):
        """Documentation for a special method.

        Notes
        -----
        Special members are any methods or attributes that start with and end
        with a double underscore.

        At the moment, special members with docstrings are not published in
        the HTML documentation.

        You can still write docstrings for them, though.
        """
        pass

    def _private(self):
        """By default private members are not included in the HTML docs either.

        Notes
        -----
        Private members are any methods or attributes that start with an
        underscore and are *not* special. By default they are not included in
        the output.

        However, you should still provide docstrings for private members to
        document code for internal developers.
        """
        pass


class ExampleError(Exception):
    """An example exception.

    Parameters
    ----------
    msg : `str`
        Human readable string describing the exception.
    code : `int`, optional
        Numeric error code.

    Notes
    -----
    Exceptions are documented in the same manner as other classes.

    Do not include the ``self`` parameter in the ``Parameters`` section.
    """

    msg = None
    """Human readable string describing the exception (`str`).
    """

    code = None
    """Numeric error code (`int`).
    """

    def __init__(self, msg, code=None):
        self.msg = msg
        self.code = code
