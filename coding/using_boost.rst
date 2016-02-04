###########
Using Boost
###########

.. _cpp_using_boost:

Certain Boost libraries are recommended; they should be used whenever applicable in preference to any other method of accomplishing the same effect. In general, any library that is tagged with *"Standard .... {something}"* in the `Boost library listing <http://www.boost.org/doc/libs>`_ falls into this category, unless the feature is already supported by the currently-mandated LSST ``g++`` version.
Among others, this category includes:

* ``current_function``
* ``format``
* ``regex`` (until we adopt ``gcc`` 4.9 as our minimum compiler version, at which point use ``std::regex``)
* ``test``

Libraries that were accepted before we switched to C++11 (in particular made ``gcc`` 4.8 our minimum supported compiler), but have been or are being replaced by ``std::`` equivalents include:

* ``array``: use ``std::array`` from ``<array>``
* ``cstdint``: use ``<cstdint>``
* ``filesystem``: use ``<filesystem>``
* ``noncopyable``: use ``= delete`` on the copy constructor and assignment operator
* ``smart_ptr``: use ``std::shared_ptr`` and ``std::unique_ptr`` from ``<memory>`` instead of ``boost::shared_ptr`` and ``boost::scoped_ptr``
* ``static_assert``: use ``static_assert``
* ``type_traits``: use ``<type_traits>``
* ``unordered_map``: use ``std::unordered_map`` from ``<unordered_map>``

Additional Boost libraries are considered safe; they may be used freely where applicable.

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
