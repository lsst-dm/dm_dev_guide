#####################################
Python wrappers for C++ with pybind11
#####################################

We use the `pybind11 <https://github.com/pybind/pybind11>`_ library to generate Python wrappers for our C++ code.
These wrappers are subject to the rules laid out in the :doc:`style`.

What follows is a basic step-by-step guide to writing pybind11 wrappers.

It attempts to cover the most frequently encountered patterns in LSST code.
But it is not intended to be a full tutorial on pybind11.
For far more detailed information please see the `pybind11 documentation <http://pybind11.readthedocs.io>`_.

.. _wrapping:

Wrapping step-by-step
=====================

To illustrate how wrapping is done we will recreate the example wrappers from the `pybind11_example`_ repository.

.. _wrapping-simple-class:

Wrapping a simple class
-----------------------

We start by wrapping the basic `ExampleOne class in pybind11_example`_.
Its header file looks like:

.. code-block:: cpp

    #ifndef LSST_TMPL_EXAMPLEONE_H
    #define LSST_TMPL_EXAMPLEONE_H

    #include <ostream>
    #include <string>
    #include <vector>

    #include "ndarray.h"

    namespace lsst {
    namespace tmpl {

    class ExampleOne {
    public:
        enum State { RED = 0, ORANGE, GREEN };

        static constexpr int someImportantConstant = 10;  ///< Important constant

        /**
         * Default constructor: default construct an ExampleOne
         */
        explicit ExampleOne() : _state(RED), _value(someImportantConstant) {}

        /**
         * Construct an ExampleOne from a filename and a state
         *
         * @param[in] fileName  name of file;
         * @param[in] state  initial state (RED, ORANGE or GREEN, default RED).
         */
        explicit ExampleOne(std::string const& fileName, State state = RED);

        /**
         * Copy constructor
         *
         * @param[in] other  the other object
         * @param[in] deep  make a deep copy
         */
        ExampleOne(ExampleOne const& other, bool deep = true);

        /**
         * Get state
         *
         * @return current state (RED, ORANGE or GREEN, default RED).
         */
        State getState() const { return _state; }

        /**
         * Set state
         *
         * @param[in] state  state
         * @param[in] state  initial state (RED, ORANGE or GREEN, default RED).
         */
        void setState(State state) { _state = state; }

        /**
         * Compute something
         *
         * @param[in] myParam some parameter
         * @return a particular value
         */
        double computeSomething(int myParam) const;

        /**
         * Compute something else
         *
         * @param[in] myFirstParam some parameter
         * @param[in] mySecondParam some other parameter
         * @return a particular value
         */
        double computeSomethingElse(int myFirstParam, double mySecondParam) const;

        /**
         * Compute something else
         *
         * @param[in] myFirstParam some parameter
         * @param[in] anotherParam some other parameter
         * @return a particular value
         */
        double computeSomethingElse(int myFirstParam, std::string anotherParam = "foo") const;

        /**
         * Compute some vector
         *
         * @return a vector with results
         */
        std::vector<int> computeSomeVector() const;

        /**
         * Do something with an input array
         *
         * @return some result
         */
        void doSomethingWithArray(ndarray::Array<int, 2, 2> const& arrayArgument);

        /**
         * Initialize something with some value
         *
         * @param someValue some value to do something with
         */
        static void initializeSomething(std::string const& someValue);

        bool operator==(ExampleOne const& other) { return _value == other._value; }
        bool operator!=(ExampleOne const& other) { return _value != other._value; }

        ExampleOne& operator+=(ExampleOne const& other) {
            _value += other._value;
            return *this;
        }

        friend std::ostream& operator<<(std::ostream&, ExampleOne const&);

    private:
        State _state;  ///< Current state
        int _value;    ///< Some value
    };

    ExampleOne operator+(ExampleOne lhs, ExampleOne const& rhs) {
        lhs += rhs;
        return lhs;
    }

    std::ostream& operator<<(std::ostream& out, ExampleOne const& rhs) {
        out << "Example(" << rhs._value << ")";
        return out;
    }

    }}  // namespace lsst::tmpl

    #endif

.. _adding-dependencies:

Adding dependencies
^^^^^^^^^^^^^^^^^^^

First we need to add some dependencies to the build.

Scons will not use pybind11 unless it is setup, so in ``{{pkg}}/ups/{{pkg}}.table``,
where ``{{pkg}}`` is the name of the package, you will need to add the dependency ``setupRequired(pybind11)``.
You also need to modify the ``dependencies`` in ``{{pkg}}/ups/{{pkg}}.cfg``, by adding ``"pybind11"`` to ``"buildRequired"``.

.. _creating-module-file:

Creating module files
^^^^^^^^^^^^^^^^^^^^^

Following :ref:`our rules on file naming <style-guide-pybind11-module-naming>`, we start by creating a minimal module file ``python/lsst/tmpl/_tmpl.cc`` with the following content:

.. code-block:: cpp

    #include "pybind11/pybind11.h"

    #include "lsst/utils.python.h"

    namespace lsst {
    namespace tmpl {

    void wrapExampleOne(utils::python::WrapperCollection & wrappers);

    PYBIND11_MODULE(_tmpl, mod) {
        utils::python::WrapperCollection wrappers(mod, "lsst.tmpl");
        wrapExampleOne(wrappers);
        wrappers.finish();
    }

    }}  // lsst::tmpl

.. warning::

    The name used for the ``PYBIND11_MODULE(..., mod)`` macro must match the name of the file, otherwise an ``ImportError`` will be raised.

``WrapperCollection`` is a helper class provided by the LSST ``utils`` package that should be used in essentially all LSST pybind11 wrappers (the only exception being packages that have a good reason not to have a dependency on ``utils``).
It makes it easier to avoid dependency problems when wrapping multiple interrelated classes.
It also makes wrapped classes appear as if they were defined directly in the higher-level Python package (``lsst.tmpl`` here) rather than a hidden nested module like ``lsst.tmpl._tmpl``, which should be considered an implementation detail.
``WrapperCollection`` instances should always be passed by non-const reference.

Modules should have exactly one source file with a ``PYBIND11_MODULE`` block, and usually that block should delegate the real work to functions defined in other source files (generally one for each C++ header to be wrapped).

.. note::

    An older version of this tutorial advocated compiling each source file as a separate module, which makes it impossible to correctly handle circular dependencies, and generally leads to larger-than-necessary binary module sizes.

The source file that will actually contain the wrappers for ``ExampleOne.h`` will start out looking like this:

.. code-block:: cpp

    // _ExampleOne.cc

    #include "pybind11/pybind11.h"

    #include "lsst/utils/python.h"
    #include "lsst/tmpl/ExampleOne.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst { namespace tmpl {

    void wrapExampleOne(utils::python::WrapperCollection & wrappers) {
        // ... wrappers for ExampleOne go here ...
    }

    }}  // lsst::tmpl

Because it's only called in one place (the ``PYBIND11_MODULE`` block), we didn't create a header for the declaration of ``wrapExampleOne``.
That means we need to make sure the names and signatures exactly match, because errors will only be caught by the linker (not the compiler), and linker error messages can be quite cryptic.

Tiny packages that provide just one header can be wrapped by putting all of the wrapper code directly in the ``PYBIND11_MODULE`` block, but before taking that approach it's worth considering whether the package may gain additional headers in the future.


Wrapping the class
^^^^^^^^^^^^^^^^^^

We wrap the class using the ``py::class_<T>`` template:

.. code-block:: cpp

    void wrapExampleOne(utils::python::WrapperCollection & wrappers) {
        wrappers.wrapType(
            py::class_<ExampleOne, std::shared_ptr<ExampleOne>>(wrappers.module, "ExampleOne"),
            [](auto & mod, auto & cls) {
                // method and other attribute wrappers go here
            }
        );
    }

.. note::

    As in the example, classes should almost always have a :ref:`shared_ptr holder type <style-guide-pybind11-holder-type>`.

``WrapperCollection`` will automatically call the callback given as the second argument with the module and the ``pybind11::class_`` object passed as the first argument, but not until all other classes defined in the module have been declared.
That ensures all types are known to pybind11 before any signatures are declared, which in turn ensures pybind11 can generate the right type conversions when wrapping those signatures.

Usually the wrappers for a class can be defined entirely within the callback function, but ``wrapType`` also returns the ``class_`` object in case it's needed elsewhere.
All of the examples in the next few sections that operate on a ``cls`` object can go inside the callback.

Wrapping constructors
^^^^^^^^^^^^^^^^^^^^^

Constructors are added to the class using the ``py::init<T...>`` helper:

.. code-block:: cpp

    cls.def(py::init<>());
    cls.def(py::init<std::string const&, ExampleOne::State>());
    cls.def(py::init<ExampleOne const&, bool>()); // Copy constructor

However, two of the constructors have default arguments. So we use the argument literal from ``pybind::literals`` to wrap them as keyword arguments (which following the rule on :ref:`keyword arguments <style-guide-pybind11-keyword-arguments>` should almost always be done, except for non-overloaded functions taking a single argument):

.. code-block:: cpp

    cls.def(py::init<>());
    cls.def(py::init<std::string const&, ExampleOne::State>(), "fileName"_a, "state"_a=ExampleOne::State::RED);
    cls.def(py::init<ExampleOne const&, bool>(), "other"_a, "deep"_a=true); // Copy constructor

We also need to add: ``using namespace pybind11::literals;`` at the top.

.. warning::

    Unfortunately there is no way for pybind11 to track the value of the default argument.
    So be careful to duplicate it correctly, and update it when it is changed in the C++ interface.

Getters and setters
^^^^^^^^^^^^^^^^^^^

We can wrap ``getState`` and ``setState`` as follows:

.. code-block:: cpp

    cls.def("getState", &ExampleOne::getState);
    cls.def("setState", &ExampleOne::setState);

Following the :ref:`rules on properties <style-guide-pybind11-properties>` you may choose to add a property too:

.. code-block:: cpp

    cls.def_property("state", &ExampleOne::getState, &ExampleOne::setState);

Wrapping (overloaded) member functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wrapping a member function is easy:

.. code-block:: cpp

    cls.def("computeSomething", &ExampleOne::computeSomething);

However, when the function is overloaded we need to disambiguate the overloads.
Following the rule on :ref:`overload disambiguation <style-guide-pybind11-overload-disambiguation>` we use ``overload_cast`` for for this:

.. code-block:: cpp

    cls.def("computeSomethingElse",
            py::overload_cast<int, double>(&ExampleOne::computeSomethingElse, py::const_),
            "myFirstParam"_a, "mySecondParam"_a);
    cls.def("computeSomethingElse",
            py::overload_cast<int, std::string>(&ExampleOne::computeSomethingElse, py::const_),
            "myFirstParam"_a, "anotherParam"_a="foo");

Note that ``py::const_`` is necessary for a const member function.

STL containers
^^^^^^^^^^^^^^

The function ``ExampleOne::computeSomeVector`` returns a ``std::vector<int>``.
Following the :ref:`rule on STL containers <style-guide-pybind11-stl-containers>` we simply include the ``pybind11/stl.h`` header (to enable automatic conversion to and from Python containers) and wrap the function as normal:

.. code-block:: cpp

    cls.def("computeSomeVector", &ExampleOne::computeSomeVector);

.. note::

    The converters defined in ``pybind11/stl.h`` do a complete conversion from a C++ container to a Python container (e.g. ``std::vector`` to ``list``).
    Unless the values of the container are smart pointers, that will involve a deep copy of the entire container.

Ndarray
^^^^^^^

The function ``ExampleOne::doSomethingWithArray`` takes an ``ndarray::Array`` argument.
To enable automatic conversion to and from ``numpy.ndarray`` in Python add the following include (right below the pybind11 ones):

.. code-block:: cpp

    #include "ndarray/pybind11.h"

Then the function can be wrapped as normal:

.. code-block:: cpp

    cls.def("doSomethingWithArray", &ExampleOne::doSomethingWithArray);

.. note::

    If your wrapper needs to convert Eigen objects, include ``pybind11/eigen.h``.
    Previous versions of the ndarray library included automatic conversion for Eigen objects,
    but that code has been removed and we now rely on pybind11's standard support for Eigen.

.. note::

    Previous versions of the ndarray library also required ``numpy/arrayobject.h`` to be included, as well as a call to ``_import_array()`` in the module initialization function.
    As of ndarray 1.4.0, these steps are no longer necessary, but they will not yield incorrect behavior or errors (though they will generate warnings and slightly bloated code).

Static member functions
^^^^^^^^^^^^^^^^^^^^^^^

Wrapping *static* member functions is trivial:

.. code-block:: cpp

    cls.def_static("initializeSomething", &ExampleOne::initializeSomething);

Wrapping operators
^^^^^^^^^^^^^^^^^^

According to our :ref:`rule on operators <style-guide-pybind11-operator>` we can either wrap operators directly, or use a lambda.
Here we use both approaches:

.. code-block:: cpp

    cls.def("__eq__", &ExampleOne::operator==, py::is_operator());
    cls.def("__ne__", &ExampleOne::operator!=, py::is_operator());
    cls.def("__iadd__", &ExampleOne::operator+= /* no py::is_operator() here */);
    cls.def("__add__", [](ExampleOne const & self, ExampleOne const & other) { return self + other; }, py::is_operator());

.. note::

    * We use ``py::is_operator()`` to return ``NotImplemented`` on failure.
    * We don't use ``py::is_operator()`` for in-place operators as this can lead to confusing behavior.
    * We name the lambda arguments :ref:`self <style-guide-pybind11-lambda-self-argument>` and :ref:`other <style-guide-pybind11-lambda-other-argument>`.

Module-Level Declaration
^^^^^^^^^^^^^^^^^^^^^^^^

Module-level free functions and variables can be declared inside a ``wrapType`` callback, and you should do so when they're closely related to the class it defines.

In other cases, you can add a callback not associated with any class by calling the ``wrap`` method instead:

.. code-block:: cpp

    wrappers.wrap(
        [](auto & mod) {
            // any number of module-level wrappers go here
        }
    );

.. note::

    We do not attempt to update the ``__module__`` attribute of free functions, as these are rarely used.
    Free functions that are used by ``__reduce__`` to reconstruct pickled objects should have their ``__module__`` updated manually to avoid making serialized forms unnecessarily dependent on how our Python modules are structured.

Custom exceptions
^^^^^^^^^^^^^^^^^

The example contains a custom exception (``ExampleError``) added by the ``LSST_EXCEPTION_TYPE`` macro:

.. code-block:: cpp

    LSST_EXCEPTION_TYPE(ExampleError, lsst::pex::exceptions::RuntimeError, ExampleError)

To wrap it we can use the ``wrapException`` method:

.. code-block:: cpp

    wrappers.wrapException<ExampleError, pex::exceptions::RuntimeError>("ExampleError", "RuntimeError");

Note that this involves creating a subclass of ``RuntimeError``, which is wrapped in the ``lsst.pex.exceptions`` module.
We'll need to import that module *before* calling ``wrapException``.
As we'll discuss in more detail in :ref:`pybind11-cross-module-dependencies`, this is best handled via a line like:

.. code-block:: cpp

    wrappers.addSignatureDependency("lsst.pex.exceptions");


Wrapping enums and nested types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``wrapType`` should be used for enums as well as classes, as enums are also types and hence should be declared before any signatures are wrapped.

Because the enum in our example is defined in a class scope, we'll need to capture the return value of the ``wrapType`` call for ``ExampleOne`` so we can use it to define the enum:

.. code-block:: cpp

    auto clsExampleOne = wrappers.wrapType(
        py::class_<ExampleOne, std::shared_ptr<ExampleOne>>(wrappers.module, "ExampleOne"),
        [](auto & mod, auto & cls) {
            // ... wrappers for ExampleOne ...
        }
    );

    wrappers.wrapType(
        py::enum_<ExampleOne::State>(clsExampleOne, "State"),
        [](auto & mod, auto & enm) {
            enm.value("RED", ExampleOne::State::RED);
            enm.value("ORANGE", ExampleOne::State::ORANGE);
            enm.value("GREEN", ExampleOne::State::GREEN);
        }
    );

.. note::

    We attach the ``enum`` values to the class (by passing the ``py::class_`` object ``clsExampleOne`` as the first argument)

.. note::

    Add ``.export_values()`` if (and only if) you need to export the values into the class scope (so they can be reached as ``ExampleOne.RED``, in addition to ``ExampleOne.State.RED``).

    Never do this for C++11 scoped ``enum class`` types, since that will give them different symantics in C++ and Python.


Finished wrapper
^^^^^^^^^^^^^^^^

The end result of all the steps above looks like this:

.. code-block:: cpp

    #include "pybind11/pybind11.h"
    #include "pybind11/stl.h"
    #include "ndarray/pybind11.h"

    #include "lsst/utils/python.h"
    #include "lsst/tmpl/ExampleOne.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst { namespace tmpl {

    void wrapExampleOne(utils::python::WrapperCollection & wrappers) {

        wrappers.addInheritanceDependency("lsst.pex.exceptions");

        wrappers.wrapException<ExampleError, pex::exceptions::RuntimeError>("ExampleError", "RuntimeError");

        auto clsExampleOne = wrappers.wrapType(
            py::class_<ExampleOne, std::shared_ptr<ExampleOne>>(wrappers.module, "ExampleOne"),
            [](auto & mod, auto & cls) {
                cls.def(py::init<>());
                cls.def(py::init<std::string const&, ExampleOne::State>(),
                        "fileName"_a, "state"_a=ExampleOne::State::RED);
                cls.def(py::init<ExampleOne const&, bool>(), "other"_a, "deep"_a=true); // Copy constructor
                cls.def("getState", &ExampleOne::getState);
                cls.def("setState", &ExampleOne::setState);
                cls.def_property("state", &ExampleOne::getState, &ExampleOne::setState);
                cls.def("computeSomething", &ExampleOne::computeSomething);
                cls.def("computeSomethingElse",
                        py::overload_cast<int, double>(&ExampleOne::computeSomethingElse, py::const_),
                        "myFirstParam"_a, "mySecondParam"_a);
                cls.def("computeSomethingElse",
                        py::overload_cast<int, std::string>(&ExampleOne::computeSomethingElse, py::const_),
                        "myFirstParam"_a, "anotherParam"_a="foo");
                cls.def("computeSomeVector", &ExampleOne::computeSomeVector);
                cls.def("doSomethingWithArray", &ExampleOne::doSomethingWithArray);
                cls.def_static("initializeSomething", &ExampleOne::initializeSomething);
                cls.def("__eq__", &ExampleOne::operator==, py::is_operator());
                cls.def("__ne__", &ExampleOne::operator!=, py::is_operator());
                cls.def("__iadd__", &ExampleOne::operator+=);
                cls.def("__add__",
                        [](ExampleOne const & self, ExampleOne const & other) {
                            return self + other;
                        },
                        py::is_operator());
            }
        );

        wrappers.wrapType(
            py::enum_<ExampleOne::State>(clsExampleOne, "State"),
            [](auto & mod, auto & enm) {
                enm.value("RED", ExampleOne::State::RED);
                enm.value("ORANGE", ExampleOne::State::ORANGE);
                enm.value("GREEN", ExampleOne::State::GREEN);
                enm.export_values();
            }
        );

    }

    }}  // namespace lsst::tmpl


Building the wrapper
--------------------

The next step is to tell SCons to build your wrapper.
Edit ``python/.../SConscript`` to look like this:

.. code-block:: python

    # -*- python -*-
    from lsst.sconsUtils import scripts
    scripts.BasicSConscript.python()


Importing the wrapper
---------------------

The Python name for your wrapper module is `exampleOne`.
If the wrapped classes can be returned by a function or unpickled then it is crucial that your module is imported when the package is imported.
If the symbols are part of the public API then this is typically done by adding the following to your package's main ``__init__.py`` file:

.. code-block:: python

    from ._tmpl import *

.. note::

    One or more ``__init__.py`` files with imports like this *must* be used to make sure all wrapped types are actually available from the package used to construct the ``WrapperCollection``.


Advanced Wrappers
=================

In this section we are going to look at some more advanced wrapping.
In particular inheritance and templates
We shall also cover how to add pure Python members to wrapped C++ classes.

We wrap the following two header files from the ``templates`` package, ``ExampleTwo.h``:

.. code-block:: cpp

    #ifndef LSST_TMPL_EXAMPLETWO_H
    #define LSST_TMPL_EXAMPLETWO_H

    namespace lsst { namespace tmpl {

    class ExampleBase {
    public:
        virtual int someMethod(int value) { return value + 1; }

        virtual double someOtherMethod() = 0;

        virtual ~ExampleBase() = default;
    };

    class ExampleTwo : public ExampleBase {
    public:
        ExampleTwo() = default;

        double someOtherMethod() override {
            return 4.0;
        }
    };

    }}  // namespace lsst::tmpl

    #endif

and ``ExampleThree.h``:

.. code-block:: cpp

    #ifndef LSST_TMPL_EXAMPLETHREE_H
    #define LSST_TMPL_EXAMPLETHREE_H

    #include "lsst/tmpl/ExampleTwo.h"

    namespace lsst { namespace tmpl {

    template <typename T>
    class ExampleThree : public ExampleBase {
    public:
        ExampleThree(T value) : _value(value) { }

        double someOtherMethod() override {
            return static_cast<double>(_value);
        }
    private:
        T _value;
    };

    }}  // namespace lsst::tmpl

    #endif

More wrapper files
------------------

Because code in different headers should usually be wrapped in different source files, we'll create two new skeletons for ``ExampleTwo.h`` and ``ExampleThree.h``:

.. code-block:: cpp

    // _ExampleTwo.cc

    #include "pybind11/pybind11.h"

    #include "lsst/utils/python.h"
    #include "lsst/tmpl/ExampleTwo.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst { namespace tmpl {

    void wrapExampleTwo(utils::python::WrapperCollection & wrappers) {
        // ... wrappers for ExampleTwo go here ...
    }

    }}  // lsst::tmpl

.. code-block:: cpp

    // _ExampleThree.cc

    #include "pybind11/pybind11.h"

    #include "lsst/utils/python.h"
    #include "lsst/tmpl/ExampleThree.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst { namespace tmpl {

    void wrapExampleThree(utils::python::WrapperCollection & wrappers) {
        // ... wrappers for ExampleThree go here ...
    }

    }}  // lsst::tmpl


Our main source file should then be updated to declare and call all of the ``wrap*`` functions:

.. code-block:: cpp

    // _tmpl.cc

    #include "pybind11/pybind11.h"

    #include "lsst/utils/python.h"

    namespace lsst { namespace tmpl {

    void wrapExampleOne(utils::python::WrapperCollection & wrappers);
    void wrapExampleTwo(utils::python::WrapperCollection & wrappers);
    void wrapExampleThree(utils::python::WrapperCollection & wrappers);

    PYBIND11_MODULE(_tmpl, mod) {
        utils::python::WrapperCollection wrappers(mod, "lsst.tmpl");
        wrapExampleOne(wrappers);
        wrapExampleTwo(wrappers);
        wrapExampleThree(wrappers);
        wrappers.finish();
    }

    }} // lsst::tmpl

.. note::

    If any of this looks unfamiliar please see :ref:`"Wrapping a simple class" <wrapping-simple-class>` first.

Inheritance
-----------

``ExampleTwo.h`` defines two classes (``ExampleBase`` and ``ExampleTwo``) which we wrap as follows:

.. code-block:: cpp

    wrappers.wrapType(
        py::class_<ExampleBase, std::shared_ptr<ExampleBase>>(wrappers.module, "ExampleBase"),
        [](auto & mod, auto & cls) {
            cls.def("someMethod", &ExampleBase::someMethod);
        }
    );

    wrappers.wrapType(
        py::class_<ExampleTwo, std::shared_ptr<ExampleTwo>, ExampleBase>(wrappers.module, "ExampleTwo"),
        [](auto & mod, auto & cls) {
            cls.def(py::init<>());
            cls.def("someOtherMethod", &ExampleTwo::someOtherMethod);
        }
    );

There are two subtleties:

* ``ExampleTwo`` inherits from ``ExampleBase``.
* To indicate this we list ``ExampleBase`` as a template parameter when declaring ``clsExampleTwo``.
* If ``ExampleTwo`` had additional base classes they would all be listed here.

* ``ExampleBase`` is abstract and therefore in pybind11 cannot have a constructor (even if it is present in C++).

Templates
---------

Now we move on to ``ExampleThree``.
This is a class template.
Following :ref:`this rule <style-guide-pybind11-declare-template-wrappers>` we declare its wrapper in a function ``declareExampleThree`` (that is itself templated on the same type, although the latter is not required):

.. code-block:: cpp

    namespace {

    template <typename T>
    void declareExampleThree(utils::python::WrapperCollection & wrappers, std::string const & suffix) {
        using Class = ExampleThree<T>;
        using PyClass = py::class_<Class, std::shared_ptr<Class>, ExampleBase>;

        wrappers.wrapType(
            PyClass(wrappers.module, ("ExampleThree" + suffix).c_str()),
            [](auto & mod, auto & cls) {
                cls.def(py::init<T>());
                cls.def("someOtherMethod", &Class::someOtherMethod);
            }
        );
    }

    } // anonymous

    void wrapExampleThree(utils::python::WrapperCollection & wrappers) {
        declareExampleThree<int>(wrappers, "I");
        declareExampleThree<double>(wrappers, "D");
    }

.. note::

    * We follow :ref:`this rule <style-guide-pybind11-common-code-namespace>` and stick the declare function in an annonymous namespace;
    * We use the alias rules for :ref:`types <style-guide-pybind11-class-alias>` and :ref:`pybind11 class objects <style-guide-pybind11-class-object-alias>` to minimize typing;
    * A ``suffix`` is appended to the name of the class in Python.
      Commonly used suffixes are:

      - ``I`` for ``int``,
      - ``L`` for ``uint64_t``,
      - ``F`` for ``float``,
      - ``D`` for ``double`` and
      - ``U`` for ``uint16_t``.

    (For historical reasons we have a mix of both traditional integer types and defined-size integer types.)

.. _pybind11-cross-module-dependencies:

Cross-module dependencies
-------------------------

All of the dependencies in the example classes we've defined here are within the same compiled module, and hence we've been able to rely on ``WrapperCollection`` and its callback system to ensure the wrappers are defined in an order that works.
The only exception is inheritance: ``ExampleTwo`` and ``ExampleThree`` both inherit from ``ExampleBase``, and that means it's critical that the ``wrapType`` call (or more precisely, the ``py::class_`` instantiation) for ``ExampleBase`` appear before that of either of its derived classes.

When dependencies extend beyond module boundaries, we need to import the modules that provide the classes we're using.
While it's possible to do that directly with ``py::module::import`` calls, it's more readable and less error-prone to use the ``addInheritanceDependency`` and ``addSignatureDependency`` methods of ``WrapperCollection``.
As its name suggests, the former is needed when you want to inherit from a base class defined in another module; this must be called before the ``py::class_`` instantiation of the derived class.
``addSignatureDependency`` declares that the external type is used only in function or method signatures.
Regardless of when it is called, these dependencies will be imported after all local types are declared and before any definition callbacks are run.

Circular *inheritance* dependencies are impossible in both C++ and Python, but circular signature dependencies are relatively common *within a single library* in C++ (via forward declarations) and quite possible in Python (via function-level imports and duck-typing).
In pybind11 wrappers, circular signature dependencies are more of a problem than they are in either language independently.
Using ``WrapperCollection`` solves that problem within a single module (in which all wrappers are added to the same ``WrapperCollection`` instance).
It also does its best to work around circular dependencies between different modules, but this relies on the details of how Python handles circular imports, making it very hard to guarantee correct behavior in all cases.
Circular dependencies between modules should be avoided whenever possible.


Wrapping Submodules with their Parent Module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the desired namespace for some symbols involves a subpackage nested below the level at which the ``WrapperCollection`` was defined, it's usually best to just define an entirely independent module for that subpackage.

It's also possible to create a submodule within the same compiled module, however, and this can be necessary when the classes in the subpackage have circular dependencies with those in the main package or other subpackages.

.. note::

    Compiled submodules are complex and make the organization of a package's code difficult to understand.
    Completely independent regular submodules should be used unless compiled submodules are necessary to deal with circular dependencies.

The module names and file/directory structure can be quite confusing in this case, so we'll look at a very concrete example.
Let's imagine we have a package ``lsst.foo``, with a normal package-level
module ``_foo``.
That implies we have the following files::

    lsst/
        foo/
            __init__.py
            _foo.cc
            SConscript

In order to add a submodule ``bar`` that wraps content from ``BarStuff.h``, we'll add a subpackage directory and ``__init__.py`` for it, and put a new source file in the subpackage directory, so the full structure now looks like this::

    lsst/
        foo/
            __init__.py
            _foo.cc
            SConscript
            bar/
                __init__.py
                _BarStuff.cc

Note that we've named the new file after the header it wraps, because it's going to be compiled into the ``_foo`` module.
In fact, it won't matter at all to the compiler where we put the source file; we've put it in the subpackage to signal to humans that that's where its symbols will land.

We will have to tell SCons about that extra file:

.. code-block:: py

    # SConscript
    from lsst.sconsUtils import scripts
    scripts.BasicSConscript.python(extra=["bar/_BarStuff.cc"])

The new ``_BarStuff.cc`` looks just like it would if ``bar`` was an independent module; it defines a regular ``wrap`` function:

.. code-block:: cpp

    namespace lsst { namespace foo { namespace bar {

    void wrapBarStuff(WrapperCollection & wrappers) {
        // ...
    }

    }}} // namespace lsst::foo::bar

When invoking that in ``_foo.cc``, however, we create a submodule ``WrapperCollection`` and pass that in:

.. code-block:: cpp

    namespace lsst { namespace foo {

    namespace bar {

    void wrapBarStuff(WrapperCollection & wrappers);

    } // namespace bar

    PYBIND11_MODULE(_foo, mod) {
        WrapperCollection wrappers(mod, "lsst.foo");
        { // extra scope just keeps variables very local
            auto barWrappers = wrappers.makeSubmodule("bar");
            bar::wrapBarStuff(barWrappers);
            wrappers.collectSubmodule(std::move(barWrappers));
        }
        wrappers.finish();
    }

    }} // namespace lsst::foo

Note that we need to use ``std::move`` to indicate that we're consuming ``barWrappers`` and are promising not to do anything else with it.

This submodule ``WrapperCollection`` doesn't actually put symbols in ``lsst.foo._foo.bar``, however.
If it did, the ``from ._foo import *`` line would create an ``lsst.foo.bar`` submodule that would clash with the existing directory/subpackage one.

Instead, ``makeSubmodule`` creates a ``lsst.foo._foo._bar`` submodule, while setting the ``__module__`` of its contents to ``lsst.foo.bar``.
That makes the ``lsst/foo/bar/__init__.py`` a bit tricky:

.. code-block:: py

    from .._foo._bar import *

While the higher-level ``lsst/foo/__init__.py`` stays simple:

.. code-block:: py

    from ._foo import *  # lifts _bar, too, but we don't care

    from . import bar  # optional; imports the package if it's always wanted


Pure-Python Customization
=========================

Adding new members
------------------

Sometimes it is necessary to add pure Python members to a wrapped C++ class.
Following our :ref:`structure and naming convention <style-guide-pybind11-module-naming>` for this, we'll add a new pure-Python ``_ExampleTwo.py`` module.
Note that this name doesn't conflict with ``_ExampleTwo.cc``, because that's never compiled into a standalone Python module.

We'll use the ``continueClass`` decorator to reopen the class and add a new method:

.. code-block:: python

    from lsst.utils import continueClass

    from ._tmpl import ExampleTwo

    __all__ = []  # import for side effects


    @continueClass
    class ExampleTwo:

        def someExtraFunction(self, x):
            return x + self.someOtherMethod()


Both the combined `_tmpl` module and any pure-Python customizations should be lifted into the package in its ``__init__.py``:

.. code-block:: python

    from ._tmpl import *
    from ._ExampleTwo import *

.. warning::

    Python's built-in ``super()`` function doesn't work properly in a ``continueClass`` block.

Grouping templated types with an ABC
------------------------------------

Using the ``TemplateMeta`` metaclass from ``lsst.utils`` we can group templated types together with a single abstract base class.

This gives users a familiar interface to work with templated types.
It allows them to do ``isinstance(my_object, ExampleThree)`` and create an ``ExampleThreeF`` type using ``ExampleThree(dtype=np.float32)``.

As with ``ExampleTwo``, add this to a pure-Python ``_ExampleThree.py``:

    .. code-block:: python

    import numpy as np

    from lsst.utils import TemplateMeta

    from ._tmpl import ExampleThreeI, ExampleThreeD

    __all__ = ["ExampleThree"]


    class ExampleThree(metaclass=TemplateMeta):
        pass


    ExampleThree.register(np.int32, ExampleThreeI)
    ExampleThree.register(np.float64, ExampleThreeD)
    ExampleThree.alias("I", ExampleThreeI)
    ExampleThree.alias("D", ExampleThreeD)

.. _pybind11_example: https://github.com/lsst-dm/pybind11_example
.. _`ExampleOne class in pybind11_example`: https://github.com/lsst-dm/pybind11_example/blob/master/src/ExampleOne.cc
