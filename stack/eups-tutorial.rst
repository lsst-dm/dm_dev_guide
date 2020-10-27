#############
EUPS Tutorial
#############

`EUPS`_\—"Extended Unix Product System"—is a tool for managing multiple
versions of interdependent software packages.

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
Throughout, we use the ``%`` symbol to represent a shell prompt (i.e., it
precedes commands one might type into a terminal).

.. _EUPS: https://github.com/RobertLuptonTheGood/eups

Getting Started
===============

Having installed the stack, you already have EUPS available. However, its
internal database is pre-populated with knowledge about the stack packages you
have installed. For simplicity, we begin by re-targeting it by setting the
``EUPS_PATH`` variable::

   % . ${STACK_PATH}/loadLSST.bash
   % eups path
   ${STACK_PATH}
   % unsetup lsst
   % export EUPS_PATH="/tmp/eups_demo"
   % mkdir -p ${EUPS_PATH}/ups_db
   % eups path
   /tmp/eups_demo

Observe that the majority of EUPS commands follow the pattern :command:`eups
<verb> <options>` (reminiscent of Git, for example). :command:`(un)setup` is
the exception.

Building and Using a Simple EUPS Product
========================================

Assume we have a trivial software package — ``a`` — which we want to have EUPS
manage as a "product". Our package is about as simple as they come::

   % cat python/a.py
   __VERSION__ = 1

   % cat bin/a
   #!/usr/bin/env python

   import a

   if __name__ == "__main__":
       print("Package a with version %d" % (a.__VERSION__,))

This is stored in :file:`${{EUPS_PATH}}/a/v1`.

Adding an EUPS Table File
-------------------------

In order to make our package usable, we need EUPS to ensure:

- That :file:`a.py` is on ``PYTHONPATH`` (so that we can import it);
- That :file:`bin/a` is on ``PATH`` (so that we can execute it).

We communicate this to EUPS through a *table file*, located in the
:file:`eups` directory within the product (in this case,
:file:`${{EUPS_PATH}}/a/v1/ups/a.table`). Our file contains::

  % cat ups/a.table
  envPrepend(PYTHONPATH ${PRODUCT_DIR}/python)
  envPrepend(PATH ${PRODUCT_DIR}/bin)

When we ask EUPS to enable ("set up") the product, it will manipulate the
environment in the obvious way. Of course, pre-pending things to environment
variables (``envPrepend``) isn't all it can do: we'll see some more commands
shortly.

Declaring the Product to EUPS
-----------------------------

We next *declare* the product to EUPS, causing it to read the table file and
record information about the product in its database. The general form of the
declaration command is::

   % eups declare [PRODUCT_NAME] [VERSION] -r [PATH]

In this case we execute::

   % eups declare a v1 -r ${EUPS_PATH}/a/v1

Having thus declared the product, we can query the EUPS database for the list
of all products it is tracking::

   % eups list
   a                      v1                  current

And then we can set up the product using the :command:`setup` command, use it,
and tear it down again with :command:`unsetup`::

   % setup a

   % echo $PATH
   /tmp/eups_demo/a/v1/bin:…

   % a
   Package a with version 1

   % eups list -s # Only lists products which have been set up.
   a                     v1                 current setup

   % unsetup a

   % a
   -bash: a: command not found

Managing Versions of Products
=============================

Being able to :command:`(un)setup` a single version of a single product is of
limited practical utility. However, EUPS lets us easily switch between
different versions of the same product. We construct ``v2`` of ``a`` by simply
copying the source to :file:`${{EUPS_PATH}}/a/v2` and incrementing the version
number in the source. We then declare it to EUPS as before::

   % eups declare a v2 -r ${EUPS_PATH}/a/v2

   % eups list
   a                     v1                 current
   a                     v2

Note that EUPS is now tracking two versions of ``a``. ``v1`` is marked as
``current``: this indicates the version we get if we :command:`setup a`
without further qualification::

   % setup a

   % a
   Package a with version 1

   % unsetup a

   % setup a v2

   % a
   Package a with version 2

.. _tags:

Tags
====

The ``current`` moniker we encountered above is just one example of a *tag*:
a name associated with a particular combination of products and versions. EUPS
defines some standard tags by default::

   % eups tags
   current latest stable user:${username}

``current``
   If you don’t do anything "clever", you’ll get the version tagged current when
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

   $ eups declare -t ${USER} a v2

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

Dependent Products
==================

Frustrated by the limitations of ``a``, we now want to augment it with an
additional product: ``b``. Again, the code is quite straightforward::

   % cat bin/b
   #!/usr/bin/env python

   import a

   if __name__ == "__main__":
       print("Package b is using a version %d" % (a.__VERSION__,))

Note, though, that ``b`` imports ``a``: it is not possible to use ``b`` unless
``a`` has already been set up. We specify this dependency in the table file
using the :command:`setupRequired` command::

   % cat ups/b.table
   setupRequired(a)
   envPrepend(PATH, ${PRODUCT_DIR}/bin)

We can :command:`declare` and :command:`setup` ``b``, and ``a`` is
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
``b``'s table file if required::

   setupRequired(a v2)

Sometimes, it's not enough to simply hard-code a versioned dependency in
advance. For example, when dealing with compiled code, the version required
may depend on the :abbr:`ABI (Application Binary Interface)` baked in at build
time. EUPS provides the :command:`eups expandtable` command command to
annotate a table file with the detailed state of the environment: it can be
run at build time and the results stored for later use. For example::

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
setup would balk::

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

:ref:`Earlier <tags>` we saw that we get the version tagged ``current`` unless
we do something "clever". So what counts as clever?

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
- Otherwise, choose a version based on an expression (e.g., ``>= 2.0``) specified
  in the table file or elsewhere;
- Otherwise, set up the version tagged ``current``.

It is possible for users to customize the VRO, but this is only necessarily in
exceptional cases and is outside the scope of this guide.

The LSST Stack
==============

We can now apply all the above to understand the structure of the LSST stack.
:command:`eups list` will tell us about all the packages known to our copy of
the stack, including tags and versions::

   % . ${STACK_PATH}/loadLSST.bash
   % eups list
   activemqcpp           10.1           2015_05 b1327 b1326 […]
   […]

Be aware that there are generally many packages and many, many tags,
corresponding to different :doc:`CI </jenkins/getting-started>` runs, official releases,
and so on.

Setting up the ``lsst_apps`` product will, by default, give us the ``current``
version, and pull in all the products upon which it depends::

   % setup -v lsst_apps
   Setting up: lsst_apps                       Flavor: DarwinX86  Version: 11.0+3
   Setting up: |meas_deblender                 Flavor: DarwinX86  Version: 11.0+3
   […]

It's equally possible to request other versions or tags of ``lsst_apps`` when
required, and to apply tags like ``current`` or the ``user:`` tag to versions
of particular interest for convenient access.

It's occasionally informative to inspect the expanded table files of the
installed products to see how version information was baked into the build::

   % more ${LSST_APPS_DIR}/ups/lsst_apps.table
   if (type == exact) {
      setupRequired(meas_deblender  -j 11.0+3)
      setupRequired(utils           -j 11.0-1-g47edd16)
   […]

:command:`eups distrib`
=======================

:command:`eups distrib` is a package distribution mechanism which provides a
convenient way of installing and updating the LSST stack. It is distinct from
the core EUPS functionality described above, but is closely integrated and
shares many concepts.

:command:`eups distrib` reads details about available packages from a remote
server. The appropriate location for finding LSST software is
https://eups.lsst.codes/stack/src. We can use :command:`eups distrib list` to
list available software, and :command:`eups distrib install` to install it::

   % eups distrib path
   https://eups.lsst.codes/stack/src

   % eups distrib list lsst_apps
   lsst_apps            generic    8.0.0.1+2
   lsst_apps            generic    8.0.0.1+3
   […]

   % eups distrib install -t v11_0 lsst_apps

Note that :command:`eups distrib list` does not list tags, even though
:command:`eups distrib install` accepts a tag as a command line option (``-t
v11_0``). The most convenient way to see a list of available tags is to visit
the distribution server (https://eups.lsst.codes/stack/src/tags) in a web
browser.

Further Information
===================

EUPS is developed outside the LSST stack in an `independent GitHub
repository`_ which provides its own `issue tracker`_. However, it is important
to track problems with installing the stack in :ref:`JIRA <workflow-jira>`,
even if they are already known in the EUPS tracker.

EUPS ships with a `manual`_, but it can be hard to read when getting started.

.. _independent GitHub repository: https://github.com/RobertLuptonTheGood/eups
.. _issue tracker: https://github.com/RobertLuptonTheGood/eups/issues
.. _manual: https://github.com/RobertLuptonTheGood/eups/blob/master/doc/eups.tex
