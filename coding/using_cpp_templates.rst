###################
Using C++ Templates
###################

.. _cpp_template_intro:

Introduction
============

The classical use of templates is well illustrated by examples such as vector in the C++ STL.
The entire definition of the template must be available to the compiler in order to handle code that instantiates LSST types such as ``std::vector<DataProperty>``.

The case of many of the LSST framework classes is quite different.
We have a templated class ``Image<typename T>``, but we do not expect users to instantiate a wild and wooly zoo of ``Images``; a type such as ``Image<DataProperty>`` makes no sense (and won't compile).
As a consequence, we can move the definitions of much of the implementation of these classes out of the header files, which produces at least three desirable effects:

- Compile times are shorter.
- Implicit dependencies are (sometimes greatly) reduced, as much less of the supporting structure for the classes is exposed to user code that includes e.g. :file:`lsst/fw/Image.h`.
- Self-contained (even shared) libraries can be built.

For true container classes like the STL that require full definitions, we will still place the definitions in separate files, but these implementation files will be included in the header files.
In the absence of compiler options this leads to code duplication, but we will live with it until the overhead, similar to that of inline functions, proves excessive.

Explicit instantiation
======================

For cases such as ``Image`` we will use explicit instantiation.
A complete example is here, and consists of three source files (:ref:`Foo.h <cpp_template_example_foo_h>`, :ref:`Foo.cc <cpp_template_example_foo_cpp>` and :ref:`main.cc <cpp_template_example_main>`) and an :ref:`SConstruct <cpp_template_example_sconstruct>` file.

:ref:`foo.h <cpp_template_example_foo_h>` looks something like this:

.. literalinclude:: using_cpp_templates_snippets/Foo.h
   :language: cpp
   :lines: 6-17

*See* :ref:`below <cpp_template_example_foo_h>` *for the full source.*

You'll notice that the class is defined, but none of its members are.

In :ref:`main.cc <cpp_template_example_main>`,

.. literalinclude:: using_cpp_templates_snippets/main.cc
   :language: cpp

``Foo``, without any knowledge of its implementation.
This is a *good thing*; but how was it achieved? Look at :ref:`Foo.cc <cpp_template_example_foo_cpp>`:

.. literalinclude:: using_cpp_templates_snippets/Foo.cc
   :language: cpp
   :lines: 4-12,14,16-18,24

Here are the missing method definitions, along with the lines

.. literalinclude:: using_cpp_templates_snippets/Foo.cc
   :language: cpp
   :lines: 28-29

which tell the compiler to generate the classes ``Foo<float>`` and ``Foo<int>``; exactly the classes that :ref:`main.cc <cpp_template_example_main>` uses.

More explicit instantiation
---------------------------

If you look at :ref:`Foo.h <cpp_template_example_foo_h>` you'll see that there's more code than discussed above.
The main features are that an inline member of ``Foo`` needs to be fully specified in :ref:`Foo.h <cpp_template_example_foo_h>` (how else could the compiler inline it?), and also an example of explicit instantiation of a function, rather than a class.
There should be no surprises.

What about `extern template` and `-no-implicit-templates`?
==========================================================

These code examples didn't use either ``extern template`` or ``-no-implicit-templates``; why not?

The former, ``extern template`` is not (yet) in the C++ standard (but see C++ proposal N1987), while the latter is a :command:`g++` command line flag.
What would we gain by using them?

The example C++ in the previous section didn't give the compiler a choice; even if it wanted to instantiate ``Foo<int>`` in  :ref:`main.cc <cpp_template_example_main>` it simply didn't know enough. 
However, if we'd included the full template implementation in :ref:`Foo.h <cpp_template_example_foo_h>`, matters would have been different; exactly what happens isn't specified by the C++ standard as you cannot tell what the compiler decided, but many compilers (including :command:`g++`) generate a definition of the class and its members in each object file, and then use the linker to remove duplicates.

It is this behavior that is modified by ``extern template`` and ``-no-implicit-templates``; they instruct the compiler not to instantiate ``Foo<int>`` even if it could.

How do I know what it did?
Well, the most direct way (on a command line) is to say:

.. code-block:: bash

   nm main.o | c++filt | grep 'Foo(float)'

which results in:

.. code-block:: cpp

   U Foo<float>::Foo(float)

That is, the constructor ``Foo<float>::Foo`` isn't defined in :ref:`main.cc <cpp_template_example_main>`.

If you move the definition of the constructor from :ref:`Foo.cc <cpp_template_example_foo_cpp>` to  :ref:`Foo.h <cpp_template_example_foo_h>` and repeat the experiment, you'll get:

.. code-block:: cpp

   W Foo<float>::Foo(float)

unless you add an ``extern template Foo<float>`` or compile with ``-no-implicit-templates``.

Legalities
==========

Careful reading of Stroustrup implies that this technique is legal.

The relevant passage is Section 13.7 (p. 351), which is talking about the use of the ``export`` keyword.
We're not using ``export``, but the compiler doesn't know that when it compiles :file:`out.h`:

.. FIXME migrate page on export? https://dev.lsstcorp.org/trac/wiki/WhyNotExport

.. code-block:: cpp

   // out.h:
   template <class T> void out(const T& t);

   // user1.c:
   #include "out.h"
   // use out() 

.. _cpp_template_example:

Template usage example
======================

.. _cpp_template_example_sconstruct:

Sconstruct
----------

.. literalinclude:: using_cpp_templates_snippets/Sconstruct
   :language: python

.. _cpp_template_example_foo_h:

Foo.h
-----

.. literalinclude:: using_cpp_templates_snippets/Foo.h
   :language: cpp

.. _cpp_template_example_foo_cpp:

Foo.cc
------

.. literalinclude:: using_cpp_templates_snippets/Foo.cc
   :language: cpp

.. _cpp_template_example_main:

main.cc
-------

.. literalinclude:: using_cpp_templates_snippets/main.cc
   :language: cpp
