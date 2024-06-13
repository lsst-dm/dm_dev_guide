###########################################
Distributing Third-Party Packages with EUPS
###########################################

This page documents how to make a third-party software package installable using the :command:`eups distrib install` command via two methods: the "forked repo" and the "tarball-and-patch" (TaP) package.

Generally, most dependencies :doc:`should be added via conda </stack/conda>` using the ``rubin-env`` metapackage rather than either of these eups methods.
If the package is already in conda-forge, it can be added to ``rubin-env`` :ref:`via RFC <third-party-approval>`.
(Changes to ``rubin-env`` are made approximately 2-4 times a year.)
If the package is not already in conda-forge, `creating and maintaining a conda-forge recipe`_ is about the same level of effort as maintaining a TaP package, and it makes the package available to the conda-forge community at large rather than just LSST Science Pipelines consumers.

.. _creating and maintaining a conda-forge recipe: https://conda-forge.org/docs/maintainer/adding_pkgs/

If the package is changing rapidly, particularly in its interface, and if the Science Pipelines need those new features or fixes as soon as possible, perhaps even before an official release of the package, a forked repo is usually recommended.
This also :ref:`requires an RFC <third-party-approval>` to add the dependency, but new versions can be incorporated into weekly and even daily builds of the Science Pipelines.

The primary, and rare, reasons to add a TaP package as described here are if we require a fix that will not be released in conda-forge or if the package has no conda-forge recipe at all and we do not want to create one because maintenance of a community recipe might be more burdensome than that of a Science Pipelines-only package (e.g. if we only use a piece of the package but the community would use all of it).


.. _third-party-approval:

Getting Approval
================

Creating a new third-party package that will be a dependency of the LSST code requires an :doc:`RFC </communications/rfc>`.
If the code is to be distributed via :command:`eups`, as this page describes, the license for the third-party code should be verified and cited in the text of that RFC.
The license must be compatible with the license under which we distribute our code, currently GPL3.
See `this page`_ for a list of compatible licenses.

.. _this page: https://www.gnu.org/licenses/license-list.html


.. _fork-creating:

Creating A Forked Repo
======================

A forked repo relies on building the package from source, rather than using binary artifacts, on the assumption that we may need to use the latest developments.
Accordingly, we fork the package on GitHub into the ``lsst`` organization and add the "DM Externals" and "Overlords" teams to it as described in :doc:`adding-a-new-package`.
This ensures that it will be tagged appropriately for official releases (while not conflicting with the third-party tags).

Since the third-party package likely has no support for eups, we need to add a ``ups`` directory.
This directory should contain the package's EUPS table file as well as an optional file :file:`eupspkg.cfg.sh` which will contain any customized commands for building and installing the third-party package.

The upstream source has no need to know about the ``ups`` directory, so we put it on a separate branch in the ``lsst`` fork.
That branch is traditionally named ``lsst-dev``.
We set that branch to be the GitHub default in our fork.

When changes are made to the upstream source, they can be merged into the ``lsst-dev`` branch, or ``lsst-dev`` can be rebased on an upstream branch.
If we make local changes for our own needs, they can be converted into PRs to the upstream fork, leaving out any commits that refer to the ``ups`` directory contents.

The new package then needs to be added to ``etc/repos.yaml`` in the ``lsst/repos`` repository.
We indicate that the ``lsst-dev`` branch is the one that we will build from by adding a ``ref:`` clause in that file.

Finally, the package should be added as an eups dependency to some other package or meta-package in its ``.table`` file.
This will ensure that it is incorporated in the Science Pipelines build.

If Rubin Data Management becomes the primary maintainer of the package, it can still be treated as third-party, but it may make sense to transition it to being a first-party package.
That would mean ensuring it follows all DM standards and processes.
It can still be published :doc:`via PyPI </stack/building-with-pip>` and conda, in addition to eups.


.. _third-party-creating:

Creating a TaP Package
======================

Repositories containing third-party packages exist in the `LSST GitHub organization`_.
(Unfortunately, it is currently difficult to distinguish between an LSST package and a third-party package: `the table file`_ in the ``lsst_thirdparty`` package and the documentation on `third party software`_ may help.)
In order to distribute a new third-party package, someone with administrator privileges will have to create a new repository of this form for you.
Make sure that the new repository is accessible by the "DM Externals" and "Overlords" teams as described in :doc:`adding-a-new-package`.
Create a development branch on that repository and set it up to distribute the package as described below.
You will be able to test the package distribution off of your development branch before you merge to the default branch.

The repository, once created, needs to contain the following directories:

:file:`upstream/`
    This directory should contain a gzipped tarball of the source code for the third-party package.
    Literally, that is all it should contain.
    The code should not be altered from whatever is distributed by the package's author.
    Any changes that need to be made to the source code should be done with patches in the patches/ directory.
    If you are testing out a version that is not a distributed package (e.g. from the package's git repo), you can create the correct type of repository from within a clone of the package with, e.g.::

        git archive --format=tar --prefix=astrometry.net-68b1/ HEAD | gzip > astrometry.net-68b1.tar.gz

:file:`ups/`
    This directory should contain the package's EUPS table file as well as an optional file :file:`eupspkg.cfg.sh` which will contain any customized commands for installing the third-party package.

:file:`patches/`
    This directory is optional.
    It contains any patches to the third-party package (which EUPS will apply using the :command:`patch` command) that are required to make the package work with the stack.

We discuss the contents of :file:`ups/` and :file:`patches/` in more detail below.

.. warning::

   If the root directory of your repository contains any other files (e.g. :file:`README`, :file:`.gitignore`, etc) you will need to give special instructions on how to handle them.
   See the section on :ref:`build-third-party-other-files`, below.

.. _LSST GitHub organization: https://github.com/lsst
.. _the table file: https://github.com/lsst/lsst_thirdparty/blob/main/ups/lsst_thirdparty.table
.. _third party software: https://confluence.lsstcorp.org/display/DM/DM+Third+Party+Software

The :file:`ups/` Directory
--------------------------

EUPS Table File
^^^^^^^^^^^^^^^

The :file:`ups/` directory in your repository must contain an EUPS table file named following the pattern :file:`packageName.table`.
It specifies what other packages your package depends on and environment variables that will be set when you :command:`setup` your package.
Consider the table file for the ``sphgeom`` package, :file:`sphgeom.table`::

    setupRequired(base)
    setupRequired(sconsUtils)
    setupOptional(doxygen)

    envPrepend(LD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
    envPrepend(DYLD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
    envPrepend(LSST_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
    envPrepend(PYTHONPATH, ${PRODUCT_DIR}/python)

This tells EUPS that, in order to setup the ``sphgeom`` package, it must also setup the packages ``base``, ``sconsUtils`` and ``doxygen``.
Furthermore, it adds the location of the ``sphgeom`` package (stored in the environment variable ``PRODUCT_DIR`` at build time) to the environment variables ``PYTHONPATH``, ``LD_LIBRARY_PATH``, ``DYLD_LIBRARY_PATH``, ``LSST_LIBRARY_PATH``.
These three environment variables are usually set for any installed package.
We use the pre-defined ``envPrepend`` command so that the new ``PRODUCT_DIR`` is prepended to the environment variables and does not interfere with the non-stack system of libraries.

:file:`eupspkg.cfg.sh`
^^^^^^^^^^^^^^^^^^^^^^

:file:`eupspkg.cfg.sh` is an optional script in the :file:`ups/` directory that customizes the installation of your package.
Often, EUPS is smart enough to figure out how to install your package just based on the contents of the gzipped tarball in :file:`upstream/`.
Sometimes, however, you will need to pass some additional commands in by hand.
A simple version of this can be seen in the :file:`eupspkg.cfg.sh` for the `GalSim`_ package, which passes instructions to the `SCons`_ build system using the ``SCONSFLAGS`` environment variable::

    export SCONSFLAGS=$SCONSFLAGS" USE_UNKNOWN_VARS=true TMV_DIR="$TMV_DIR" \
           PREFIX="$PREFIX" PYPREFIX="$PREFIX"/lib/python                   \
           EXTRA_LIB_PATH="$TMV_DIR"/lib EXTRA_INCLUDE_PATH="$TMV_DIR"/include"

The :file:`eupspkg.cfg.sh` for the stack-distributed anaconda package is more complicated::

	# EupsPkg config file. Sourced by 'eupspkg'

	prep()
	{
	    # Select the apropriate Anaconda distribution
	    OS=$(uname -s -m)
	    case "$OS" in
	        "Linux x86_64")       FN=Anaconda-2.1.0-Linux-x86_64.sh ;;
	        "Linux "*)        FN=Anaconda-2.1.0-Linux-x86.sh ;;
	        "Darwin x86_64")  FN=Anaconda-2.1.0-MacOSX-x86_64.sh ;;
	        *)          die "unsupported OS or architecture ($OS). try installing Anaconda manually."
	    esac

	    # Prefer system curl; user-installed ones sometimes behave oddly
	    if [[ -x /usr/bin/curl ]]; then
	        CURL=${CURL:-/usr/bin/curl}
	    else
	        CURL=${CURL:-curl}
	    fi

	    "$CURL" -s -L -o installer.sh http://repo.continuum.io/archive/$FN
	}

	build() { :; }

	install()
	{
	    clean_old_install

	    bash installer.sh -b -p "$PREFIX"

	    if [[ $(uname -s) = Darwin* ]]; then
	        #run install_name_tool on all of the libpythonX.X.dylib dynamic
	        #libraries in anaconda
	        for entry in $PREFIX/lib/libpython*.dylib
	        do
	            install_name_tool -id $entry $entry
	        done
	    fi

	    install_ups
	}

When EUPS installs a third party package, it does so in five steps:

#. ``fetch``
#. ``prep``
#. ``config``
#. ``build``
#. ``install``

The :file:`eupspkg.cfg.sh` file allows you to customize any or all of these steps for your package.
Above, we see that the prep and install steps have been customized for the `Anaconda`_ package.
More detailed documentation of the purpose and capabilities of the :file:`eupspkg.cfg.sh` file can be found in the source code file :file:`$EUPS_DIR/python/eups/distrib/eupspkg.py`.

.. _GalSim: https://github.com/GalSim-developers/GalSim/
.. _SCons: http://www.scons.org/
.. _Anaconda: https://www.continuum.io/why-anaconda

The :file:`patches/` Directory
------------------------------

Sometimes, it will be necessary to change the source code in the gzipped tarball stored in :file:`upstream/` to make the package installable and runnable with the stack.
If this is necessary, it is done using the :command:`patch` command, which applies diffs to source code files.
For each logical change that needs to be made to the source code (possibly affecting multiple files), generate a patch file by following these instructions:

#. Untar the tarball you're trying to patch (e.g., :file:`astrometry.net-0.50.tar.gz`).
   It will generate a directory (e.g., :file:`astrometry.net-0.50/`) with the source.
#. Make a copy of that directory::

    cp -a astrometry.net-0.50 astrometry.net-0.50.orig

#. Make any changes you need to the source in :file:`astrometry.net-0.50/`
#. Create a patch :command:`diff -ru` and move it into the patches/ subdirectory::

    diff -ru astrometry.net-0.50.orig astrometry.net-0.50 > blah.patch

EUPS will apply these patches after it unpacks the gzipped tarball in :file:`upstream/`.
Patches are applied in alphabetical order, so it can be useful to start your patches with, e.g. :file:`000-something.patch`, :file:`001-somethingelse.patch`.

.. note::

   EUPS expects the patches to be in unified format, as generated by the ``-u`` option to the :command:`diff` command.

.. _build-third-party-other-files:

Other Files
-----------

The form of package that has been constructed is referred to by EUPS as a ‘tarball-and-patch’ or ‘TaP’ package.
Although these are standard for use in LSST, they are not the only type of package EUPS supports.

When confronted with a source directory, EUPS attempts to determine what sort of package it is dealing with.
If it sees *any* files other than the directories listed above, it concludes that the package in question is *not* a TaP package.

Often, it is desirable to add other files to the package (for example, :file:`README` or :file:`.gitignore`).
EUPS will then misidentify the package type, and the build will fail.

To account for this, it is necessary to explicitly flag this as a TaP package.
This is done by adding the line ``TAP_PACKAGE=1`` to the top of :file:`ups/eupspkg.cfg.sh`.
(An older mechanism relied on a :file:`.tap_package` file in the package root directory, but this is deprecated.)


.. _third-party-testing:

Testing the package
===================

If you've created a new external package or updated an existing package, you need to test whether the new package builds and works.
From within :file:`build/yourPackage` (add ``-r`` to build in the current directory, which is effectively how Jenkins does it, instead using :file:`_eupspkg/`):

- :command:`rm -r _eupspkg`
- :command:`eupspkg -e -v 1 fetch`
- :command:`eupspkg -e -v 1 prep`
- :command:`eupspkg -e -v 1 config`
- :command:`eupspkg -e -v 1 build`
- :command:`eupspkg -e -v 1 install`
- :command:`setup -r _eupspkg/binary/yourPackage/tickets.DM-NNNN` to set up the newly built version.
- Run your tests.
- When your local tests pass, :command:`git push`.
- See if the stack will build with your branch in :ref:`Jenkins <workflow-testing>`.
  For the branch name, specify the branch you created above (i.e. ``tickets/DM-NNNN``), leaving the rest of the fields as they are.
- Merge to the default branch after Jenkins passes and your changes are reviewed.

.. _third-party-updating:

Updating the Package
====================

To update the version of your external package after a new upstream release, start with a copy of the LSST stack (`installed using the lsstsw tool`_).
Then:

- Create a ticket for the package update (and/or an :doc:`RFC </communications/rfc>`, if it may cause more trouble), and note the ticket number ``NNNN``.
- :command:`cd build/yourPackage`
- :command:`git checkout -b tickets/DM-NNNN` (where ``NNNN`` is the ticket number above)
- :command:`git clean -id`
- Download a copy of the tarball from wherever the external package is distributed.
  Don't unzip or untar it.
- :command:`git rm` the copy of the tarball that is currently in :file:`upstream/`.
- Copy the new version of the external tarball into :file:`upstream/` and :command:`git add` it.
- :command:`git commit`

Now test your package by following :ref:`the instructions above <third-party-testing>`.
Then continue with the tagging and distribution instructions below.

.. _installed using the lsstsw tool: https://pipelines.lsst.io/install/lsstsw.html

.. _third-party-distributing:

Distributing the Package
========================

Once the package builds, passes tests, passes review, and is merged to the default branch, you need to tell EUPS that it is available for distribution to the wide world.
To do this, add an annotated tag to your package repository using::

    git tag -a versionNumber -m "Some comment."

The initial ``versionNumber`` should match the external package's version number.
If the package does not supply an appropriate version number, one can be generated from an upstream git SHA1 or equivalent version control revision number: use the format ``0.N.SHA1``, where ``N`` is ``1`` for the first release of the package, ``2`` for the second, etc.
Note that the version number should never start with a letter, as EUPS regards that as semantically significant.

If changes are required to the packaging (in the :file:`ups` or :file:`patches` directories) but not the external package source (in the :file:`upstream` directory), the string ``.lsst1`` (and ``.lsst2`` etc.  thereafter) should be appended to the external package's version number.

Push your tags to the remote repository using::

    git push --tags

Also add the package to :doc:`repos.yaml </stack/adding-a-new-package>` and to the table file(s) of the package(s) that depend on it.

The third-party package will be published by Jenkins with the next nightly release.

.. third-party-announcing:

Announcing the Package
======================

Any new packages, major version upgrades, or other breaking changes to third-party package versions should be announced in the DM Notifications category of community.lsst.org.

For upgrades to third-party packages with headers we build against, this should include a note that source packages should be cleaned and recompiled  after the upgrade, because SCons/sconsUtils will not automatically detect changes in third-party headers.
