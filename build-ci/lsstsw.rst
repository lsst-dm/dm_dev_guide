############################
The LSST Software Build Tool
############################

Introduction
============

The :command:`lsst-build` tool recursively clones, builds, and installs the
LSST Stack.  While the motivation for its creation was to serve as a backend
for the :doc:`continuous integration system <ci_overview>`, anyone may
download and run it to do stack-wide integration builds (including building
with alternative versions of external packages, etc.). The core tool lives in
the `lsst_build repository`_.

Howevever the :command:`lsstsw` tool provides a more convenient way to set up
a personal build environment. It is available from the `lsstsw repository`_::

    git clone https://github.com/lsst/lsstsw.git

The :command:`lsstsw` package is primarily used to manage the :abbr:`CI
(Continuous Integration)` system, but it is self contained and can be used
anywhere by anyone.

After the clone, bootstrap the environment as follows::

    cd lsstsw
    ./bin/deploy

This will:

- Download and install `Miniconda`_ in :file:`./miniconda`;
- Download and install `Git`_ in :file:`./lfs`;
- Download and install `EUPS`_ in :file:`./eups`;
- Make an empty stack directory in :file:`./stack`, with a default
  :file:`manifest.remap`;
- Run :command:`git clone lsst_build master`
- Run :command:`git clone versiondb master`

Once the bootstrap has completed, set up the environment as directed. For
example::

    export LSSTSW=<where you've set it up>
    export EUPS_PATH=$LSSTSW/stack
    . $LSSTSW/bin/setup.sh

.. note::

   It is only necessary to run :command:`deploy` once, although it is clever
   enough to turn into a no-op when it detects it has successfully run
   already.

.. _lsst_build repository: https://github.com/lsst/lsst_build.git
.. _lsstsw repository: https://github.com/lsst/lsstsw.git
.. _Miniconda: http://conda.pydata.org/miniconda.html
.. _Git: http://git-scm.com/
.. _EUPS: https://github.com/RobertLuptonTheGood/eups/

Recursively Cloning & (Re)building a Package
============================================

Assuming you've done all of the above, simply run::

    rebuild lsst_apps

``lsst_apps`` is an empty package that depends on all of the LSST packages.
You can use the :command:`rebuild` command to build other packages by name as
well.

Once you have built a package you may want to clone the new EUPS tag to
``current``, so you can setup the package without specifying a particular tag.
For example if :command:`lsstsw` just built a package using EUPS tag ``b6132``
you clone that to current using::

    eups tags --clone b6132 current

The :command:`rebuild` command is is a wrapper around the lower-level
:command:`lsst-build` tool (described below). It will:

* Search for and clone the package from our Git repositories (as configured in
  :file:`etc/repos.yaml`) into :file:`$LSSTSW/build`;

* Recursively clone all of its dependencies (also into :file:`$LSSTSW/build`);

* Recursively build all its dependencies bottom-up, installing the built
  packages into :file:`$LSSTSW/stack`, using an eups tag of the form ``bNNN``
  (where ``N`` is a digit), e.g. ``b6132``;

* Build the package as well, and install it into ``$LSSTSW/stack``.


.. note::

   Rebuilding ``afwdata`` may take awhile, since it must download several GB
   of data. If you already have copy that is checked out from the same URL as
   in the :file:`etc/repos.yaml` file, you can use it by making a symlink to
   :file:`$LSSTSW/build/afwdata`. In fact it is very useful to store
   ``afwdata`` outside the ``lsstsw`` directory and symlink to it, as it
   allows you to delete your copy of ``lsstsw`` at any time to start fresh,
   without downloading ``afwdata`` again.  To do this, run ``bin/deploy``
   on your fresh copy of ``lsstsw``, then make the symlink before running
   ``rebuild``. If you don't want a copy of ``afwdata`` at all
   then you can add it to the :file:`etc/exclusions.txt` file.

Customizations are possible by editing the :file:`etc/settings.cfg.sh` file,
or by running :command:`lsst-build` manually. See the documentation in
:command:`bin/rebuild` to see how.

To rebuild the entire stack, pick one of the top-level packages (e.g.,
``lsst_distrib`` or ``lsst_apps``).

Building Branches
-----------------

You can build specific branch(es) by running::

    rebuild -r branch1 -r branch2 -r ... <packagename>

Before building, the code above will attempt to checkout ``branch1`` (both in the
package and its dependencies), and fall back to ``branch2`` if it doesn't exist,
and then fall back to master (or another default branch configured in
:file:`etc/repos.yaml`).

Other command-line options for :command:`rebuild`
-------------------------------------------------

``-p`` will clone the required packages and then stop, without building
anything.

``-u`` will bring over a current copy of :file:`etc/repos.yaml` before
starting the build.  This can be handy if repositories have moved or been
added and is used by our continuous integration system.

``-t <tag>`` is deprecated. Use this instead: :command:`eups tags
--clone=oldtag newtag`.

Low(er)-level tool: :command:`lsst-build`
=========================================

Here is an example of how to run :command:`lsst-build`::

    lsst-build prepare \
      --exclusion-map=exclusions.txt \
      --version-git-repo=versiondb \
      ./build lsst_distrib
    lsst-build build ./build

.. note::

   For full details of the :command:`lsst-build` setup procedure, see the
   :file:`README` file included in the package.

The :command:`lsst-build prepare` command will begin by cloning the
``lsst_distrib`` product into :file:`./build/lsst_distrib`, it will read its
dependencies from the table file, and then recursively repeat the process with
each one of them until all leafs of the dependency graph are reached. If you
just want to clone all packages needed to build a certain package from Git,
this is the tool.  More than one top-level package can be prepared at the same
time (e.g., run it with :command:`... lsst_distrib git anaconda`).

In addition to the mass clone, running :command:`lsst-build prepare` will also
create a "build manifest" file in :file:`build/manifest.txt`. This is a
topologically sorted list of all cloned products and the versions that were
computed for them. The versions are of the form ``<tag>[+<N>]`` (if an
annotated tag exists on a commit), or ``<branch>-g<sha>[+<N>]`` if there's no
tag. The way the code tracks which ``+N`` number to use is through the
``versiondb`` database (which is just a specially formatted git repository;
again see the :file:`README` for details).

The second command then takes the cloned repositories and the information in
:file:`manifest.txt` and builds the products, installs them into the stack
pointed to by ``EUPS_PATH``, and tags them with a "build ID" (a unique
ID computed for each :file:`manifest.txt`, and listed in the
:file:`manifest.txt` itself as ``BUILD=bNNN``). Therefore, running the two
commands will build and install a complete, functioning stack for you. The log
of build output for each package is in :file:`_build.log` in its directory
(e.g., in :file:`./build/afw`), as well as in the directory where it's
installed (if the build is successful).

Importantly, :command:`lsst-build prepare` can take one or more ``--ref
<branch_or_tag>`` arguments. So, you can say::

    lsst-build prepare \
      ... \
      --ref tickets/1234 --ref next --ref master \
      build lsst_distrib

and, upon cloning each repository, it will attempt to checkout
``tickets/1234``, falling back to ``next`` if it doesn't exist, and finally to
``master``. This is how we test whether the changes on a branch break the
stack.

Implementing that was the easy part. The hard part was making these tools
efficient, while being robust (and there is still room for improvement). As an
example, on subsequent times you run :command:`lsst-build prepare` (possibly
with different arguments), it will avoid cloning the repositories it already
has (and the hard-hard part was making this robust so it works even in
presence of forced pushes, dirty directories, removed or changed tags, changed
remote URLs, and all sorts of evil nastiness that we shouldn't have but almost
certainly will). Also, :command:`lsst-build prepare` is guaranteed to produce
the same version for the same source code + dependencies. That enables
:command:`lsst-build build` to check if the product with that version already
exists in the stack, before building it. Therefore, :command:`lsst-build
build` will only build the packages that need to be built (either because they
or their depencencies have changed), and can skip the already built ones.

.. warning::

   The timings cited below are old and likely unrepresentative of a modern
   (2016) stack.

Using :command:`lsst-build`, it is possible to rebuild the complete stack
(everything up to ``lsst_distrib``) in ~25 minutes in ``lsst-dev:/ssd``. If
something above ``afw`` has changed, the build time drops to ~10-ish minutes.

.. warning::

   The material below is old and may be outdated; refer to the
   :doc:`ci_overview` documentation for the current story.

This machinery is now also installed into :file:`~lsstsw`, and Buildbot will
use it from there. Buildbot will ultimately manage both the ``lsst-dev`` stack
and the distribution server. The old tools (e.g., :command:`submitRelease`,
...) are gone. The old stack (the one in :file:`/lsst/DC3/....`) will be gone as well.
The new (automated) workflow is as follows:

#. The new ``lsst-dev`` stack is in :file:`~lsstsw/stack`. Set your
   ``EUPS_PATH`` to point to it.

#. :command:`lsst-build` right now periodically runs from :command:`cron` and
   builds the ``master`` branch any time it changes. The results end up in
   :file:`~lsstsw/stack`.  each build is EUPS-tagged with a unique build
   number (e.g., ``b1``, ``b2``, ``b3``, ...).  The latest build gets EUPS
   tagged as ``current``. There's no more need to run ``submitRelease``, since
   everything is available.

#. When we want to release the stack, someone with :file:`~lsstsw` access will
   log into :file:`~lsstsw` and runs the standard :command:`eups distrib
   create`, possibly EUPS-tagging it as something more memorable than ``bNNN``
   (e.g., ``Winter2014``). If it's useful, we could also automatically release
   the ``bNNN`` builds.  Right now there is a set of product with ``b1`` EUPS
   tag there. These are a build of master as of yesterday, which I Git-tagged
   as ``8.0.0.0``. Consider this a release candidate for Winter'14, and take a
   look.  I'll proceed to build an EUPS distribution as well soon.
