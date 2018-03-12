###########
Using Boost
###########

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these policies, please file an :doc:`RFC </communications/rfc>`.


.. _cpp_using_boost:

A Boost library may be used only if:

1. the desired effect cannot be accomplished with a C++14 standard language feature, and
2. a C++ standard library equivalent is either unavailable or unusable with our minimum required compiler version (i.e. ``gcc`` version 6.3.1).

In particular, the following Boost libraries are no longer accepted as they have standard equivalents in gcc 6.3.1 and above:

``array``
        use ``<array>``

``bind``
        prefer C++14 lambda functions instead, but use ``std::bind`` from ``<functional>`` if you must

``cstdint``
        use ``<cstdint>``

``filesystem``
        use ``<filesystem>``

``lambda``
        use C++14 lambda functions

``lexical_cast``
        use ``std::to_string``, ``std::stoi``, ``std::stod`` etc.

``math``
        use ``<cmath>`` wherever possible

``noncopyable``
        use ``= delete`` on the copy constructor and assignment operator

``random``
        use ``<random>``

``ref``
        use ``std::forward`` and universal / forwarding references (or ``std::ref`` if you must)

``smart_ptr``
        use ``std::shared_ptr`` and ``std::unique_ptr`` (and its array specialization) from ``<memory>`` instead of ``boost::shared_ptr``, ``boost::scoped_ptr`` and ``boost::scoped_array``

``static_assert``
        use C++14 ``static_assert``

``tuple``
        use ``<tuple>``

``type_traits``
        use ``<type_traits>``

``unordered_map``
        use ``<unordered_map>``

Certain Boost libraries are recommended: they should be used whenever applicable in preference to any other method of accomplishing the same effect. In general, any library that is tagged with *"Standard .... {something}"* in the `Boost library listing <http://www.boost.org/doc/libs>`_ falls into this category (unless its use conflicts with the above rules on the availability of standard library / language equivalents).
Among others, this category includes:

* ``current_function``
* ``format``
* ``regex``
* ``test``

Additional Boost libraries are considered safe: they may be used freely where applicable.

* ``any``
* ``GIL``
* ``iterator``
* ``MPI``
* ``multi_index``
* ``numeric``
* ``tokenizer``
* ``variant``

Most other Boost libraries may be used after appropriate design review.
Particular caution should be used when the library involves substantial template metaprogramming or requires linking (is not listed on the above page as *"Build & Link .... Header-only"*).
Among others, the following libraries fall into the extra-caution category:

* ``Fusion``
* ``MPL``
* ``serialization``

Certain Boost libraries conflict with LSST-standard ways of doing things, are inappropriate for LSST code, are insufficiently developed or well-maintained, or have been found to be excessively complicated.
These are not allowed without special permission.

* ``config``
* ``preprocessor``
* ``python``
* ``throw_exception``
