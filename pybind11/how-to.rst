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
where ``{{pkg}}`` is the name of the package, you will need to add the dependency
``setupRequired(pybind11)``.
You also need to modify the ``dependencies`` in ``{{pkg}}/ups/{{pkg}}.cfg``, by adding ``"pybind11"`` to ``"buildRequired"``.

.. _creating-module-file:

Creating a module file
^^^^^^^^^^^^^^^^^^^^^^

Following :ref:`our rules on file naming <style-guide-pybind11-module-naming>`, we start by creating a minimal module file ``python/lsst/TMPL/exampleOne.cc`` with the following content:

.. code-block:: cpp

    #include "pybind11/pybind11.h"

    #include "lsst/TMPL/ExampleOne.h"

    namespace py = pybind11;

    namespace lsst {
    namespace tmpl {

    PYBIND11_PLUGIN(exampleOne) {
        py::module mod("exampleOne");

        return mod.ptr();

    }}}  // lsst::tmpl

.. warning::

    The name used for the ``PYBIND11_PLUGIN(...)`` macro must match both the
    name used for ``mod(...)`` and the name of the file, otherwise an
    ``ImportError`` will be raised.

Wrapping the class
^^^^^^^^^^^^^^^^^^

We wrap the class using the ``py::class_<T>`` template:

.. code-block:: cpp

    PYBIND11_PLUGIN(exampleOne) {
        py::module mod("exampleOne");

        py::class_<ExampleOne, std::shared_ptr<ExampleOne>> clsExampleOne(mod, "ExampleOne");

        return mod.ptr();
    }

.. note::

    As in the example, classes should almost always have a :ref:`shared_ptr holder type <style-guide-pybind11-holder-type>`.

Wrapping enums
^^^^^^^^^^^^^^

The next thing to wrap is the enum (because it is used in the constructor arguments).
This is done using ``py::enum_``:

.. code-block:: cpp

    py::class_<ExampleOne, std::shared_ptr<ExampleOne>> clsExampleOne(mod, "ExampleOne");

    py::enum_<ExampleOne::State>(clsExampleOne, "State")
        .value("RED", ExampleOne::State::RED)
        .value("ORANGE", ExampleOne::State::ORANGE)
        .value("GREEN", ExampleOne::State::GREEN);

.. note::

    We attach the ``enum`` values to the class (by passing the ``py::class_`` object ``clsExampleOne`` as the first argument)

.. note::

    Add ``.export_values()`` if (and only if) you need to export the values into the
    class scope (so they can be reached as ``ExampleOne.RED``, in addition to ``ExampleOne.State.Red``).

    Never do this for new style scoped ``enum class`` types, since that will give
    them different symantics in C++ and Python.

Wrapping constructors
^^^^^^^^^^^^^^^^^^^^^

Constructors are added to the class using the ``py::init<T...>`` helper:

.. code-block:: cpp

    clsExampleOne.def(py::init<>());
    clsExampleOne.def(py::init<std::string const&, ExampleOne::State>());
    clsExampleOne.def(py::init<ExampleOne const&, bool>()); // Copy constructor

However, two of the constructors have default arguments. So we use the argument literal from ``pybind::literals`` to wrap them as keyword arguments (which following the rule on :ref:`keyword arguments <style-guide-pybind11-keyword-arguments>` should almost always be done, except for non-overloaded functions taking a single argument):

.. code-block:: cpp

    clsExampleOne.def(py::init<>());
    clsExampleOne.def(py::init<std::string const&, ExampleOne::State>(), "fileName"_a, "state"_a=ExampleOne::State::RED);
    clsExampleOne.def(py::init<ExampleOne const&, bool>(), "other"_a, "deep"_a=true); // Copy constructor

We also need to add: ``using namespace pybind11::literals;`` at the top.

.. warning::

    Unfortunately there is no way for pybind11 to track the value of the default argument.
    So be careful to dupplicate it correctly, and update it when it is changed in the code.

Getters and setters
^^^^^^^^^^^^^^^^^^^

We can wrap ``getState`` and ``setState`` as follows:

.. code-block:: cpp

    clsExampleOne.def("getState", &ExampleOne::getState);
    clsExampleOne.def("setState", &ExampleOne::setState);

Following the :ref:`rules on properties <style-guide-pybind11-properties>` you may choose to add a property too:

.. code-block:: cpp

    clsExampleOne.def_property("state", &ExampleOne::getState, &ExampleOne::setState);

Wrapping (overloaded) member functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Wrapping a member function is easy:

.. code-block:: cpp

    clsExampleOne.def("computeSomething", &ExampleOne::computeSomething);

However, when the function is overloaded we need to disambiguate the overloads.
Following the rule on :ref:`overload disambiguation <style-guide-pybind11-overload-disambiguation>` we use C-style casts for this:

.. code-block:: cpp

    clsExampleOne.def("computeSomethingElse",
                      (double (ExampleOne::*)(int, double) const) & ExampleOne::computeSomethingElse,
                      "myFirstParam"_a, "mySecondParam"_a);
    clsExampleOne.def("computeSomethingElse",
                      (double (ExampleOne::*)(int, std::string) const) &ExampleOne::computeSomethingElse,
                      "myFirstParam"_a, "anotherParam"_a="foo");

.. note::

    In the spirit of ``py::init<T...>``, there is also ``py::overload_cast<T...>``.
    This would be **really nice** to use, but we can't because it requires C++14.

STL containers
^^^^^^^^^^^^^^

The function ``ExampleOne::computeSomeVector`` returns a ``std::vector<int>``.
Following the :ref:`rule on STL containers <style-guide-pybind11-stl-containers>` we simply include
the ``pybind11/stl.h`` header (to enable automatic conversion to and from Python containers) and wrap the function as normal:

.. code-block:: cpp

    clsExampleOne.def("computeSomeVector", &ExampleOne::computeSomeVector);

Ndarray
^^^^^^^

The function ``ExampleOne::doSomethingWithArray`` takes an ``ndarray::Array`` argument.
To enable automatic conversion to and from ``numpy.ndarray`` in Python add the following include (right below the pybind11 ones):

.. code-block:: cpp

    #include "ndarray/pybind11.h"

Then the function can be wrapped as normal:

.. code-block:: cpp

    clsExampleOne.def("doSomethingWithArray", &ExampleOne::doSomethingWithArray);

The ndarray library also includes similarly automatic conversions for Eigen objects, which should be used instead of the optional Eigen converters packaged with Pybind11 itself.
Using both sets of converters in the same project is a violation of C++'s "One Definition Rule", a serious problem, and because a significant amount of LSST code already uses the ndarray converters, new code must as well.

.. note::

    Previous versions of the ndarray library also required ``numpy/arrayobject.h`` to be included, as well as a call to ``_import_array()`` in the module initialization function.
    As of ndarray 1.4.0, these steps are no longer necessary, but they will not yield incorrect behavior or errors (though they will generate warnings and slightly bloated code).

Static member functions
^^^^^^^^^^^^^^^^^^^^^^^

Wrapping *static* member functions is trivial:

.. code-block:: cpp

    clsExampleOne.def_static("initializeSomething", &ExampleOne::initializeSomething);

Wrapping operators
^^^^^^^^^^^^^^^^^^

According to our :ref:`rule on operators <style-guide-pybind11-operator>` we can either wrap
operators directly, or use a lambda.
Here we use both approaches:

.. code-block:: cpp

    clsExampleOne.def("__eq__", &ExampleOne::operator==, py::is_operator());
    clsExampleOne.def("__ne__", &ExampleOne::operator!=, py::is_operator());
    clsExampleOne.def("__iadd__", &ExampleOne::operator+= /* no py::is_operator() here */);
    clsExampleOne.def("__add__", [](ExampleOne const & self, ExampleOne const & other) { return self + other; }, py::is_operator());

.. note::

    * We use ``py::is_operator()`` to return ``NotImplemented`` on failure.
    * We don't use ``py::is_operator()`` for in-place operators as this can lead to confusing behavior.
    * We name the lambda arguments :ref:`self <style-guide-pybind11-lambda-self-argument>` and :ref:`other <style-guide-pybind11-lambda-other-argument>`.

Custom exceptions
^^^^^^^^^^^^^^^^^

The example contains a custom exception (``ExampleError``) added by the ``LSST_EXCEPTION_TYPE`` macro:

.. code-block:: cpp

    LSST_EXCEPTION_TYPE(ExampleError, lsst::pex::exceptions::RuntimeError, ExampleError)

To wrap it we can use the ``declareException`` macro from ``#include "lsst/pex/exceptions/python/Exception.h"``:

.. code-block:: cpp

    pex::exceptions::python::declareException<ExampleError, pex::exceptions::RuntimeError>(
            mod, "ExampleError", "RuntimeError");

Finished wrapper
^^^^^^^^^^^^^^^^

The end result of all the steps above looks like this:

.. code-block:: cpp

    #include "pybind11/pybind11.h"
    #include "pybind11/stl.h"

    #include "numpy/arrayobject.h"
    #include "numpy/arrayobject.h"
    #include "ndarray/pybind11.h"

    #include "lsst/pex/exceptions/python/Exception.h"

    #include "lsst/TMPL/ExampleOne.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst {
    namespace tmpl {

    PYBIND11_PLUGIN(exampleOne) {
        py::module mod("exampleOne");

        if (_import_array() < 0) {
                PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import");
                return nullptr;
        };

        pex::exceptions::python::declareException<ExampleError, pex::exceptions::RuntimeError>(
                mod, "ExampleError", "RuntimeError");

        py::class_<ExampleOne, std::shared_ptr<ExampleOne>> clsExampleOne(mod, "ExampleOne");

        py::enum_<ExampleOne::State>(clsExampleOne, "State")
            .value("RED", ExampleOne::State::RED)
            .value("ORANGE", ExampleOne::State::ORANGE)
            .value("GREEN", ExampleOne::State::GREEN)
            .export_values();

        clsExampleOne.def(py::init<>());
        clsExampleOne.def(py::init<std::string const&, ExampleOne::State>(), "fileName"_a, "state"_a=ExampleOne::State::RED);
        clsExampleOne.def(py::init<ExampleOne const&, bool>(), "other"_a, "deep"_a=true); // Copy constructor

        clsExampleOne.def("getState", &ExampleOne::getState);
        clsExampleOne.def("setState", &ExampleOne::setState);
        clsExampleOne.def_property("state", &ExampleOne::getState, &ExampleOne::setState);
        clsExampleOne.def("computeSomething", &ExampleOne::computeSomething);
        clsExampleOne.def("computeSomethingElse",
                          (double (ExampleOne::*)(int, double) const) & ExampleOne::computeSomethingElse,
                          "myFirstParam"_a, "mySecondParam"_a);
        clsExampleOne.def("computeSomethingElse", (double (ExampleOne::*)(int, std::string) const) &ExampleOne::computeSomethingElse, "myFirstParam"_a, "anotherParam"_a="foo");
        clsExampleOne.def("computeSomeVector", &ExampleOne::computeSomeVector);
        clsExampleOne.def("doSomethingWithArray", &ExampleOne::doSomethingWithArray);
        clsExampleOne.def_static("initializeSomething", &ExampleOne::initializeSomething);

        clsExampleOne.def("__eq__", &ExampleOne::operator==, py::is_operator());
        clsExampleOne.def("__ne__", &ExampleOne::operator!=, py::is_operator());
        clsExampleOne.def("__iadd__", &ExampleOne::operator+=);
        clsExampleOne.def("__add__", [](ExampleOne const & self, ExampleOne const & other) { return self + other; }, py::is_operator());

        return mod.ptr();
    }

    }}  // lsst::tmpl

Moving on
---------

In this section we are going to look at some more advanced wrapping.
In particular inheritance and templates
We shall also cover how to add pure Python members to wrapped C++ classes.

We wrap the following two header files from the ``templates`` package, ``ExampleTwo.h``:

.. code-block:: cpp

    #ifndef LSST_TMPL_EXAMPLETWO_H
    #define LSST_TMPL_EXAMPLETWO_H

    namespace lsst {
    namespace tmpl {

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

    }
    }  // namespace lsst::tmpl

    #endif

and ``ExampleThree.h``:

.. code-block:: cpp

    #ifndef LSST_TMPL_EXAMPLETHREE_H
    #define LSST_TMPL_EXAMPLETHREE_H

    #include "lsst/TMPL/ExampleTwo.h"

    namespace lsst {
    namespace tmpl {

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

    }
    }  // namespace lsst::tmpl

    #endif

Create wrapper files
^^^^^^^^^^^^^^^^^^^^

Again following :ref:`our rules on file naming <style-guide-pybind11-module-naming>` we create a basic file for the wrapper ``python/lsst/TMPL/exampleTwo.cc`` (note that this file will later move to a subpackage):

.. code-block:: cpp

    #include "pybind11/pybind11.h"

    #include "lsst/TMPL/ExampleTwo.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst {
    namespace tmpl {

    PYBIND11_PLUGIN(exampleTwo) {
        py::module mod("exampleTwo");

        return mod.ptr();
    }

    }}  // lsst::tmpl

And the same for ``exampleThree.cc``.

.. note::

    If any of this looks unfamilliar please see :ref:`"Wrapping a simple class" <wrapping-simple-class>` first.

Inheritance
^^^^^^^^^^^

``ExampleTwo.h`` defines two classes (``ExampleBase`` and ``ExampleTwo``) which we wrap as follows:

.. code-block:: cpp

    py::class_<ExampleBase, std::shared_ptr<ExampleBase>> clsExampleBase(mod, "ExampleBase");
    clsExampleBase.def("someMethod", &ExampleBase::someMethod);

    py::class_<ExampleTwo, std::shared_ptr<ExampleTwo>, ExampleBase> clsExampleTwo(mod, "ExampleTwo");

    clsExampleTwo.def(py::init<>());
    clsExampleTwo.def("someOtherMethod", &ExampleTwo::someOtherMethod);

There are two subtleties:

* ``ExampleTwo`` inherits from ``ExampleBase``. To indicate this we list ``ExampleBase`` as a template parameter when declaring ``clsExampleTwo``. If ``ExampleTwo`` had additional base classes they would all be listed here.

* ``ExampleBase`` is abstract and therefore in pybind11 cannot have a constructor (even if it is present in C++).

Templates
^^^^^^^^^

Now we move on to ``ExampleThree``. This is a class template.
Following :ref:`this rule <style-guide-pybind11-declare-template-wrappers>` we declare its wrapper in a function ``declareExampleThree`` (that is itself templated on the same type, although the latter is not required):

.. code-block:: cpp

    namespace {

    template <typename T>
    static void declareExampleThree(py::module & mod, std::string const & suffix) {
        using Class = ExampleThree<T>;
        using PyClass = py::class_<Class, std::shared_ptr<Class>, ExampleBase>;

        PyClass cls(mod, ("ExampleThree" + suffix).c_str());

        cls.def(py::init<T>());
        cls.def("someOtherMethod", &Class::someOtherMethod);
    }

    }

    PYBIND11_PLUGIN(exampleThree) {
        py::module::import("exampleTwo");  // See Cross module imports

        py::module mod("exampleThree");

        declareExampleThree<int>(mod, "I");
        declareExampleThree<double>(mod, "D");

        return mod.ptr();
    }

.. note::

    * We follow :ref:`this rule <style-guide-pybind11-wrapper-code-source-file-namespace>` and stick the declare function in an annonymous namespace;
    * We use the alias rules for :ref:`types <style-guide-pybind11-class-alias>` and :ref:`pybind11 class objects <style-guide-pybind11-class-object-alias>` to minimize typing;
    * A ``suffix`` is appended to the name of the class in Python.
      Commonly used suffixes are:

      - ``I`` for ``int``,
      - ``L`` for ``long``,
      - ``F`` for ``float``,
      - ``D`` for ``double`` and
      - ``U`` for ``unsigned int``.

Cross module imports
^^^^^^^^^^^^^^^^^^^^

The import statement:

.. code-block:: cpp

    py::module::import("exampleTwo");

in the previous example is present because ``ExampleThree`` depends on ``ExampleBase`` which is defined in a different module (i.e. ``exampleTwo``).

Thus, if you forget to add the import statement, the type ``ExampleBase`` is unknown if ``exampleThree`` happens to be imported before ``exampleTwo``.

Adding these import statements in the C++ wrapper, rather than relying on import order in ``__init__`` in Python, follows :ref:`our rule on import <style-guide-pybind11-import>`.

Finished wrappers (C++ part)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The end results for the C++ part of the wrappers (see next for the Python part) are ``exampleTwo.cc``:

.. code-block:: cpp

    #include "pybind11/pybind11.h"

    #include "lsst/TMPL/ExampleTwo.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst {
    namespace tmpl {

    PYBIND11_PLUGIN(exampleTwo) {
        py::module mod("exampleTwo");

        py::class_<ExampleBase, std::shared_ptr<ExampleBase>> clsExampleBase(mod, "ExampleBase");
        clsExampleBase.def("someMethod", &ExampleBase::someMethod);

        py::class_<ExampleTwo, std::shared_ptr<ExampleTwo>, ExampleBase> clsExampleTwo(mod, "ExampleTwo");
        clsExampleTwo.def(py::init<>());
        clsExampleTwo.def("someOtherMethod", &ExampleTwo::someOtherMethod);

        return mod.ptr();
    }

    }}  // lsst::tmpl

and ``exampleThree.cc``:

.. code-block:: cpp

    #include "pybind11/pybind11.h"

    #include "lsst/TMPL/ExampleThree.h"

    namespace py = pybind11;
    using namespace pybind11::literals;

    namespace lsst {
    namespace tmpl {
    namespace {

    template <typename T>
    static void declareExampleThree(py::module & mod, std::string const & suffix) {
        using Class = ExampleThree<T>;
        using PyClass = py::class_<Class, std::shared_ptr<Class>, ExampleBase>;

        PyClass cls(mod, ("ExampleThree" + suffix).c_str());

        cls.def(py::init<T>());
        cls.def("someOtherMethod", &Class::someOtherMethod);
    }

    }

    PYBIND11_PLUGIN(exampleThree) {
        py::module mod("exampleThree");

        py::module::import("exampleTwo");

        declareExampleThree<float>(mod, "F");
        declareExampleThree<double>(mod, "D");

        return mod.ptr();
    }

    }}  // lsst::tmpl

Adding pure Python members
^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes it is necessary to add pure Python members to a wrapped C++ class.
Following our :ref:`structure and naming convention <style-guide-pybind11-subpackage>` for this, we move ``exampleTwo.cc`` to a new subpackage (``exampleTwo``) and add an ``__init__.py`` file with the following content:

.. code-block:: python

    from __future__ import absolute_import

    from .exampleTwo import *
    from .exampleTwoContinued import *

The pure Python code then goes into ``exampleTwo/exampleTwoContinued.py``.
We shall use the ``continueClass`` decorator to reopen the class and add a new method:

.. code-block:: python

    from __future__ import absolute_import
    from lsst.utils import continueClass

    from .exampleTwo import ExampleTwo

    __all__ = [] # import for side effects

    @continueClass
    class ExampleTwo:

        def someExtraFunction(self, x):
            return x + self.someOtherMethod()

Grouping templated types with an ABC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the ``TemplateMeta`` metaclass from ``lsst.utils`` we can group
templated types together with a single abstract base class.

This gives users a familiar interface to work with templated types.
It allows them to do ``isinstance(my_object, ExampleThree)`` and
create an ``ExampleThreeF`` type using ``ExampleThree(dtype=np.float32)``.

As with ``ExampleTwo``, first move the module into its own subpackage.
Create the appropriate ``__init__.py`` file, and put the following in
``exampleThree/exampleThreeContinued.py``:

.. code-block:: python

    from __future__ import absolute_import
    import numpy as np

    from lsst.utils import TemplateMeta
    from .exampleThree import ExampleThreeF, ExampleThreeD

    __all__ = [] # import for side effects

    class ExampleThree(metaclass=TemplateMeta):
        pass

    ExampleThree.register(np.float32, ExampleThreeF)
    ExampleThree.register(np.float64, ExampleThreeD)
    ExampleThree.alias("F", ExampleThreeF)
    ExampleThree.alias("D", ExampleThreeD)

.. _pybind11_example: https://github.com/lsst-dm/pybind11_example
.. _`ExampleOne class in pybind11_example`: https://github.com/lsst-dm/pybind11_example/blob/master/src/ExampleOne.cc
