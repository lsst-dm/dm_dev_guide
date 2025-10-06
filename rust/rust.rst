LSST Rust Development Guide
===========================

This document outlines the guidelines for developing Rust code within the LSST (Large Synoptic Survey Telescope) DM (Data Management) Stack. It’s designed to complement existing Python and C++ development guides and ensure consistency across the project.  
This guide is a living document and will be updated as needed. Please provide feedback and suggestions to help improve it.

1. Introduction
---------------

This guide details the standards and best practices for writing Rust code within the LSST DM Stack and includes basic knowledge of the package. Rust is being adopted to provide performance-critical components and leverage its memory safety features. This document assumes a basic understanding of Rust and the LSST DM Stack.

2. Rust Version
---------------

All LSST Rust code must be compatible with the standard Rust toolchain supported by the LSST DM Stack as provided in the conda environment. Specific versions will be maintained and announced through the standard LSST communication channels.

3. Resources
------------

* The `Rust Book <https://doc.rust-lang.org/book/>`_  is a good resource to find out information on the rust language.  
* `crates.io <https://crates.io/>`_ is where third party crates (libraries) are stored and distributed. This contains links to the documentation on each crate.  
* While knowledge of this is not needed by most developers, the `cargo book <https://doc.rust-lang.org/cargo/>`_ may be useful for any obscure packaging issues.  
* Likewise the python/rust build system can be found at `maturin <https://www.maturin.rs/>`_
* Documentation for the python binding engine PyO3 can be found `here <https://docs.rs/pyo3/latest/pyo3/>`_

4. Code Organization
--------------------

Unlike the package-centric organization often seen in Python, Rust code within the LSST DM Stack should be organized by functionality. This promotes code reuse and maintainability. 
* Top-Level Module: All Rust code will be bound to a single top-level module. This module will serve as the entry point for Python interaction. If for some reason independent repos are needed they must first be proposed in an RFC and will adhear otherwise to what is in this guide. 
* Functional Modules: Within this top-level module, create sub-modules representing distinct functionalities (e.g., image processing, coordinate transformations, data structures).
* Avoid Package-Specific Structure: Do not mirror the Python package structure in your Rust organization. Focus on logical groupings of functionality.

5. Python Interoperability
--------------------------

All Rust code intended for use within the LSST DM Stack must be exposed to Python via a well-defined API. This is achieved using the `pyO3`_ bindings.  
* `pyO3`_ is Mandatory: `pyO3`_ is the only supported mechanism for exposing Rust functionality to Python.  
* API Design: Carefully design your Python API to be intuitive and consistent with existing LSST Python interfaces.  
* Documentation: Thoroughly document your Python API using docstrings. Docstrings are written as doc comments in the rust and are automatically translated to python docstrings by pyO3. Doc strings should be written in the same numpydoc format as specified in the python section of the devguide.

6. Dependencies
---------------

Managing dependencies is crucial for maintaining a stable and reproducible build environment.  
* RFC Process: All new Rust dependencies added to the Cargo.toml file must be approved via the LSST RFC (Request for Comments) process. This ensures that dependencies are vetted for licensing, security, and long-term maintainability.  
* Dependency Versions: Pin dependency versions in Cargo.toml to ensure reproducible builds.  
* Minimal Dependencies: Strive to minimize the number of dependencies to reduce build times and potential conflicts.

7. Testing
----------

Robust testing is essential for ensuring the quality and reliability of the LSST DM Stack.  
Python Unit Tests: All Rust code must be tested via Python unit tests. This provides a consistent testing framework and leverages the existing LSST testing infrastructure.  
pytest: Use pytest as the testing framework.  
Import Rust Modules: Python tests should import the Rust modules (exposed via `pyO3`_) and exercise their functionality.  
Comprehensive Coverage: Strive for high test coverage to ensure that all critical code paths are tested.  
Integration Tests: In addition to unit tests, consider integration tests to verify the interaction between Rust components and other parts of the LSST DM Stack.

8. Code Style and Formatting
----------------------------

Consistent code style improves readability and maintainability.  

* `rustfmt`_: Use rustfmt to automatically format your Rust code.  
* `Clippy`_: Use Clippy to lint your Rust code and identify potential issues.  
* Documentation Comments: Write clear and concise documentation comments for all public functions and data structures.  
* To the extent possible, make apis that will be public to python feel exactly as if they are written in python.

9. Testing
----------

Test code in the most appropriate way possible.  

* If possible write tests against the public python api using pytest. These tests should be placed in the **tests** top level directory.  
* For functionality that does not have a public python api, or is not well covered by a python api, or is difficult to appropriately test with a python unit test rust unit tests may be written using the standard rust unit test infrastructure. Genreally avoid a rust until test on any code that is wrapped with pyo3.

10. Logging
-----------

Logging should be done using the log crate, and accompanying macros. The standard rubinoxide package initializes the pyo3_log crate to forward all logs through to the python log handler to the approprate log level.

11. Don'ts
----------

* Do not use implicit multithreading in rust  
* Do not introduce any cross package rust bindings that transit through python aka how we use c++ now.  
* As mentioned above, do not arange module structure according to lsst packages. Write modules by related functionality.

12. Build and management system integration
-------------------------------------------

* Rust packages should be built using maturin, which manages the complexities of compiling and bundling cargo products.  
* Cargo additionally is to be used manage dependencies and run rust level tests.  
* pip is used as the mechanism to locally depoly the wheels created by maturin  
* pytest is used to run python level unit tests  
* coordinating these scripts for the developer is a Makefile

.. _rustfmt: https://github.com/rust-lang/rustfmt  
.. _Clippy: https://github.com/rust-lang/rust-clippy
.. _pyO3: https://pyo3.rs/
