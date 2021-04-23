###########
Using Boost
###########

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these policies, please file an :doc:`RFC </communications/rfc>`.


.. _cpp_using_boost:

A Boost library may be used only if:

1. the desired effect cannot be accomplished with a C++17 standard language feature, and
2. a C++ standard library equivalent is either unavailable or unusable with our :ref:`minimum required compiler version <style-guide-cpp-2-2>`.

In particular, the following Boost libraries are no longer accepted as they have standard equivalents in gcc 6.3.1 and above:

``any``
        use ``<any>``

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

``variant``
        use ``<variant>``

Certain Boost libraries are recommended: they should be used whenever applicable in preference to any other method of accomplishing the same effect.
Among others, this category includes:

* ``current_function``
* ``format``
* ``test``

Additional Boost libraries are considered safe: they may be used freely where applicable.

* ``GIL``
* ``iterator``
* ``MPI``
* ``multi_index``
* ``numeric``
* ``tokenizer``

Most other Boost libraries may be used after appropriate design review.
Particular caution should be used when the library involves substantial template metaprogramming or requires linking.
Among others, the following libraries fall into the extra-caution category:

* ``Fusion``
* ``MPL``
* ``regex``
* ``serialization``

Certain Boost libraries conflict with LSST-standard ways of doing things, are inappropriate for LSST code, are insufficiently developed or well-maintained, or have been found to be excessively complicated.
These are not allowed without special permission.

* ``config``
* ``preprocessor``
* ``python``
* ``throw_exception``
