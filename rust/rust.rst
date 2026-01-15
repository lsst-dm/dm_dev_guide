LSST Rust Development Guide
===========================

1. Introduction
---------------

This guide details the standards and best practices for writing Rust code within the LSST DM Stack and includes basic knowledge of the package.
Rust is being adopted to provide performance-critical components and leverage its memory safety features.
Of note, we are making use of Rust's memory safety in the sense of the design of the language.
This does not mean one can not use unsafe blocks where appropriate, but they should be used with due consideration and held to the same standards as where they are used elsewhere in Rust.
For example, unsafe blocks should be limited in scope to the smallest size needed to accomplish a unit of work.

There should be careful consideration when deciding to write new code in Rust.
The line between when something is simple enough and should be done in Python with a small performance hit versus written in Rust and bound to Python is hard to define and is left up to our 'empowering developers' directive for them to make the most informed decision.
This document assumes a basic understanding of Rust and the LSST DM Stack.

The *de facto* location, and reference implementation, of Rust within the LSST Science Pipelines is in a package called ``rubinoxide``.
This does not mean developers are not allowed to use Rust in another dedicated package, but unless there is a compelling reason to do so Rust code should be placed in ``rubinoxide``.
This guide defines the package layout of ``rubinoxide``.
Any other Rust based packages that are written should adhere to this as best as possible.

2. Rust Version
---------------

All LSST Rust code must be compatible with the standard Rust toolchain provided in the ``rubin-env`` conda environment.

3. Resources
------------

Unlike the C++ section of the guide, where the language has no clear community consensus or resources, we defer to standard published Rust resources for guidance on how to work with Rust.

* The `Rust Book <https://doc.rust-lang.org/book/>`_  is a good resource to find out information on the Rust language.
* `crates.io <https://crates.io/>`_ is where third party crates (libraries) are stored and distributed.
  This contains links to the documentation on each crate.
* Likewise the Python/Rust build system can be found at `maturin <https://www.maturin.rs/>`_
* Documentation for the Python binding engine PyO3 can be found `here <https://docs.rs/pyo3/latest/pyo3/>`__

4. Code Organization
--------------------

Unlike the package-centric organization often seen in Python, packages containing Rust code should be monolithic and not depend on other lsst packages.

* Top-Level Module: All Rust code will be bound to a single top-level module.
  This module will serve as the entry point for Python interaction.
* Functional Modules: Within this top-level module, create sub-modules representing distinct functionalities (e.g., image processing, coordinate transformations, data structures).
* Avoid Package-Specific Structure: Do not mirror the Python package structure in your Rust organization.
  Focus on logical groupings of functionality.

5. Python Interoperability
--------------------------

All Rust code intended for use within the LSST DM Stack must be exposed to Python via a well-defined API. This is achieved using the `pyO3`_ bindings.

* `pyO3`_ is Mandatory: `pyO3`_ is the only supported mechanism for exposing Rust functionality to Python.
* API Design: Rust-implemented Python functions and types should adhere to Python interface best practices instead of maximizing similarity to other internal Rust interfaces.
* Documentation: Thoroughly document your Python API using docstrings. Docstrings are written as doc comments in the Rust and are automatically translated to Python docstrings by pyO3. Doc strings should be written in the same ``numpydoc`` format as specified in `the Python section <python/numpydoc.rst>`__ of this Developer Guide.

6. Dependencies
---------------

Managing dependencies is crucial for maintaining a stable and reproducible build environment.

* RFC Process: All new Rust dependencies added to the Cargo.toml file must be approved via the LSST RFC (Request for Comments) process and the DM CCB (Change Control Board).
  This ensures that dependencies are vetted for licensing, security, and long-term maintainability.
* Dependency Versions: Pin dependency versions in Cargo.toml to ensure reproducible builds with exact pins.
  As the Cargo.lock file is also committed to git, this ensures all builds remain on equal footing.
  Incrementing versions should be done on a standalone commit after evaluating the effect on compiling and packaging.

7. Testing
----------

* Python Unit Tests: All Rust code with a Python interface must be tested via Python unit tests.
  This provides a consistent testing framework and leverages the existing LSST testing infrastructure.
  These tests should be placed in the ``tests`` top level directory.
* ``pytest``: Use ``pytest`` as the Python testing framework.
* For functionality that does not have a public Python api, or is not well covered by a Python api, or is difficult to appropriately test with a Python unit test, Rust unit tests may be written using the standard Rust unit test infrastructure.
  Generally avoid Rust unit tests on any code that is wrapped with `pyO3`_.
* Import Rust Modules: Python tests should import the Rust modules (exposed via `pyO3`_) and exercise their functionality.
* Comprehensive Coverage: Strive for high test coverage to ensure that all critical code paths are tested.
* Integration Tests: In addition to unit tests, consider integration tests to verify the interaction between Rust components and other parts of the LSST DM Stack.

8. Code Style and Formatting
----------------------------

Consistent code style improves readability and maintainability.

* `rustfmt`_: One must use `rustfmt`_ to automatically format your Rust code, or otherwise produce output that is the same as would have been produced with `rustfmt`_.
* `Clippy`_: Use Clippy to lint your Rust code and identify potential issues. Not every suggestion from Clippy must be adopted, but all should be carefully considered. Suggestions which make code conform to community standards should only be skipped with good justification.
* Documentation Comments: Write clear and concise documentation comments for all public functions and data structures.
* To the extent possible, make APIs that will be public to Python feel exactly as if they are written in Python.

9. Logging
-----------

Logging should be done using the `log`_ crate, and accompanying macros.
The standard ``rubinoxide`` package initializes the ``pyo3_log`` crate to forward all logs through to the Python log handler to the appropriate log level.

10. Don'ts
----------

* Do not use implicit multithreading in Rust.
* Do not introduce any cross package Rust bindings that transit through Python (do not emulate current C++ practice).
* As mentioned above, do not arrange module structure according to lsst packages. Write modules by related functionality.

11. Build and management system integration
-------------------------------------------

* Rust packages should be built using ``maturin``, which manages the complexities of compiling and bundling cargo products.
* Cargo additionally is to be used manage dependencies and run Rust level tests.
* ``pip`` is used as the mechanism to locally deploy the wheels created by ``maturin``.
* ``pytest`` is used to run Python level unit tests.
* Coordinating these scripts for the developer is a ``Makefile``.
* The ``Makefile`` supports ``build`` and ``test`` modes independently (as well as an ``all`` mode) so authors can more quickly iterate in development.

.. _rustfmt: https://github.com/rust-lang/rustfmt
.. _Clippy: https://github.com/rust-lang/rust-clippy
.. _pyO3: https://pyo3.rs/
.. _log: https://docs.rs/log/latest/log/
