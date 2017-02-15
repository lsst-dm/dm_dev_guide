##################
DM C++ Style Guide
##################

This is the DM C++ Coding Standard.

Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
To request changes to these standards, please file an :ref:`RFC <decision-making-rfc>`.

.. contents::
   :depth: 4

.. _style-guide-cpp-preface:

Preface
=======

The communal nature of creating project software necessitates simplicity and elegance in the crafting of code.
Since a piece of code may be a collaboration, as much as any paper, without readability and comprehensibility the result of the collaboration may not preserve integrity of design intent.
Without simplicity, it might not be possible to make a judgment of that integrity.

Preserving integrity of design intent is important. The creation of a piece of software is an exercise in developing a consistent set of descriptions (requirements, design, code, tests, manuals) that preserve and manage the evolution of the intent of that software throughout its lifetime.
This gains more importance as the key form of these descriptions is an operational (imperative) form, which will decide how a system will react to specified (an, in some cases, unexpected) external stimuli.

This document is strongly based on (verily, virtually identical to) the `CARMA <http://www.mmarray.org/workinggroups/computing/cppstyle.html>`_ [Pound]_ C++ Coding Standards which, in turn, was strongly based on Geosoft [Geosoft]_ and `ALMA C++ Coding Standards <https://science.nrao.edu/facilities/alma/aboutALMA/Technology/ALMA_Computing_Memo_Series/0009/2001-06-06.pdf>`_ [Bridger2001]_.
The layout section of this document is also based on the `Google C++ Style Guide <https://google.github.io/styleguide/cppguide.html>`_ [Google]_.
We have taken the CARMA HTML document and changed it in places to match LSST's needs.
CARMA, Geosoft, ALMA and Google retain their respective copyrights where appropriate.

.. _style-guide-cpp-intro:

1. Introduction
===============

This document lists C++ coding recommendations common in the C++ development community.
The recommendations are based on established standards collected from a number of sources, individual experience, local requirements/needs, as well as suggestions given in [McConnell2004]_, [Henricson1992]_, [Henricson1992]_, [Hoff2008]_ and [Google]_. 

While a given development environment (IDE) can improve the readability of code by access visibility, color coding, automatic formatting and so on, the programmer should never rely on such features.
Source code should always be considered larger than the IDE it is developed within and should be written in a way that maximizes its readability independent of any IDE.

Refer to the :ref:`stringency level reference <style-guide-rfc-2119>` for the guiding principles regarding the stringency levels and under what circumstances you may deviate from a guideline.

.. _style-guide-cpp-intro-layout:

1.1 Layout of recommendations
-----------------------------

The recommendations are grouped by topic and each recommendation is numbered to make it easier to refer to during reviews.

Layout of the recommendations is as follows:

   **x.y Guideline**

   Short description

   Motivation, background and additional information.

The motivation section is important.
Coding standards and guidelines tend to start "religious wars", and it is important to state the background for the recommendation.

.. _style-guide-cpp-intro-vocab:

1.2. Recommendation Importance
------------------------------

In the guideline sections, the terms **required**, **must**, **should**, amongst others, have special meaning.
Refer to :ref:`Stringency Level <style-guide-rfc-2119>` reference.
DM uses the spirit of the IETF organization's `RFC 2199 Reference <http://www.ietf.org/rfc/rfc2119.txt>`_ definitions.

.. _style-guide-cpp-2:

2. General Recommendations
==========================

.. _style-guide-cpp-2-1:

2-1. Remember, we are writing code for humans to read, not computers.
---------------------------------------------------------------------

At some point, someone unfamiliar with your code (often a future you) will have to examine it, typically to fix a bug or upgrade it.
These tasks are made much simpler if the code is easily readable and well-documented.

.. _style-guide-cpp-2-2:

2-2. We are writing C++11/14 with some restrictions.
----------------------------------------------------

The official policy on the use of C++11 features is at :ref:`Policy on use of C++11/14 language features <style-guide-cpp-cpp-11-14>`.

.. _style-guide-cpp-2-3:

2-3. Some rules MAY be violated under certain circumstances.
------------------------------------------------------------

See :ref:`Deviating from the DM Style Guides <style-guide-deviations>`.

.. _style-guide-cpp-2-4:

2-4. Object orientation SHOULD be used in your programs
-------------------------------------------------------

- Do not just code C style in C++.

- Make a real class for any behavior on a data structure, do not make a struct for the data and separate functions to operate on it.

- Structs are appropriate only for cases needing very lightweight data structure and no behavior.

- Avoid overly complex inheritance hierarchies, more than 3 levels should be a warning sign (except in Frameworks).

- Use inheritance to specialize behavior for the same or similar data, use templates to specialize data for the same behavior.

- Avoid multiple inheritance, and only use when it is for completely distinct/disjoint considerations (such as application role versus persistence container type).

- You may overload member functions but try to do so only where required (virtual functions) or you need to vary the parameter list.

- Keep functions short and with a single purpose.

The process combines UML modeling and C++ programming, they are integrated and reinforce each other.
This process integration is documented in `LSST Prototyping Environment <https://dev.lsstcorp.org/trac/wiki/PrototypingEnvironment>`_.

.. _style-guide-cpp-3:

3. Naming Conventions
=====================

.. _style-guide-cpp-general-naming-conventions:

3.1. General Naming Conventions
-------------------------------

.. _style-guide-cpp-3-0:

3-0. Guidance on Selecting Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The fundamental quantity being described should appear first in the name, with modifiers concatenated afterward.
A rule of thumb is to ask what the units of the quantity would be, and make sure that quantity appears first in the name.

- ``dateObs``, not ``obsDate`` for a quantity that fundamentally is a date/time of significance;
- ``timeObsEarliest`` (or, ``timeObsFirst``), not ``earliestObsTime``
- ``nGoodPix`` not ``goodPixN`` since this is fundamentally a number
- There are some historical exceptions (e.g., ``expTime`` from the FITS standard) that must be preserved

Use care to select the most meaningful name to represent the quantity being described

- ``imageMean`` not ``pixelMean`` if we are talking about the mean value of an image, not repeated measurements of a pixel

Names should not explicitly include units

- ``skyBackground`` not ``skyADU`` to indicate the sky background level
- ``expMidpoint`` rather than ``taiMidPoint``; or ``timeRange" not "taiRange``

Acronyms should be used sparingly, and limited to very common usages in the relevant community.

- CCD, FWHM, ID, PSF, and RA would be fine as name fragments

Obscure abbreviations should be avoided: clarity is probably more important than brevity.

- ``apertureDiam`` would be better than ``apDia``

The Database Schema document should be reviewed for existing appropriate names

- Check the authoritative DB Column names for the current Project in order to select consistent names between persisted C++ variables and their corresponding DB Columns.
  
.. FIXME

   Refer to Section 3.3 Names Exposed to Database. (Note: Sect. 3.3 does not appear to exist!)

.. _style-guide-cpp-3-1:

3-1. Names of user defined types MUST be in mixed case starting with uppercase.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class Line, SavingsAccount;
   
   struct {
       float bar;
       int yoMama;
   } Foo;
   Foo myFoo;

   typedef Vector<Frame> FrameVector;

Common practice in the C++ development community.
The capitalization rule for class names should be all words in the name capitalized, e.g., ``ClassName``.

.. _style-guide-cpp-3-2:

3-2. Variable names MUST be in mixed case starting with lower case.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int lineWidth;

Common practice in the C++ development community.
Makes variables easy to distinguish from types, and effectively resolves potential naming collision as in the declaration Line line.
Keep variable names balanced between short and longer, more meaningful.
Use 8 to 20 characters as a guideline (excluding integer loop counters which may be as little as 1 character).

.. _style-guide-cpp-3-3:

3-3. Named constants (including enumeration values) MUST be all uppercase using underscore to separate words.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Common practice in the C++ development community.

.. code-block:: cpp

   int const MAX_ITERATIONS = 25;
   int const MIN_ITERATIONS(23);
   enum { HIGH_SCHOOL, GRAMMAR_SCHOOL, KINDEGARTEN };

In general, the use of such constants should be minimized.
In many cases implementing the value as a method is a better choice:

.. code-block:: cpp

   int getMaxIterations() {  // NOT: int const MAX_ITERATIONS = 25
       return 25;
   }

This form is both easier to read, and it ensures a unified interface towards class values.
Note that this rule applies only to ``const`` variables that represent constants (i.e. those that would be set using an ``enum`` or ``#define`` in C); it does not apply to variables that happen to be determined at their point of definition, e.g.:

.. code-block:: cpp

   void foo(string const& filename);
   float const r2 = r * r;  // radius^2

.. _style-guide-cpp-3-4:

3-4. Names representing methods or functions SHOULD naturally describe the action of the method (and so will usually start with a verb) and MUST be written in mixed case starting with lowercase. Private member function names MUST additionally lead with an underscore.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do not put a space between the function name and the opening parenthesis when declaring or invoking the function.

.. code-block:: cpp

   class GoodClass {
   public:
       void const getPublic() {}  // OK
   protected:
       void const getProtected() {}  // OK
   private:
       void const _getPrivate() {}  // OK
   };
   
   void getName() { ... }            // OK
   void computeTotalWidth() { ... }  // OK

Refer to :ref:`Rule 3-10 <style-guide-cpp-3-10>` for a discussion on the leading underscore requirement for private member functions.

Common practice in the C++ development community.
This is identical to variable names, but functions in C++ are already distinguishable from variables by their specific form.

.. _style-guide-cpp-3-4a:

3-4a. Names for methods that return new objects MAY start with past-tense verbs.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is sometimes useful to pair a mutator with a ``const`` method that returns a mutated copy of the callee.
When it is, the imperative verb in the name of the mutator MAY be changed to the past tense to make the distinction clear.
For example:

.. code-block:: cpp

   Box b;
   b.dilateBy(a);           // b is modified
   Box c = b.dilatedBy(a);  // a modified copy of b is assigned to c

.. _style-guide-cpp-3-5:

3-5 A name representing a ``typedef`` MUST be initial letter capitalized, camel-case with no prefix of the enclosing class.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   typedef unsigned char Byte;
   typedef unsigned long BitMask;
   Byte smallMask;

This syntax is consistent with template type names and classes which are also similar in usage.

.. _style-guide-cpp-3-5a:

3-5a. A name representing a ``typedef`` SHOULD have a ``T`` suffix if and only if necessary to disambiguate the typedef from a template bare name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the ``typedef`` is a template specialization of a concrete type, the typedef name should typically include some indication of the parameter type (e.g. ``typedef Image<float> ImageF;``).
If the specialization uses an incoming template parameter, the suffix ``T`` is preferred to using the specialized template's bare name, as the latter is very difficult to use correctly in C++.

.. _style-guide-cpp-3-6:

3-6. Names representing namespaces MUST be camelCase with leading lowercase letter and based on component or directory name.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The original package developer will specify in the ``.cc`` file the preferred abbreviation to use and, optionally, also use it throughout their code.
The original developer may consider using the following guideline to fabricate the name:

- remove the preliminary 'lsst';
- concatenate the remaining fields;
- if desired to make shorter, abbreviate each field while still maintaining a relevant word.

.. code-block:: cpp

   namespace pexLog = lsst::pex::logging;
   namespace afwMath = lsst::afw::math;

Three options are available for using a namespace when defining symbols

1. Specify the namespace explicitly in the definition

   .. code-block:: cpp

      lsst::foo::bar::myFunction(...) { ... }

2. Use an abbreviation for the namespace

   .. code-block:: cpp

      namespace fooBar = lsst::foo::bar;
      fooBar::myFunction(...) { ... };

3. Put the definitions into a namespace block

   .. code-block:: cpp
   
      namespace lsst {
      namespace foo {
      namespace bar {

      myFunction(...) { ... };

      }}}  // lsst::foo::bar

.. _style-guide-cpp-3-7:

3-7. Names representing template parameters MAY be a single uppercase letter or a mixed case phrase, first letter capitalized in each word, indicating the desired type.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   template <typename T> ...             // acceptable
   template <typename C, typename D> ... // acceptable
   template <class PixelType> ...  // acceptable, user-defined class only

Common practices in the C++ development community.
Regarding the use of ``typename`` versus ``class``, we will adopt the convention of using ``typename`` in all cases except where the intent is ONLY a user-defined class and not primitives.
It is recommended that template parameter names that are not a single character be suffixed with ``T`` or ``Type`` to distinguish them from other, concrete types.

.. _style-guide-cpp-3-8:

3-8. Abbreviations and acronyms MUST not be uppercase when used as name.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   exportHtmlSource();    // NOT: exportHTMLSource();
   openDvdPlayer();       // NOT: openDVDPlayer();

Using all uppercase for the base name will give conflicts with the naming conventions given above.
A variable of this type would have to be named ``dVD``, ``hTML`` etc., which obviously is not very readable.

Another problem is illustrated in the examples above.
When the name is connected to another, the readability is seriously reduced; the word following the abbreviation does not stand out as it should.

.. _style-guide-cpp-3-9:

3-9. Global variables and functions SHOULD be avoided and if used MUST always be referred to using the ``::`` operator.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   ::mainWindow.open(), ::applicationContext.getName(), ::erf(1.0)

In general, the use of global variables should be avoided.
Consider using singleton objects instead.
Only use where required (i.e. reusing a framework that requires it.).
See :ref:`Rule 5-7 <style-guide-cpp-5-7>`.

Global functions in the root namespace that are defined by standard libraries can often be avoided by using the C++ versions of the include files (e.g. ``#include <cmath>`` instead of ``#include <math.h>``).
Since the C++ include files place functions in the std namespace, ``using namespace std;``, which is permitted by :ref:`Rule 5-41 <style-guide-cpp-5-41>`, will allow these functions to be called without using the ``::`` operator.
In cases where functions are only available in the C include files, the ``::`` operator must be used to call them.
This requirement is intended to highlight that these functions are in the root namespace and are different from class methods or other namespaced free functions.

.. _style-guide-cpp-3-10:

3-10. Private class variables and methods MUST have underscore prefix.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*(TBD In the future, commentary will be added on restrictions regarding single letter private functions)*

.. code-block:: cpp

   class SomeClass {
   private:
       int _length;
       int _computeBlob();
   }

Apart from its name and its type, the scope of a variable or method is its most important feature.

Indicating class scope by using underscore makes it easy to distinguish class variables from local scratch variables.
This is important because class variables are considered to have higher significance than method variables, and should be treated with special care by the programmer.
A side effect of the underscore naming convention is that it nicely resolves the problem of finding reasonable variable names for setter methods and constructors:

.. code-block:: cpp

   void setDepth(int depth) { _depth = depth; }

An issue is whether the underscore should be added as a prefix or as a suffix.
Both practices are commonly used.
Since LSST Data Management uses both C++ and Python as implementation languages, prefixing the underscore is recommended in order to maintain conformity with Python's naming convention where variables and functions with leading underscore are treated specially.
Care must be given to avoid using a reserved name.

It should be noted that scope identification has been a controversial issue for quite some time.
It seems, though, that this practice now is gaining acceptance and that it is becoming more and more common as a convention in the professional development community.

.. _style-guide-cpp-3-11:

3-11. Generic variables MAY have the same name as their type.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void setTopic(Topic *topic)      // NOT: void setTopic (Topic *value)
                                    // NOT: void setTopic (Topic *aTopic)
                                    // NOT: void setTopic (Topic *x)
    
   void connect(Database *database) // NOT: void connect (Database *db)
                                    // NOT: void connect (Database *oracleDB)

Reduce complexity by reducing the number of terms and names used.
Also makes it easy to deduce the type given a variable name only.

If for some reason this convention doesn't seem to fit it is a strong indication that the type name is badly chosen.

Non-generic variables have a role. These variables can often be named by combining role and type:

.. code-block:: cpp

   Point startingPoint, centerPoint;
   Name loginName;

.. _style-guide-cpp-3-12:

3-12. All names MUST be written in English and use American English spelling.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int fileName;    // NOT:   int filNavn;
   int color;       // NOT:   int colour;

English is the preferred language for international development.

.. _style-guide-cpp-3-13:

3-13. Variables with a large scope SHOULD have long names, variables with a small scope MAY have short names.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Scratch variables used for temporary storage or indices are best kept short.
A programmer reading such variables should be able to assume that its value is not used outside a few lines of code.
Common scratch variables for integers are ``i``, ``j``, ``k``, ``m``, ``n`` and for characters ``c`` and ``d``.

.. _style-guide-cpp-3-14:

3-14. The name of the object is implicit, and SHOULD be avoided in a method name.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   line.getLength();    // NOT:  line.getLineLength();

The latter seems natural in the class declaration, but proves superfluous in use, as shown in the example.

.. _style-guide-cpp-3-37:

3-37 Names representing containers of numeric STL built-ins MUST be of the form: ``[capitalized STL name][element type suffix used in afw::image]``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<double> => VectorD
   std::list<int> => ListI

.. _style-guide-cpp-3-37a:

3-37a Names representing containers of DM objects SHOULD be of the form: ``[element class name, ignoring ptrs][capitalized STL name]``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   std::vector<PTR(Span)> => SpanVector
   std::list<Box2I> => Box2IList

However, containers which have a clear meaning in a particular context, (e.g. ``MaskPlaneDict``), MAY use a name that describes that meaning (like ``MaskPlaneDict``).

Or if, for example, a container is logically a list (i.e. doesn't need random access) but is actually a ``std::vector`` for simplicity/performance reasons, it may be called a ``List``, especially to preserve backwards compatibility.

.. _style-guide-cpp-3-38:

3-38 Names representing static factory methods SHOULD indicate the special properties of the objects created by that factory method.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Vector3d v = Vector3d::orthogonalTo(vector1, vector2);
   Vector3d n = Vector3d::northFrom(vector);
   Circle c = Circle::empty();

Sometimes, there can be more than one factory method with the same argument signature, all of which create objects with similar characteristics.
In this case, the factory method name SHOULD begin with 'from' and indicate the distinguishing properties of the arguments.
For example:

.. code-block:: cpp

   Angle::fromDegrees(1.0);
   Angle::fromRadians(1.0);

.. _style-guide-cpp-specific-naming-conventions:

3.2. Specific Naming Conventions
--------------------------------

.. _style-guide-cpp-3-15:

3-15. The terms ``get``/``set`` MUST be used where an attribute is accessed directly and in the imperative form. The variable name portion should be the same as the actual variable name but now with the first letter capitalized.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   employee.getName();       matrix.getElement(2, 4);
   employee.setName(name);   matrix.setElement(2, 4, value);

Common practice in the C++ development community.
In Java this convention has become more or less standard.
Methods that return a reference to an object for which "set" has no meaning, should not follow this convention.
For instance, use:

.. code-block:: cpp

   Antenna().Drive().getFoo()

rather than:

.. code-block:: cpp

   getAntenna().getDrive().getFoo()

.. _style-guide-cpp-3-16:

3-16.
^^^^^

*Deleted*

.. _style-guide-cpp-3-17:

3-17. The term ``find`` SHOULD be used in methods where something is looked up.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   vertex.findNearestVertex();   matrix.findMinElement();

Give the reader the immediate clue that this is a simple look up method with a minimum of computations involved.
Consistent use of the term enhances readability.

.. _style-guide-cpp-3-18:

3-18. The term ``initialize`` SHOULD be used where an object or a concept is established.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   printer.initializeFontSet();

The American ``initialize`` should be preferred over the English ``initialise.``
Abbreviation ``init`` should be avoided.

.. _style-guide-cpp-3-19:

3-19. Variables representing GUI components SHOULD be suffixed by the component type name.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``mainWindow``, ``propertiesDialog``, ``widthScale``, ``loginText``, ``leftScrollbar``, ``mainForm``, ``fileMenu``, ``minLabel``, ``exitButton``, ``yesToggle``, etc..

Enhances readability since the name gives the user an immediate clue of the type of the variable and thereby the object's resources.

.. _style-guide-cpp-3-20:

3-20. The suffix ``List`` MAY be used on names representing a list of objects.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   Vertex (one vertex),   vertexList (a list of vertices)

Enhances readability since the name gives the user an immediate clue of the type of the variable and the operations that can be performed on the object.

Simply using the plural form of the base class name for a list---e.g., ``matrixElement`` (one matrix element) and ``matrixElements`` (list of matrix elements)---should be avoided since the two only differ in a single character and are thereby difficult to distinguish.

A list in this context is the compound data type that can be traversed backwards, forwards, etc. (typically an STL vector ).
A plain array is simpler.
The suffix ``Array`` can be used to denote an array of objects.

.. _style-guide-cpp-3-21:

3-21. The prefix ``n`` SHOULD be used for variables representing a number of objects.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   nPoints, nLines

The notation is taken from mathematics where it is an established convention for indicating a number of objects.

.. _style-guide-cpp-3-22:

3-22. The filter name prefix (ugrizy) MUST be used if and only if the name is specific to a filter.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example:

.. code-block:: cpp

   float iAmplitude, iPeriod;   // OK
   float gAmplitude, gPeriod;   // OK
   int iLoopCtr;                // BAD

This recommendation fosters consistent naming of C++ and DB shared persistent objects which use a filter-initial prefix.
Naming DB persistent objects by incorporating their filter band fosters the efficiency of a simple sort rule.
If the C++ data is maintained in an array indexed by filter, this rule doesn't apply.

.. _style-guide-cpp-3-23:

3-23. Iterator variables SHOULD be declared within the loop scope.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   for (vector<MyClass>::iterator listIter = list.begin(); listIter != list.end(); listIter++) {
       Element element = *listIter;
       // ...
   }

It is not always possible to declare iterator variables in scope (for example if you have several iterators of different type), but do it when you can.
Declare additional iterator variables just before the loop, so it's clear that they are associated with the loop.

.. _style-guide-cpp-3-24:

3-24. Names for boolean variables and methods SHOULD be obviously boolean.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Examples of good names include:

.. code-block:: cpp

   bool isSet, isVisible, isFinished, isFound, isOpen;
   bool exists();
   bool hasLicense(), canEvaluate(), shouldSort()

Common practice in the C++ development community and partially enforced in Java.
Using the ``is`` prefix can highlight a common problem of choosing bad boolean names like ``status`` or ``flag``.
``isStatus`` or ``isFlag`` simply doesn't fit, and the programmer is forced to choose more meaningful names.

.. _style-guide-cpp-3-25:

3-25. Complement names MUST be used for complement operations.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``get/set``, ``add/remove``, ``create/destroy``, ``start/stop``, ``insert/delete``, ``increment/decrement``, ``old/new``, ``begin/end``, ``first/last``, ``up/down``, ``min/max``, ``next/previous``, ``old/new``, ``open/close``, ``show/hide``, ``suspend/resume``, etc..

Reduce complexity by symmetry.

.. _style-guide-cpp-3-26:

3-26. Abbreviations in names SHOULD be avoided.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   computeAverage();     // NOT:  compAvg();

There are two types of words to consider.
First are the common words listed in a language dictionary.
These must never be abbreviated.
For example, write:

- ``command`` instead of ``cmd``
- ``copy`` instead of ``cp``
- ``point`` instead of ``pt``
- ``compute`` instead of ``comp``
- ``initialize`` instead of ``init``

Then there are domain specific phrases that are more naturally known through their abbreviations/acronym.
These phrases should be kept abbreviated.
For example, write:

- ``html`` instead of ``HypertextMarkupLanguage``
- ``cpu`` instead of ``CentralProcessingUnit``
- ``ccd`` instead of ``ChargeCoupledDevice``

.. _style-guide-cpp-3-27:

3-27.
^^^^^

*(Deleted)*

.. _style-guide-cpp-3-28:

3-28. Negated boolean variable names MUST be avoided.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   bool isError;    // NOT:   isNoError
   bool isFound;    // NOT:   isNotFound

The problem arises when such a name is used in conjunction with the logical negation operator as this results in a double negative.
It is not immediately apparent what ``isNotFound`` means.

.. _style-guide-cpp-3-29:

3-29. Enumeration constants MAY be prefixed by a common type name if at global (or namespace) scope.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   enum { GRADE_HIGH, GRADE_MIDDLE, GRADE_LOW };

Where possible, put enums in appropriate classes, in which case the ``GRADE_*`` isn't needed:

.. code-block:: cpp

   class Grade {
       enum { HIGH, MIDDLE, LOW };
   
       Grade() {}
       ...
   };

This gives additional information of where the declaration can be found, which constants belongs together, and what concept the constants represent.

.. _style-guide-cpp-3-30:

3-30. Exception classes which indicate an error condition MUST end with Error, otherwise they SHOULD be suffixed with Exception.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class AccessError {
     // ...
   }

Exception classes are really not part of the main design of the program, and naming them like this makes them stand out relative to the other classes.

.. _style-guide-cpp-3-31:

3-31. Functions (methods returning something) SHOULD be named after what they return and procedures (void methods) after what they do.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   double& getElevation(unsigned int antennaId), void pointAntenna(Source const &source)

Increase readability.
Makes it clear what the unit should do and especially all the things it is not supposed to do. This again makes it easier to keep the code clean of side effects.

.. _style-guide-cpp-3-32:

3-32. Parameters in functions SHOULD be declared in order of output, input, default input.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Keeps inputs together and when SWIG is used avoids moving output parameters out of the middle of the list.

.. _style-guide-cpp-3-33:

3-33.
^^^^^

*Deleted.*

.. _style-guide-cpp-3-34:

3-34. Uncertainty values associated with a variable SHOULD be suffixed by one of ``Var``, ``Cov``, ``Sigma``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is no universal suffix for uncertainties; i.e. no ``Err`` suffix will be used.
The cases that we have identified, and their appropriate suffixes, are:

- Standard deviation: ``Sigma`` (not ``Rms``, as ``rms`` doesn't imply that the mean's subtracted)
- Covariance: ``Cov``
- Variance: ``Var``

.. code-block:: cpp

   float xAstrom;          // x position computed by a centroiding algorithm
   float xAstromSigma;     // Uncertainty of xAstrom
   float yAstrom;
   float yAstromSigma;
   float xyAstromCov;
 
The postfix ``Err`` can easily be misinterpreted as error flags.
Use the full ``Sigma`` since ``Sig`` can easily be misinterpreted as ``Signal``.

.. _style-guide-cpp-3-35:

3-35.
^^^^^

*Unused.*

.. _style-guide-cpp-3-36:

3-36.
^^^^^

*Deleted.*

.. _style-guide-cpp-3-39:

3-39. Names for static functions or methods that read from disk SHOULD start with ``read``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For consistency with existing code, prefer ``read`` over ``load``.

.. _style-guide-cpp-3-40:

3-40. Names for static methods that naturally start with some sort of creation verb SHOULD start with ``make``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For consistency with existing code, prefer ``make`` over ``build``, ``create``, or ``compute`` (at least when the method is a static method of the class that is being constructed).

.. _style-guide-cpp-files:

4. Files
========

.. _style-guide-cpp-source-files:

4.1 Source Files
----------------

.. _style-guide-cpp-4-1a:

4-1.a The head of each ``.h`` and each ``.cc`` file MUST begin with a fixed format comment declaring the file contents and format to emacs.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // -*- LSST-C++ -*-

This solved the emacs problem of not recognizing a C++ header file ending in ``.h``.
Vim use is not affected.

.. _style-guide-cpp-4-1b:

4-1.b C++ header files MUST have the extension ``.h`` (preferred) or ``.hpp`` (allowed).
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   myClass.h, myClassa.hpp

These are accepted C++ standards for file extension.

.. _style-guide-cpp-4-1c:

4-1.c C++ source files MUST have the extension ``.cc``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   myClass.cc

These are accepted C++ standards for file extensions.

.. _style-guide-cpp-4-2:

4-2. Files that contain a single class SHOULD have the name of the class, including capitalization.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   MyClass.h, MyClass.cc

Makes it easy to find the associated files of a given class.
This convention is enforced in Java and has become very successful as such.
In general, there should be one class declaration per header file.
In some cases, smaller related classes may be grouped into one header file.

.. _style-guide-cpp-4-3:

4-3. Member functions and data SHOULD be listed logically.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, all constructors should be grouped together, all event handling routines should be declared together, as should the routines which access member data.
Each logical group of functions should have a common comment above the group explaining why they are grouped together.

.. _style-guide-cpp-4-4a:

4-4.a All non-templatized class/function definitions except inlines SHOULD reside in source files.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class MyClass {
   public:
       int doSomethingComplicated() {  // NO!
           float a = exp(-h*nu/(k*T));
           float foobar = computeFooBar(a, PI/4);
           ...
           return value;
       }
   }

The header files should declare an interface, the source file should implement it.
When looking for an implementation, the programmer should always know that it is found in the source file.
The obvious exception to this rule is of course inline functions that must be defined in the header file (see next rule).

.. _style-guide-cpp-4-4b:

4-4.b All templatized classes/functions, MUST be explicitly instantiated, i.e. the type declared and the instances to be used explicitly instantiated in the header file, the type members are defined in the source file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Also, template instantiations should be declared extern to ensure that the compiler and programmers know which instantiations are intended.

In :file:`MyString.h`:

.. code-block:: cpp

   template <typename CharType>
   class MyString {
       //...
   };
   extern template class MyString<char>;  // Inhibits implicit MyString<char>

We expect to freely use template classes in the framework and possibly elsewhere in the application layer.
There will be many template class declarations and many instantiations of them.
On the other hand, we want to preserve the separation of interface (declaration) in ``.h`` files from implementation (definition) in ``.cc`` files.

The solution is explicit template instantiation.
This requires that the specific template instantiations (classes) that are to be used be compiled into a library, and then the ``.h`` files can remain separate, as long as they explicitly declare which template instantiations will be used.
In explicit template instantiation the compiler and linker handle the details of this process for you.
You can also set the compiler to prohibit any implicit template instantiations (with no-implicit-templates) to prevent accidental double definitions.

This works quite well for those using a framework and not extending it, i.e. one knows the template instantiations available to the application at compile time and does not create new instantiations, one just uses the ones that are already defined.
For most applications that are not extending the framework, this should be pretty clear and will probably work quite well.
It is less clear for the framework itself, but we can always rely on the linker to tell us when we have goofed and allowed something to be doubly defined.

.. _style-guide-cpp-4-5:

4-5. In-line functions SHOULD be avoided except for simple accessors/mutators that get or set a simple attribute or empty constructors/destructors.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If used, in-line functions should be very simple.
If an in-line function has a body of more than 5 lines, it should be placed outside the class definition.

.. code-block:: cpp

   #ifndef LSST_FOO_H
   #define LSST_FOO_H
   
   class Foo {
   public:
       Foo();
       virtual ~Foo() {}
       int getValue() const { return _value; }
       inline int getAnotherValue() const;
   
   private:
       int _value;
       int _anotherValue;
   };
   
   int Foo::getAnotherValue() const { return _anotherValue; }
   
   #endif  // LSST_FOO_H

Empty constructor:

.. code-block:: cpp

   explicit IdSpan(int id, int y) : id(id), y(y) {}

When choosing whether to inline, think about balancing compile-time and run-time performance.
Be careful to avoid requiring inclusion of additional ``.h`` files; use forward declaration if needed.
See Myers, *Effective C++ 3rd Ed.,* item 30.

.. _style-guide-cpp-4-6:

4-6. File content MUST be kept within 110 columns.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The restriction to 80 columns is no longer as much a consideration as a common dimension for editors, terminal emulators, printers and debuggers, and so on.
However, even with multi-window environments and current displays it is often useful to have multiple source windows open side by side, and limiting the number of characters facilitates this.
It improves readability when unintentional line breaks are avoided when passing a file between programmers.

.. _style-guide-cpp-4-7:

4-7. Use of special characters like TAB, carriage-return (ctrl-M) and page break are PROHIBITED.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These characters can cause problem for editors, printers, terminal emulators or debuggers when used in a multi-programmer, multi-platform environment.

.. _style-guide-cpp-4-8:

4-8. The incompleteness of split lines MUST be made obvious.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Emacs indentation rules are suggested.
As a minimum, indent the continuation at least 4 spaces.
Indentation to the right of an opening parenthesis that has not yet been closed or an assignment operator is also permitted.

.. code-block:: cpp

   totalSum = a + b + c +
              d + e;
   function(param1, param2,
            param3);
   setText("Long line split"
           "into two parts.");
   for (tableNo = 0; tableNo < nTables;
        tableNo += tableStep)

Split lines occur when a statement exceeds the 110 column limit given above.
It is difficult to give rigid rules for how lines should be split, but the examples above should give a general hint.

In general:

- Break after a comma.
- Break after an operator.
- Align the new line with the beginning of the expression on the previous line.

Additional comments on source layout are available in "C++ Naming Conventions".
In particular, namespace layout is discussed in :ref:`Rule 3-6 <style-guide-cpp-3-6>`.

.. _style-guide-cpp-include-files:

4.2 Include Files and Include Statements
----------------------------------------

.. _style-guide-cpp-4-9:

4-9. Header files MUST include a construction that prevents multiple inclusion.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The convention is an all uppercase construction of the full namespace, the file name and the ``h`` suffix.

For a file named :file:`AntennaRx.h`:

.. code-block:: cpp

   #ifndef LSST_ANTENNA_RX_H            // referring to file: AntennaRx.h
   #define LSST_ANTENNA_RX_H
    ...
   #endif // LSST_ANTENNA_RX_H

The construction is to avoid compilation errors.
The construction must appear in the top of the file (before the file header) so file parsing is aborted immediately and compilation time is reduced.

.. _style-guide-cpp-4-10:

4-10. Include statements SHOULD be sorted and grouped.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Groups are sorted by dependency (:file:`foo.h` before :file:`bar.h` if :file:`bar.h` depends on :file:`foo.h`) then alphabetically.
Leave an empty line between groups of include statements.
Place C includes first if any, then C++. Try to minimize dependencies and include the minimum required.

.. code-block:: cpp

   #include <fstream>
   #include <iomanip>
    
   #include "ui/MainWindow.h"
   #include "ui/PropertiesDialog.h"
    
   #include <Xm/ToggleB.h>
   #include <Xm/Xm.h>

In addition to showing the reader the individual include files, it also gives an immediate clue about the modules that are involved.
Include file paths must never be absolute.
Compiler directives should instead be used to indicate root directories for includes.

.. _style-guide-cpp-4-11:

4-11. Include statements SHOULD be located at the top of a file only.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the case of the implementation (``.cc`` file) of a template definition (``.h`` file) the include statement may be placed at the end of the including file.

Common practice.
Avoid unwanted compilation side effects by "hidden" include statements deep into a source file.

.. _style-guide-cpp-4-12:

4-12. There MUST be no unused include files listed in the source.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This avoids unwanted compilation side effects and reduces compilation time.

.. _style-guide-cpp-4-13:

4-13. ``using`` declarations and ``using`` directives MUST NOT be used in header files.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example ``using`` declaration:

.. code-block:: cpp

   using lsst::canbus::CanIo

Example using directive:     

.. code-block:: cpp

   using namespace lsst::canbus

A ``using`` declaration adds a name to the local scope.
This is bound to create a conflict.
Using directives are less likely to cause conflicts, since the compiler will force the user to qualify the name.
However, code is generally clearer and more precise if they are not used in header files.

See also :ref:`Appendix: On Using 'Using' <style-guide-cpp-using>`.

.. _style-guide-cpp-4-14:

4-14. There SHOULD be a header file for each library that has the name of the library and includes all of the include files necessary to define the public interface.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   #include "lsst/util.h"

Having a single include file per library makes it easier for application developers to ensure they include all the headers files they need.
It also puts the burden to keep the library header files up to date on the library developers where it belongs.
Applications can use these files, but library files should reference individual include files explicitly.

.. _style-guide-cpp-4-15:

4-15. Only system include file paths SHALL be delimited with ``<>``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``< >`` should be used to delimit include file paths only for products installed in the system locations.
Double quotes should be used to delimit those paths which refer to any code installed in an LSST distribution location; this includes the packages from the LSST repository and all 3rd party products installed in the LSST distribution tree.

.. code-block:: cpp

   #include "boost/any"
   #include "lsst/afw/image/image.h"
   #include "vw/image.h"

``<>`` includes search system paths before local paths.
It is slightly less efficient to use ``<>`` with non-system headers, which should only be searched in ``-I`` directories and the current directory.

.. _style-guide-cpp-statements:

5. Statements
=============

.. _style-guide-cpp-types:

5.1. Types
----------

.. _style-guide-cpp-5-1:

5-1. Types that are local to a single ``.cc`` file only SHOULD be declared inside that file.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For example, if a type is declared locally within a class body then the declaration goes within the ``.cc`` file, not the ``.h`` file.

Enforces information hiding.

.. _style-guide-cpp-5-2:

5-2. The parts of a class MUST be sorted ``public``, ``protected``, and ``private``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All sections must be identified explicitly.
Not applicable sections may be left out.
Member declarations should be done with data members first, then member functions, in each section:

.. code-block:: cpp

   class MyClass {
   public:
       int anInt;
       int doSomething();
   
   protected:
       float aFloat;
       float doSomethingElse();
   
   private:
       char _aChar;
       char doSomethingPrivately();
       ...
   }

The ordering is *most public first* so people who only wish to use the class can stop reading when they reach the protected/private sections.
There must be at most one ``public``, one ``protected`` and one ``private`` section in the ``class`` declaration.

.. _style-guide-cpp-5-2b:

5-2b. A class or struct definition MUST explicitly declare the privacy qualifier of its base classes.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A class or struct definition must explicitly declare the privacy qualifier of its base classes.

.. code-block:: cpp

   struct derived : public base {};
   class d : private b {};

Although C++ provides the above definitions as defaults, some compilers generate warnings if explicit privacy qualifiers are not specified.
This Rule will reduce unnecessary compiler warnings.

.. _style-guide-cpp-5-3:

5-3. Type conversions SHOULD be avoided as far as possible.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When required, type conversions MUST always be done explicitly using C++ style casts.
Never rely on implicit type conversion.

.. code-block:: cpp

   floatValue = static_cast<float>(intValue);     // YES!
   floatValue = intValue;                         // NO!
   floatValue = (float)intValue;                  // NO C-style casts!

By this, the programmer indicates that he is aware of the different types involved and that the mix is intentional.
If you find you are casting a lot, stop and think!
Maybe there is a better way to do things.

.. _style-guide-cpp-variables:

5.2. Variables
--------------

.. _style-guide-cpp-5-4:

5-4. Variables SHOULD be initialized where they are declared.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int i = 0;
   float aFloat = 0.0;
   int *i = 0          // 0 preferred pointer initialization, not NULL

This ensures that variables are valid at any time.
Sometimes it is impossible to initialize a variable to a valid value where it is declared:

.. code-block:: cpp

   int x, y, z;
   getCenter(&x, &y, &z);

In these cases it may be left uninitialized rather than initialized to some phony value.
Fixed phony values can be of use in debugging since they are consistent across runs, machines, builds and platforms.
See also :ref:`Rule 5-13 <style-guide-cpp-5-13>`.

.. _style-guide-cpp-5-5:

5-5. Multiple assignment SHOULD be used only with a constant type.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // OK:
   float a, b, c;
   a = b = c = 8675.309;
    
   // NOT OK:
   std::string a;
   int b;
   double c;
   a = b = c = 0;

Multiple assignment seems harmless when considering the first example.
However, while the second example is legal C++ (although it will generate compiler warnings), mixing types in assignment statements can lead to unintended results later.

.. _style-guide-cpp-5-6:

5-6. Variables MUST never have dual meaning.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enhance readability by ensuring all concepts are represented uniquely.
Reduce chance of error by side effects.

.. _style-guide-cpp-5-7:

5-7. Global variable use SHOULD be minimized.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In C++ there is no reason that global variables need to be used at all.
The same is true for global functions or file scope (static) variables.
See also :ref:`Rule 3-9 <style-guide-cpp-3-9>`.

.. _style-guide-cpp-5-8:

5-8. Non-constant and instance variables MUST be declared private.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Public members are allowed only if declared both ``const`` and ``static``.
The concept of C++ information hiding and encapsulation is violated by public variables.
If access to data members is required, then this must be provided through public or protected member functions.
The argument for public variables is generally one of efficiency.
However, by declaring the accessor and mutator functions in-line, efficiency can be regained.

One exception to this rule is when the class is essentially a data structure, with no behavior (equivalent to a C ``struct``).
In this case it is acceptable to make the class's instance variables public.
Note that ``struct``\ s are kept in C++ for compatibility with C only, and avoiding them increases the readability of the code by reducing the number of constructs used.
Use a class instead.

.. _style-guide-cpp-5-9:

5-9. Related variables of the same type MAY be declared in a common statement.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unrelated variables should not be declared in the same statement.

.. code-block:: cpp

   float x, y, z;
   float revenueJanuary, revenueFebruary, revenueMarch;

The common requirement of having declarations on separate lines is not useful in the situations like the ones above.
It enhances readability to group variables like this.

.. _style-guide-cpp-5-10:

5-10. The ``const`` keyword SHOULD be listed after the type name.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void f1(Widget const *v)     // NOT: void f1(const Widget *v)

This is for a mutable pointer to an immutable Widget.
Stroustrup points out one advantage to this order: you can read it from right to left i.e. "v is a pointer to a ``const Widget``."

Of course this is different than:

.. code-block:: cpp

   Widget * const p

Which is an immutable pointer to a mutable Widget.
Again, the right-to-left reading is pretty clear, so this and the above reinforce each other.

.. _style-guide-cpp-5-11:

5-11. Implicit test for ``0`` SHOULD NOT be used other than for boolean variables.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   if (nLines != 0)    // NOT:   if (nLines)

By using explicit test the statement gives an immediate clue of the type being tested.
It is common also to suggest that pointers shouldn't test implicit for 0 either, i.e. ``if (line == 0)`` instead of ``if (line)``.
The latter is regarded as such a common practice in C/C++ however that it can be used.

.. _style-guide-cpp-5-12:

5-12. Floats and doubles SHOULD NOT be tested for equality unless the comparison is to zero.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // NO
   if (value == 1.0)    // Subject to roundoff error
    
   // PREFERRED
   if (fabs(value - 1.0) < std::numeric_limits<float>::epsilon()) {
       ...
   }
    
   // OK in specific situations
   if (b == 0.0 && sigma2 == 0.0) {
       _sigma2 = 1.0;    //avoid 0/0 at center of PSF
   }

Round-off makes it difficult for two floating point numbers to be truly equal.
Always use greater than or less than.
A utility method like ``boolean closeEnough(value1,value2)`` may be useful for particular cases (e.g. to compare two images).

.. _style-guide-cpp-5-13:

5-13. Variables SHOULD be declared in the smallest scope possible.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Variables should be initialized when declared (and not declared before they can be initialized).

By keeping the operations on a variable within a small scope, it is easier to control the effects and side effects of the variable.
See also :ref:`Rule 5-4 <style-guide-cpp-5-4>`.

.. _style-guide-cpp-loops:

5.3. Loops
----------

.. _style-guide-cpp-5-14:

5-14. Loop variables SHOULD be declared in loop scope. Prefer pre- increment & decrement.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use of pre-increment and pre-decrement is preferred but not required.
Loop variables should be declared in loop scope when possible (it isn't possible if they have different types, such as ``ptr`` and ``x`` in the example).
It is permissible to advance more than one variable in the loop control part of the for if this makes logical sense (e.g. if you're advancing iterators through two arrays simultaneously, or needing to know the coordinates of a pixel iterator).

.. code-block:: cpp

   // YES:
   int sum = 0;
   double x = 0.0;
   for (iter ptr = vec.begin(), end = vec.end();  ptr != end; ++ptr, ++x) {
       sum += x*(*ptr);
   }
    
   // NO:
   int sum = 0;
   for (int i = 0; i < 100; i++) {
       sum += value[i];
   }

If you write ``iter++``, the method is required to make a copy of ``iter`` before incrementing it, as the return value is the old value.
If ``iter`` is a pointer this is cheap and probably inlined (and thus optimized away) but for complex objects it can be a significant cost.
The convention for STL code is to always pre-increment, and we should follow it.
See e.g. Meyers, *More Effective C++*, item 6.

This is only a recommendation; there are times when you do need the old value, and in that case postfix ++ is exactly what you want.

Increase maintainability and readability. Make it crystal clear what controls the loop and what the loop contains.

.. _style-guide-cpp-5-15:

5-15. Loop variables SHOULD be initialized immediately before the loop.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // YES:
   bool isDone = false;
   while (!isDone) {
       doSomething();
   }
    
   // NO: Don't separate loop variable initialization from use
   bool isDone = false;
   [....lots of code here...]
   while (!isDone) {
       doSomething();
   }

.. _style-guide-cpp-5-16:

5-16. 'do-while' loops SHOULD be avoided.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

'do-while' loops are less readable than ordinary 'while' loops and 'for' loops since the conditional is at the bottom of the loop.
The reader must scan the entire loop in order to understand the scope of the loop.

In addition, 'do-while' loops are not needed.
Any 'do-while' loop can easily be rewritten into a 'while' loop or a 'for' loop.
Reducing the number of constructs used enhance readability.

.. _style-guide-cpp-5-17:

5-17.
^^^^^

*Deleted.*

.. _style-guide-cpp-5-18:

5-18. The form ``while(true)`` SHOULD be used for infinite loops.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   while (true) {
       doSomething();
   }
 
   for (;;) { // NO!
       doSomething();
   }
 
   while (1) { // NO!
       doSomething();
   }

Testing against 1 is neither necessary nor meaningful.
The form ``for (;;)`` is not as apparent that this actually is an infinite loop.

.. _style-guide-cpp-conditionals:

5.4. Conditionals
-----------------

.. _style-guide-cpp-5-19:

5-19. Complex conditional expressions SHOULD be avoided. Introduce temporary boolean variables instead.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   if ((elementNo < 0) || (elementNo > maxElement)||
    
    
       elementNo == lastElement) {
       ...
   }

should be replaced by:

.. code-block:: cpp

   bool const isFinished = (elementNo < 0) || (elementNo > maxElement);
   bool const isRepeatedEntry = elementNo == lastElement;
   if (isFinished || isRepeatedEntry) {
       ...
   }

By assigning boolean variables to expressions, the program gets automatic documentation.
The construction will be easier to read and to debug.

.. _style-guide-cpp-5-20:

5-20. The nominal case SHOULD be put in the 'if' -part and the exception in the 'else' -part of an 'if' statement.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   int nChar;
   nChar = readFile(fileName);
   if (nChar > 0) {
       ...
   } else {
       ...
   }

Makes sure that the exceptions don't obscure the normal path of execution.
This is important for both the readability and performance.

.. _style-guide-cpp-5-21:

5-21. The conditional MAY be put on a separate line.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   //YES:
   if (isDone) {
     doCleanup();
   }
    
   // Also OK:
   if (isDone) doCleanup();

This is useful when using a symbolic debugger: when written on a single line, it is not apparent whether the test is true or not.

.. _style-guide-cpp-5-22:

5-22. Executable statements in conditionals MUST be avoided.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // NO!
   if ((fileHandle = open(fileName, "w"))) {
       ...
   }
    
   // YES:
   fileHandle = open(fileName, "w");
   if (fileHandle) {
       ...
   }

Conditionals with executable statements are just very difficult to read.
This is especially true for programmers new to C/C++.

.. _style-guide-cpp-methods-functions:

5.5. Methods and Functions
--------------------------

.. _style-guide-cpp-5-23:

5-23. Functions MUST always have the return value explicitly listed.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // YES:
   int getValue() {
       ...
   }
    
   // NO:
   getvalue() {
   }

If not explicitly listed, C++ implies int return value for functions.
A programmer must never rely on this feature, since this might be confusing for programmers not aware of this artifact.

.. _style-guide-cpp-5-23b:

5-23b. Unused method and function arguments MUST be unnamed.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void MyDerivedClass::foo(double /* scalefactor */) {
           // OK
   };
   
   void MyDerivedClass::foo(double) {
           // OK
   };

This is common in template specializations and derived methods, where a variable is needed for some cases but not all.
In order to remind the developer of the significance of the missing parameter, an in-line C comment may be used.
Although C++ allows omission of an unused argument's name, some compilers generate warnings if a named argument is not accessed.
This Rule will reduce unnecessary compiler warnings.

.. _style-guide-cpp-5-24:

5-24. Arguments that are of non-primitive types and will not be modified SHOULD be passed by ``const`` reference.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   void setWidget(Widget const &widget)

Passing by ``const`` reference when possible is much more efficient than passing large objects but also allows use of non-pointer syntax in the method.

.. _style-guide-cpp-5-24b:

5-24b. Smart pointers (such as ``shared_ptr``) should only be used as arguments if a reference or const reference cannot be used.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Examples of when a smart pointer argument is appropriate include when the pointer itself may be reset, when a null pointer is considered a valid input, and when the pointer (not the *pointee*) will be copied and held after after the function returns (as in a constructor or member function setter).
In all other cases, reference or ``const`` reference arguments should be used.
Motivation: it is difficult and sometimes expensive to create a smart pointer from a reference or plain value, so a smart pointer should not be required to call a function unless necessary.

.. _style-guide-cpp-5-25:

5-25. Class methods that do not update internal data nor return references/pointers to internal data MUST use the ``const`` label at the end of the signature.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   double getFactor() const;

This is required if one wants to manipulate constant versions of the object.

.. _style-guide-cpp-5-26:

5-26. All methods that return references/pointers to internal data MUST provide both a constant and non-constant version when appropriate.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``const`` version where possible.

.. code-block:: cpp

   Antenna& getAntenna(unsigned int i);
   Antenna const& getAntenna(unsigned int i) const;

The first example returns internal data.
If the class containing the function is constant, you can only call functions that have the trailing ``const`` label.
To call a function without the label is a compile-time error.
For example:

.. code-block:: cpp

   class Telescope {
       Antenna& getAntenna(unsigned int i);
   };
   
   const Telescope tel = obs.getTelescope();
   Antenna const& ant = tel.getAntenna(1);  // ERROR!

.. _style-guide-cpp-constructors:

5.6. Constructors and Destructors
---------------------------------

.. _style-guide-cpp-5-27:

5-27. Constructors taking one argument MUST be declared as ``explicit``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A default constructor must be provided. Avoid implicit copy constructors.

.. code-block:: cpp

   class Year {
   private:
       int y;
   
   public:
       explicit Year(int i) : y(i) {}
   };
   
   Year y1 = 1947;        // illegal
   Year y2 = Year(1947);  // OK
   Year y3(1947);         // Better
   
   // Example of unintended result and no error reported
   class String {
       int size;
       char *p;
   
   public:
       String(int sz);  // constructor and implicit conversions
   };

   void f() {
       String s(10);
       s = 100;  // programmer's typo not detected; 100 is
                 // converted to a String and then assigned to s!
   }

This avoids implicit type conversions (see :ref:`Rule 5-3 <style-guide-cpp-5-3>`).
The declaration of ``y1`` would be legal had ``explicit`` not been used.
This type of implicit conversion can result in incorrect and unintentional side effects.

.. _style-guide-cpp-5-28:

5-28. Destructors MUST NOT throw exceptions.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a violation of the C++ standard library requirements (see Stroustrup Appendix E.2).

.. _style-guide-cpp-5-29:

5-29. Destructors SHOULD be declared virtual in polymorphic base classes.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Paraphrasing Item 7 in Scott Meyer's **Effective C++**, 55 Specific Ways to Improve Your Programs and Designs:

   The rule for giving base classes virtual destructors applies only to base classes designed to allow the manipulation of derived class types through base class interfaces; such classes are known as 'polymorphic' base classes.
   Polymorphic base classes should declare virtual destructors.
   If a class has any virtual functions, it should have a virtual destructor.
   Classes not designed to be base classes or not designed to be used polymorphically should not declare virtual destructors.

In the example below, without a virtual destructor, the proper destructor will not be called.

.. code-block:: cpp

   class Base {
   public:
       Base() {}
       ~Base() {}  // Should be:   virtual ~Base() { }
   };
   
   class Derived : public Base {
   public:
       Derived() {}
       ~Derived() {}
   };
   
   void main() {
       Base *b = new Derived();
       delete b;  // Will not call Derived::~Derived() unless 'virtual ~Base()' was defined !
   }

.. _style-guide-cpp-misc:

5.7. Miscellaneous
------------------

.. _style-guide-cpp-5-30:

5-30. The use of magic numbers in the code SHOULD be avoided.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the number does not have an obvious meaning by itself, the readability is enhanced by introducing a named constant instead (see :ref:`Rule 3-3 <style-guide-cpp-3-3>`).
A different approach is to introduce a method from which the constant can be accessed.

.. _style-guide-cpp-5-31:

5-31. Floating point constants SHOULD always be written with decimal point and with at least one decimal.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   double total = 0.0;   // NOT: double total = 0;
   double speed = 3.0e8; // NOT: double speed = 3e8;
    
   double a;
   double b;
   ...
   double const SOME_GOOD_NAME = 10.0d;
   double sum = (a + b) * SOME_GOOD_NAME;

This emphasizes the different nature of integer and floating point numbers even if their values might happen to be the same in a specific case.
Although integers cannot be written using exponential notable (second example), for consistency we recommend using the decimal and trailing zero.
Also, as in the last example above, it emphasizes the type of the assigned variable (sum) at a point in the code where this might not be evident.

.. _style-guide-cpp-5-32:

5-32. Floating point constants SHOULD always be written with a digit before the decimal point.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   double gainOffset(0.5);   // NOT: double gainOffset(.5);

The number and expression system in C++ is borrowed from mathematics and one should adhere to mathematical conventions for syntax wherever possible.
Also, 0.5 is a lot more readable than .5; there is no way it can be mixed with the integer 5.

.. _style-guide-cpp-5-33:

5-33. ``goto`` SHOULD NOT be used.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

'Goto' statements violate the idea of structured code.
Only in some very few cases (for instance breaking out of deeply nested structures) should goto be considered, and only if the alternative structured counterpart is proven to be less readable.

.. _style-guide-cpp-5-34:

5-34. ``nullptr`` SHOULD be used instead of ``0`` and ``NULL``.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``nullptr`` is more explicit
* Template type deduction deduces the wrong, integral instead of pointer, type for ``0`` and ``NULL``
* Overload resolution of integral and pointer arguments picks the wrong overload with ``0`` and ``NULL``
* ``NULL`` is part of the standard C library, but is made obsolete in C++

See e.g. Meyers, *Effective Modern C++*, item 8.

.. _style-guide-cpp-5-35:

5-35. Signed int SHOULD be the preferred type for indices, even those in which a negative value is illegal.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   double d = new d[10];
   for (int i = 0; i < 10; i++) { d[i] = static_cast<double>(i); }

``unsigned int`` helps avoid index out of range exceptions at compile-time, but it throws you a curve when comparing ``int``\ s and ``unsigned int``\ s; requiring you to explicitly cast unsigned to signed.

.. _style-guide-cpp-5-36:

5-36. Exceptions MUST NOT be declared in method signatures, and all exceptions MUST be documented with the ``@throw`` tag.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use of ``throw`` in a signature does not encourage robust handling of exceptions.
The ramifications of declaring exceptions are spelled out in Stroustrup (3rd ed.) in section 14.6.

A few rules of thumb:

- A function declaration without a "throw" can throw any exception 
- A declaration containing a "throw" can only throw the listed exceptions. 
- Any exception not matching one of the declared exceptions (or a subclass of it) will be automatically rerouted to ``std::unexpected()``.
  The default implementation of this function is to call ``std::terminate()`` (which calls ``std::abort()``).
- ``Throw()`` may be used to indicate that no exceptions are expected to be thrown.

Exceptions thrown by a class should be apparent to a user of that class.
Hence the ``@throw`` requirement.

.. _style-guide-cpp-5-36b:

5-36b. Unused exception variables MUST be unnamed.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   try {
   } catch (ExceptionClass &) {  // OK
   };

Although C++ allows omission of the variable name, some compilers generate warnings if a named variable is not accessed.
This Rule will reduce unnecessary compiler warnings.

.. _style-guide-cpp-5-37:

5-37. ``#define`` statement use SHOULD be minimized.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // Preferred
   int const A_POWER_OF_TWO = 16;
    
   // NO
   #define A_POWER_OF_TWO 16

They have subtle side effects in debuggers and other tools.
For example, symbolic names for constants aren't visible to the debugger and require ``const`` variables.

.. _style-guide-cpp-5-38:

5-38. No code SHOULD be commented out; use a preprocessor directive to include or inhibit code use.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specifically for debug print statements, use the ``lsst::pex::log::Trace`` class.

.. code-block:: cpp

   #define DEBUG_IO 1
   #if defined(DEBUG_IO)
       [...statements...]
   #endif

.. _style-guide-cpp-5-39:

5-39. ``std::String`` class SHOULD be used rather than ``char *``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are developing in C++ not C, let's use the quite good standard string class.

.. _style-guide-cpp-5-40:

5-40. ``std::vector<Foo>`` SHOULD be used preferentially to array declaration (e.g. ``Foo[]``).
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is less prone to memory leaks (i.e. putting ``delete`` instead of ``delete[]``) and you don't need special pointers to work with it.
Again, let's use the good STL classes.

.. _style-guide-cpp-5-41:

5-41. ``using namespace`` SHOULD be minimized when defining symbols
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``using namespace`` should only be used for system library ``std``.

.. code-block:: cpp

   #include iostream.
   using namespace std;

It can be difficult to determine from where a particular symbol came.

.. _style-guide-cpp-5-42:

5-42. A definition or abbreviated namespace SHOULD be used when defining symbols
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is strongly recommended to use a definition or abbreviated namespace name, as in:

.. code-block:: cpp

   # Specify namespace explicitly in the definition
   lsst::foo::bar::myFunction(...) {...};
 
   # Use an abbreviation for the namespace
   namespace fooBar lsst::foo::bar;
   fooBar::myFunction(...) {...};

As a matter of policy, the module's developer should define the abbreviation to be used throughout the LSST codeset in the module's source file(s).
Uniformity of namespace abbreviation name across the full codeset makes code easier to quickly understand.
See :ref:`Rule 3-6 <style-guide-cpp-3-6>` for an almost equivalent Rule.

.. _style-guide-cpp-5-43:

5-43. Implementation-specific globals SHOULD go in namespace `*::detail`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes implementation-specific details need to be globally visible (i.e. can't be in the private part of a class, or be declared static or in an anon namespace in a single file).
For example, the fits i/o code in ``lsst::afw::image`` uses ``boost::gil`` internals but needs to be in a header file included by both :file:`Image.cc` and :file:`Mask.cc`; there are also Image traits classes.
In keeping with the boost convention, such global information should be consigned to a ``*::`` detail namespace (in this case, ``lsst::afw::image::detail``).
We should, of course, strive to minimize the amount of such information. 

5-44. The ``override`` specifier SHOULD be used whenever the intention is to override a function from a base class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add the ``override`` specifier to the member function declaration of any member function that should override
a function from a base class.
This ensures that the function is virtual and that it overrides a function from the base class.

Because ``override`` already implies ``virtual``, virtual should not be included as well.

.. code-block:: cpp

   class Base {
   public:
       virtual void foo();
   };
   
   class Derived : public Base {
   public:
       void foo() override;
   
       void bar();
   };

.. _style-guide-cpp-layout-comments:

6. Layout and Comments
======================

.. _style-guide-cpp-layout:

6.1. Layout
-----------

.. _style-guide-cpp-6-0:

6-0. Layout MAY be automated with clang-format using the LSST configuration.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The easiest way to comply with the :ref:`layout rules <style-guide-cpp-layout>` is to use `clang-format <http://clang.llvm.org/docs/ClangFormat.html>`_.

The intent is that all of the layout rules are compatible with clang-format using the LSST configuration; if any conflicts arise, this rule ensures that the clang-format result is permitted to be used notwithstanding any other.

See :ref:`here <using_clang_format>` for instructions.

.. _style-guide-cpp-6-1:

6-1. Multiple statements per line SHOULD NOT be used.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // NO!
   value = 10; setHex(value); doLess();

This is too hard to read and debug.
Always use separate lines.

.. _style-guide-cpp-6-2:

6-2. Basic indentation MUST be 4 spaces.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   for (i = 0; i < nElements; i++) (
       a[i] = 0;
   }

Indentation of 1 is too small to emphasize the logical layout of the code.
Indentation larger than 4 makes deeply nested code difficult to read and increases the chance that the lines must be split.
Choosing between indentation of 2, 3, and 4; 2 and 4 are the more common.
We require 4 because it is more visually obvious.

.. _style-guide-cpp-6-3:

6-3. Deeply nested code SHOULD be avoided.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code that is too deeply nested is hard to both read and debug.
One should replace excessive nesting with function calls.

.. _style-guide-cpp-6-4:

6-4. Block layout SHOULD be as illustrated in example 1 below (K&R, strongly recommended) not as in example 2 or 3.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // Example 1:
   while (!done) {        // Yes
       doSomething();
       done = moreToDo();
   }
   // Example 2:
   while (!done)
   {                      // No
       doSomething();
       done = moreToDo();
   }
   // Example 3:
   while (!done)
       {                    // NO
         doSomething();
         done = moreToDo();
       }

Example 3 introduces an extra indentation level which doesn't emphasize the logical structure of the code as clearly as example 1.
Example 2 adds an additional line without significant increase in readability.

.. _style-guide-cpp-6-5:

6-5. The class declarations SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   class SomeClass : public BaseClass1, public BaseClass2, private BaseClass3 {
   public:
       SomeClass() {}
   
   protected:
       ...
   
   private:
       ...
   };

Note that:

  - Any base class name should be on the same line as the subclass name,
    subject to the 110-column limit.
  - The ``public:``, ``protected:``, and ``private:`` keywords should not be indented.
  - Except for the first instance, these keywords should be preceded by a blank line.
    This rule is optional in small classes.
  - Do not leave a blank line after these keywords.
  - The ``public`` section should be first, followed by the ``protected`` and finally the ``private`` section.

.. _style-guide-cpp-6-6:

6-6. Function declarations MAY have any of the following three forms:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return type on the same line as function name, parameters on the same line if they fit.

.. code-block:: cpp

  ReturnType ClassName::functionName(Type parName1, Type parName2) {
      doSomething();
      ...
  }

If you have too much text to fit on one line:

.. code-block:: cpp

  ReturnType ClassName::reallyLongFunctionName(Type parName1, Type parName2,
                                               Type parName3) {
      doSomething();
      ...
  }

or if you cannot fit even the first parameter:

.. code-block:: cpp

  ReturnType LongClassName::reallyReallyReallyLongFunctionName(
          Type parName1, Type parName2, Type parName3) {  // 8 space indent
      doSomething();  // 4 space indent
      ...
  }

Some points to note:

- If you cannot fit the return type and the function name on a single line, break between them.
- If you break after the return type of a function declaration or definition, do not indent.
- The open parenthesis is always on the same line as the function name.
- There is never a space between the function name and the open parenthesis.
- There is never a space between the parentheses and the parameters.
- The open curly brace is always on the end of the last line of the function declaration, not the start of the next line.
- The close curly brace is either on the last line by itself or on the same line as the open curly brace.
- There should be a space between the close parenthesis and the open curly brace.
- All parameters should be aligned if possible.
- Default indentation is 4 spaces.
- Wrapped parameters have a 8 space indent.

Documentation for function arguments may be placed after the arguments, as shown here, or in the main documentation block using ``@param``.

.. code-block:: cpp

   /**
     * Documentation
     */
   void someMethod(type arg,   ///< Helpful comment about arg
                   type2 arg2  ///< Helpful comment about arg2
                   ) {
       ...
   }

.. _style-guide-cpp-6-7:

6-7. The 'if-else' class of statements SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   if (condition) {
       ...
   }
    
   if (condition) {
       ...
   } else {
       ...
   }
    
   if (condition) {
       ...
   } else if (condition) {
       ...
   } else {
       ...
   }

This is equivalent to the Sun recommendation. 

.. _style-guide-cpp-6-8:

6-8. A 'for' statement SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   for (initialization; condition; update) {
       statements;
   }

This follows from the general block rule above.

.. _style-guide-cpp-6-9:

6-9. Empty loops SHOULD be avoided. But if needed, empty loops MUST be clearly identified
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Empty loop bodies should use an empty pair of braces or continue, but not a single semicolon.

.. code-block:: cpp

  while (condition) {
      // Repeat test until it returns false.
  }

  for (int i = 0; i < kSomeNumber; ++i) {}  // Good - one newline is also OK.

  while (condition) continue;  // Good - continue indicates no logic.

This emphasizes that the statement is empty and it makes it obvious for the reader that this is intentional.

.. code-block:: cpp

  while (condition);  // Bad - looks like part of do/while loop.

.. _style-guide-cpp-6-10:

6-10. A ``while`` statement SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   while (condition) {
       statements;
   }

This follows from the general block rule above.

.. _style-guide-cpp-6-11:

6-11. A 'do-while' statement SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   do {                    // better yet: use a 'while (condition) {}'
       statements;
   } while (condition);

This follows from the general block rule above.

.. _style-guide-cpp-6-12:

6-12. A ``switch`` statement SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

  switch (condition) {
      case ABC:
          statements;
      // Fallthrough
  
      case DEF:
          statements;
          break;
  
      case XYZ:
          statements;
          break;
  
      default:
          statements;
          break;
  }

Note that each ``case`` keyword is indented 4 spaces relative to the ``switch`` statement as a whole and the statement blocks are also indented 4 spaces.
This makes the entire ``switch`` statement stand out.

The explicit 'Fallthrough' comment should be included whenever there is a ``case``` statement without a ``break`` statement.
Leaving the ``break`` out is a common error, and it must be made clear that it is intentional when it is not there.

.. _style-guide-cpp-6-13:

6-13. A 'try-catch' statement SHOULD have the following form:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

  try {
      statements;
  } catch (std::logic_error const& logicError) {
      statements;  // stifling the exception
  } catch (...) {
      statements;
      throw;
  }

This follows partly from the general block rule above.
The discussion about closing brackets for 'if-else' statements apply to the 'try-catch' statements.
If the ``catch`` clause is not going to re-throw the exception, a comment indicating so for clarity is a good idea.

.. _style-guide-cpp-6-14:

6-14. Single statement 'if-else' , 'for' or 'while' statements MUST only be written without brackets if on one line.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   if (condition) statement;
    
   while (condition) statement;
 
   for (initialization; condition; update) statement;

It is a common recommendation (Sun Java recommendation included) that brackets should always be used in all these cases.
Brackets are in general a language construct that groups several statements and thus by definition superfluous on a single statement.
However, the use of brackets in the above cases would make it trivial to add statements without error.

.. _style-guide-cpp-6-15:

6-15. The function return type SHOULD be put on the same line as the function name.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

  void MyClass::myMethod(void) {
      ...
  }

This is general practice.

.. _style-guide-cpp-6-15a:

6-15a. The minimum number of parentheses needed for syntactic correctness and readability SHOULD be used.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

  a = b(nSigmaToGrow * sigma + 0.5);    // YES
  a = b((nSigmaToGrow * sigma) + 0.5);  // NO
 
.. _style-guide-cpp-whitespace:

6.2. White Space
----------------

.. _style-guide-cpp-6-16:

6-16. The following white space conventions SHOULD be followed:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Assignment operators always have spaces around them.
- Other binary operators usually have spaces around them, but it's
  OK to remove spaces around ``*``, ``/`` and ``%``.
- Parentheses should have no internal padding.
- No spaces separating unary operators and their arguments.
- C++ reserved words should be followed by a white space.
- Commas should be followed by a white space.
- Colons should be surrounded by white space.
- Semicolons in for statements should be followed by a space character.

.. code-block:: cpp

   v = w * x + y / z;          // GOOD
   v = w*x + y/z;              // OK TOO
   v = w * (x + z);            // GOOD (no padding)
   while (true) {              // NOT:   while(true) ...
   doSomething(a, b, c, d);    // NOT:   doSomething(a,b,c,d);
   for (i = 0; i < 10; i++) {  // NOT:   for (i=0;i<10;i++){

Makes the individual components of the statements stand out.
Enhances readability.
It is difficult to give a complete list of the suggested use of whitespace in C++ code.
The examples above however should give a general idea of the intentions.

.. _style-guide-cpp-6-18:

6-18. Logical units within a block SHOULD be separated by one blank line.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enhance readability by introducing white space between logical units of a block.

.. _style-guide-cpp-6-19:

6-19. Methods SHOULD be separated by one blank line in .h files and two blank lines in .cc files.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By making the space larger than space within a method, the methods will stand out within the file.
However, this must be balanced with being able to see more of the code at a glance (one screen), which enhances readability through increased context.

.. _style-guide-cpp-6-20:

6-20.
^^^^^

*Deleted*

.. _style-guide-cpp-6-21a:

6-21a.
^^^^^^

*Deleted*

.. _style-guide-cpp-6-21b:

6-21b. Nested namespaces SHOULD be aligned left with each level of nesting on a new line.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The contents of namespaces are not indented.
The closing braces may all appear on one line and should be commented with the full nested namespace.

.. code-block:: cpp

  namespace lsst {
  namespace level1 {
  namespace level2 {

  class MyClass {
      // ...
  };

  }}}  // lsst::level1::level2

This is a common practice in the C++ community, until the proposed ``level1::level2::level3`` syntax is supported.

.. note::

  For compatibility with ``clang-format`` the closing braces may also each be on a line by themselves.

.. _style-guide-cpp-comments:

6.3. Comments
-------------

:doc:`../docs/cpp_docs` Documentation Standards contains most of the rules about comments.
A few detailed rules are listed here.

.. _style-guide-cpp-6-22:

6-22. Tricky code SHOULD not be commented but rewritten!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes tricky code is unavoidable, but if the choice is between being clever and being clear, choose clarity.

.. _style-guide-cpp-6-23:

6-23. All comments MUST be written in English.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Comments should not be about the obvious logic of the code, rather they should provide expanded information about why an action is being done, or some non-obvious result or side effect.
In an international environment English is the preferred language.

.. _style-guide-cpp-6-24:

6-24. Block comments MUST never be mixed with lines of code.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This:

.. code-block:: cpp

   /* Get an antenna reference
    * and if it is pointed at the Sun,
    * point it at the moon, after checking
    * to see if the moon is blue.
    */
   
   Antenna& ant = getAntenna("bima.ant1");
   bool moonIsBlue = (Planet.MOON.getColor() == "blue");
   if (ant.isPointedAt(Planet.SUN) && moonIsBlue) {
       ant.pointAt(Planet.MOON);
   } else {
       ant.pointAt(Planet.VENUS);
   }

Not this:

.. code-block:: cpp

   /* Get antenna reference */ Antenna& ant = getAntenna("bima.ant1");
   /* and if it is pointed  */ bool moonIsBlue = (Planet.MOON.getColor() == "blue");
   /* at the Sun, point it */  if (ant.isPointedAt(Planet.SUN) && moonIsBlue) {
   /* at the moon */               ant.pointAt(Planet.MOON);
   /* after checking */        } else {
   /* if the moon is blue */       ant.pointAt(Planet.VENUS);
                               }

Commenting in the second way makes code difficult to read and difficult to modify.

.. _style-guide-cpp-6-25:

6-25. Comments SHOULD be included relative to their position in the code.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: cpp

   // YES:
   while (true) {
       // Do something
       something();
   }
   
   // NOT:
   while (true) {
   // Do something now
       something();
   }

This maintains consistency by positioning the comment at the same level as the code being discussed.

.. _style-guide-cpp-legacy-code:

7. Legacy Code
==============

.. _style-guide-cpp-7-1:

7-1. All legacy code SHOULD have an interface definition specification that follows these rules.
------------------------------------------------------------------------------------------------

This rule is primarily in the case of writing wrapper classes for legacy code.
While it is not expected that we will bring the guts of all legacy code in line with the specifications in this document, it is important that public interfaces follow the rules of new code.

.. _style-guide-cpp-references:

8. References
=============

.. [Pound] Pound, M. W., Amarnath, N.S., & Teuben, P.J. CARMA C++ Programming Style Guidelines. Available online at http://www.mmarray.org/workinggroups/computing/cppstyle.html.

.. [Geosoft] Geosoft C++ Programming Style Guide. Available on-line at http://geosoft.no/development/cppstyle.html.

.. [Bridger2001] Bridger, Alan, Brooks, M., & Pisano, Jim. C++ Coding Standards, Revision 3, ALMA Computing Memo 0009 (Atacama Large Millimeter Array), 2001. Available on-line at https://science.nrao.edu/facilities/alma/aboutALMA/Technology/ALMA_Computing_Memo_Series/0009/2001-06-06.pdf

.. [McConnell2004] McConnell, Steve. Code Complete, 2nd Edition, (Redmond, WA: Microsoft Press), 2004. See http://www.stevemcconnell.com/cc.htm.

.. [Henricson1992] Henricson, M., & Nyquist, E. Programming in C++, Rules and Recommendations, (Alvsjo, Sweden: Ellemtel Telecommmunication Systems Laboratories), 1992. Available on-line at:
 http://www.mmarray.org/workinggroups/computing/ellemtel.pdf

.. [Eckel2000] Eckel, Bruce. Thinking in C++, (2nd Ed; Englewood Cliffs, NJ: Prentice Hall), 2000. Available on-line at: http://www.eckelobjects.com

.. [Hoff2008] Hoff, Todd. C++ Coding Standard, 2008. Available on-line at:
   http://www.possibility.com/Cpp/CppCodingStandard.htm

.. [Google] Google C++ Style Guide, 2017. Available on-line at:
   https://google.github.io/styleguide/cppguide.html

.. _style-guide-cpp-cpp-11-14:

Appendix: Policy on using C++11/14 Features
===========================================

The C++11 standard and the C++14 improvements to it bring a number of useful language features that make the resulting code more expressive, easier to read, and safer.
They are becoming well-implemented and widespread.
C++11/14 features supported by the default compiler provided with the oldest operating system distribution commonly used to install the LSST Stack, currently gcc 4.8.3, may be used at will in ``.cc`` implementation files.
They may be used in ``.h`` interface header files if:

- the usage is hidden from SWIG, either because they are not in method signatures or because they have been explicitly excluded with ``#ifndef`` SWIG, or
- SWIG has been empirically shown to work with the code (e.g. by successful buildbot run with appropriate Python-based test cases).

.. seealso::

   - :ref:`pipelines:source-install-redhat-legacy` from the `LSST Science Pipelines <https://pipelines.lsst.io>`__ documentation.
   - :doc:`/services/lsst-dev` provides :ref:`instructions for using devtoolset-3 <lsst-dev-tools>` to obtain a more modern GCC on LSST cluster machines.
   - C++11 compiler support matrix: http://wiki.apache.org/stdcxx/C++0xCompilerSupport.

.. _style-guide-cpp-using:

Appendix: On Using `Using`
==========================

C++ provides the ``using`` keyword for use in declarations and directives relating to namespaces.
This powerful capability can simplify and reduce the verbosity of code, but it can also lead to reliability and maintainability challenges when the source of non-local names is not obvious.

Using-declarations are of the form ``using N::Class;`` or ``using N::function;``.
These inject a name from a different namespace into the current namespace, where it may be used without qualification.

Using-directives are of the form ``using namespace N;``.
These inject all the names in the different namespace into the current namespace.

Coding convention :ref:`4-13 <style-guide-cpp-4-13>` bans using using-declarations and using-directives in header files. (It is incorrect about using-directives requiring qualification of names from the different namespace; this may be due to an incorrect analogy with the Python ``import`` statement.)

The LSST convention for ``.cc`` source files that are not included in header files is:

- Using-declarations are acceptable and appropriate for use when the class or function is to be referenced repeatedly.
- Using-directives are to be avoided except where ``N`` is std. This convention ensures that unfamiliar names will be properly namespace-qualified at least once in the file.
- Namespace renaming declarations of the form ``namespace Short = Long::Qualified::Name;`` are acceptable to reduce typing.
