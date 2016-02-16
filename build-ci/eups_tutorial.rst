#############
EUPS Tutorial
#############

`EUPS <https://github.com/RobertLuptonTheGood/eups>`_\ —Extended Unix Product
System—is a tool for managing multiple versions of interdependent software
packages.

The LSST stack consists of many separate packages: ``lsst_apps`` alone depends
on more than 50; other top level packages bring in more. The relationships
between these packages can be complex ("``lsst_apps`` version ``X`` depends on
``afw`` version ``Y`` which depends on ``boost`` version at least ``Z`` but no
greater than ``Z+N``"). Furthermore, it's convenient to keep multiple versions
of the packages installed and available simultaneously—the developer likely
wants to develop targeting today's version of the stack, while fixing bugs in
yesterday's; the scientist to run the latest versions of the algorithms while
also being able to reproduce their results from last year. EUPS aims to make
this situation tractable.

Here, we provide a tutorial-based introduction to basic EUPS functionality.

.. _eups-tutorial-getting-started:

Getting Started
===============

Having installed the Stack, you already have EUPS available. However, its
internal database is pre-populated with knowledge about the Stack packages you
have installed. For simplicity, we begin by re-targeting it by setting the
:envvar:`EUPS_PATH` variable::

   % . ${STACK_PATH}/loadLSST.bash
   % eups path
   ${STACK_PATH}

   % unsetup lsst
   % export EUPS_PATH="/tmp/eups_demo"
   % mkdir -p ${EUPS_PATH}/ups_db
   % eups path
   /tmp/eups_demo

Observe that the majority of EUPS commands follow pattern :command:`eups
<verb> <options>` (reminiscent of Git, for example). :command:`(un)setup` is
the exception.

.. _eups-tutorial-building-simple-product:

Building and Using a Simple EUPS Product
========================================

Create a demo product called `a`
--------------------------------

Let's create a simple Python package, called ``a``, and have EUPS manage it as
a **product**. First create a directory structure::

   % mkdir -p ${EUPS_PATH}/a/v1/python
   % mkdir -p ${EUPS_PATH}/a/v1/bin

Create a file :file:`${EUPS_PATH}/a/v1/python/a.py` with content:

.. code-block:: python

   __VERSION__ = 1

and create a file :file:`${EUPS_PATH}/a/v1/bin/a` with content:

.. code-block:: python

   #!/usr/bin/env python

   import a

   if __name__ == "__main__":
       print("Package a with version %d" % (a.__VERSION__,))

Adding an EUPS table file
-------------------------

For the ``a`` product to be usable, we need EUPS to ensure that

- :file:`a.py` is on :envvar:`PYTHONPATH` (so that we can import it); and
- :file:`bin/a` is on :envvar:`PATH` (so that we can execute it).

We configure EUPS to this through a *table file*, located in a product's
:file:`ups` directory. First create that directory in the Python package::

   mkdir -p ${EUPS_PATH}/a/v1/ups

and create a :file:`${EUPS_PATH}/a/v1/ups/a.table` with the following contents:

.. code-block:: text

  envPrepend(PYTHONPATH ${PRODUCT_DIR}/python)
  envPrepend(PATH ${PRODUCT_DIR}/bin)

When we ask EUPS to enable ("set up") the product, it will manipulate the
environment according to these commands (``envPrepend``) in the table file. Of
course, pre-pending things to environment variables isn't all it can do: we'll
see some more commands shortly.

Declaring the product to EUPS
-----------------------------

We next *declare* the product to EUPS, causing it to read the table file and
record information about the product in its database. The general form of the
declaration command is::

   % eups declare [PRODUCT_NAME} [VERSION] -r [PATH]

In this case we execute::

   % eups declare a v1 -r ${EUPS_PATH}/a/v1

Having declared the product, we can query the EUPS database for the list of all
products it is tracking::

   % eups list
   a                      v1                  current

And then we can set up the product using the :command:`setup` command::

   % setup a

   % echo $PATH
   /tmp/eups_demo/a/v1/bin:…

   % eups list -s # Only lists products which have been set up.
   a                     v1                 current setup

Use the command provided by the ``a`` package::

   % a
   Package a with version 1

And tear it down with :command:`unsetup`::

   % unsetup a

After :command:`unsetup`, the :command:`a` command is not longer in your
:envvar:`PATH`::

   % a
   -bash: a: command not found

.. _eups-tutorial-multiple-versions:

Managing Versions of Products
=============================

Where EUPS truly becomes useful is when we have multiple versions of a product
that we want to switch between.

Normally we get different versions of a package from Git history, but here
we'll simulate that by copying :file:`${EUPS_PATH}/a/v1` to
:file:`${EUPS_PATH}/a/v2`::

   % cp -R ${EUPS_PATH}/a/v1 ${EUPS_PATH}/a/v2

In :file:`${EUPS_PATH}/a/v2/python/a.py`, update the module's ``__VERSION__``:

.. code-block:: python

   __VERSION__ = 2

We then declare it to EUPS as before::

   % eups declare a v2 -r ${EUPS_PATH}/a/v2

   % eups list
   a                     v1                 current
   a                     v2

Note that EUPS is now tracking two versions of ``a``. Note that ``v1`` is marked as
``current`` to indicate this is the version we get if we :command:`setup a` without
further qualification::

   % setup a

   % a
   Package a with version 1

   % unsetup a

   % setup a v2

   % a
   Package a with version 2

.. _eups-tutorial-tags:

Tags
====

The ``current`` moniker we encountered above is just one example of a *tag*:
a name associated with a particular combination of products and versions. EUPS
defines some standard tags by default::

   % eups tags
   current latest stable user:${username}

``current``
   If you don’t do anything "clever," you’ll get the version tagged current when
   you set up a product.

``latest``
   Reserved for special purposes: users should not interact with this tag.

``stable``
   You can apply this tag at will; you might find it semantically meaningful.

``user:${username}``
   Personal tag; apply at will. Omit the "user" when referring to it.

We can apply tags to particular versions using :command:`eups declare` and
then pass them as arguments to :command:`(un)setup`::

   % eups list
   a                     v1                current
   a                     v2

   % eups declare -t stable a v1

   % eups declare -t ${USER} a v2

   % eups list
   a                     v1                current stable
   a                     v2                ${USER}

   % setup -t ${USER} a

   % a
   Package a with version 2

   % setup a

   % a
   Package a with version 1

Note that when we don't specify a tag, we default to ``current``.

.. _eups-tutorial-dependencies:

Dependent Products
==================

Another core function of EUPS is coordinating multiple packages. We'll see how
this works by creating a product ``b`` that has a declared dependency on
product ``a``.

First, create the product's directory structure::

   mkdir -p ${EUPS_PATH}/b/v1/bin
   mkdir -p ${EUPS_PATH}/b/v1/ups

Write the contents of :file:`${EUPS_PATH}/b/v1/bin/b`:

.. code-block:: python

   #!/usr/bin/env python

   import a

   if __name__ == "__main__":
       print("Package b is using a version %d" % (a.__VERSION__,))

Note that ``b`` imports ``a``: it is not possible to use ``b`` unless ``a`` has
already been set up. We specify this dependency in the table file
(:file:`${EUPS_PATH}/b/v1/ups/b.table`) using the ``setupRequired`` command:

.. code-block:: text

   setupRequired(a)
   envPrepend(PATH, ${PRODUCT_DIR}/bin)

When we :command:`eups declare` and :command:`setup` ``b``, ``a`` is
automatically loaded when required. Using the ``-v`` ("verbose") option with
:command:`setup` makes this obvious::

   % eups declare b v1 -r ${EUPS_PATH}/b/v1

   % eups list
   a                     v1            current
   a                     v2
   b                     v1            current

   % setup -v b
   Setting up: b                               Flavor: Darwin X86  Version: v1
   Setting up: |a                              Flavor: Darwin X86  Version: v1

   % b
   Package b is using a version 1

Versioned Dependencies
======================

Since we weren't specific about the version of ``a`` required by ``b``, EUPS
just gives us the version tagged ``current``. We could override this in
``b``’s table file if required::

   setupRequired(a v2)

Sometimes, it's not enough to simply hard-code a versioned dependency in
advance. For example, when dealing with compiled code, the version required may
depend on the :abbr:`ABI (Application Binary Interface)` baked in at build
time. EUPS provides the :command:`eups expandtable` command to annotate a table
file with the detailed state of the environment; :command:`eups expandtable`
can be run at build time and the results stored for later use. For example::

   % eups expandtable ups/b.table
   if (type == exact) {
      setupRequired(a               -j v2)
   } else {
       setupRequired(a v2 [>= v2])
   }
   envPrepend(PATH, ${PRODUCT_DIR}/bin)

Passing the ``--exact`` flag to :command:`setup` on the command line will set
up only the exact versions that are specified in the expanded table file;
otherwise, EUPS assumes that any greater version is equally acceptable. For
example, if we added a ``v3`` of ``a`` and removed ``v2``, an ``--exact``
setup would baulk::

   % eups list
   a                     v1
   a                     v3
   b                     v1                 current

   % setup --exact b
   setup: in file /tmp/eups_demo/b/v1/ups/b.table: Product a v2 not found

   % setup -v --inexact b
   Setting up: b                               Flavor: Darwin X86  Version v1
   Setting up: |a                              Flavor: Darwin X86  Version v3

Version Resolution
==================

:ref:`Earlier <eups-tutorial-tags>` we saw that we get the version tagged
``current`` unless we do something "clever." So what counts as clever?

In fact, EUPS decides which version to load based on a user-configurable
"Version Resolution Order" or VRO (analogous to Python's :abbr:`MRO (Method
Resolution Order)`). The default VRO is::

   % eups vro
   type:exact commandLine version versionExpr current

This says:

- Set things up in ``exact`` mode;
- If possible, set up the version specified on the command line;
- Otherwise, set up an explicit version specified elsewhere (e.g. in the table
  file);
- Otherwise, choose a version based on an expression (e.g. >= 2.0) specified
  in the table file or elsewhere;
- Otherwise, set up the version tagged ``current``.

It is possible for users to customize the VRO, but this is only necessarily in
exceptional cases and is outside the scope of this guide.

.. _eups-tutorial-lsst-stack:

The LSST Stack
==============

We can now apply all the above to understand the structure of the LSST Stack.
:command:`eups list` will tell us about all the packages known to our copy of
the Stack, including tags and versions::

   % . ${STACK_PATH}/loadLSST.bash
   % eups list
   activemqcpp           10.1           2015_05 b1327 b1326 […]
   […]

Be aware that there are generally many packages and many, many tags,
corresponding to different :doc:`CI <ci_overview>` runs, official releases,
and so on.

Setting up the ``lsst_apps`` product will, by default, give us the ``current``
version, and pull in all the products upon which it depends::

   % setup -v lsst_apps
   Setting up: lsst_apps                       Flavor: DarwinX86  Version: 11.0+3
   Setting up: |meas_deblender                 Flavor: DarwinX86  Version: 11.0+3
   […]

It's equally possibly to request other versions or tags of ``lsst_apps`` when
required, and to apply tags like ``current`` or the ``user:`` tag to versions
of particular interest for convenient access.

It's occasionally informative to inspect the expanded table files of the
installed products to see how version information was baked into the build::

   % more ${LSST_APPS_DIR}/ups/lsst_apps.table
   if (type == exact) {
      setupRequired(meas_deblender  -j 11.0+3)
      setupRequired(utils           -j 11.0-1-g47edd16)
   […]

.. _eups-tutorial-eups-distrib:

:command:`eups distrib`
=======================

:command:`eups distrib` is a package distribution mechanism which provides a
convenient way of installing and updating the LSST Stack. It is distinct from
the core EUPS functionality described above, but is closely integrated and
shares many concepts.

:command:`eups distrib` reads details about available packages from a remote
server. The appropriate location for finding LSST software is
http://sw.lsstcorp.org/eupspkg. We can use :command:`eups distrib list` to
list available software, and :command:`eups distrib install` to install it::

   % eups distrib path
   http://sw.lsstcorp.org/eupspkg

   % eups distrib list lsst_apps
   lsst_apps            generic    8.0.0.1+2
   lsst_apps            generic    8.0.0.1+3
   […]

   % eups distrib install -t v11_0 lsst_apps

Note that :command:`eups distrib list` does not list tags, even though
:command:`eups distrib install` accepts a tag as a command line option (``-t
v11_0``). The most convenient way to see a list of available tags is to visit
the distribution server (https://sw.lsstcorp.org/eupspkg/tags/) in a web
browser.

.. _eups-tutorial-more-info:

Further Information
===================

EUPS is developed outside the LSST Stack in an `independent GitHub
repository`_ which provides its own `issue tracker`_. However, it is important
to track problems with installing the Stack in :ref:`JIRA <workflow-jira>`,
even if they are already known in the EUPS tracker.

EUPS ships with a `manual`_, but it can be hard to read when getting started.
There are also some tips on the `old LSST wiki`_.

.. _independent GitHub repository: https://github.com/RobertLuptonTheGood/eups
.. _issue tracker: https://github.com/RobertLuptonTheGood/eups/issues
.. _manual: https://github.com/RobertLuptonTheGood/eups/blob/master/doc/eups.tex
.. _old LSST wiki: https://dev.lsstcorp.org/trac/wiki/EupsTips
