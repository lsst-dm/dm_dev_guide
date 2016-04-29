###########################################
Distributing Third-Party Packages with EUPS
###########################################

This page documents how to make a third-party software package install-able
using the :command:`eups distrib install` command.

Creating the Package
====================

Repositories containing third-party packages exist in the `LSST GitHub
organization`_. (Unfortunately, it is currently difficult to distinguish
between an LSST package and a third-party package: `the table file`_ in the
``lsst_thirdparty`` package and the documentation on `third party software`_
may help.) In order to distribute a new third-party package, someone with
administrator privileges will have to create a new repository of this form for
you. Create a development branch on that repository and set it up to
distribute the package as described below.  You will be able to test the
package distribution off of your development branch before you merge to
``master``.

The repository, once created, needs to contain the following directories:

:file:`upstream/`
    This directory should contain a gzipped tarball of the source code for the
    third-party package.  Literally, that is all it should contain.  The code
    should not be altered from whatever is distributed by the package's
    author.  Any changes that need to be made to the source code should be
    done with patches in the patches/ directory.

:file:`ups/`
    This directory should contain the packages EUPS table file as well as an
    optional file :file:`eupspkg.cfg.sh` which will contain any customized
    commands for installing the third-party package.

:file:`patches/`
    This directory is optional. It contains any patches to the third-party
    package (which EUPS will apply using the :command:`patch` command) that
    are required to make the package work with the stack.

We discuss the contents of :file:`ups/` and :file:`patches/` in more detail
below.

.. warning::

   If the root directory of your repository contains any other files (e.g.
   :file:`README`, :file:`.gitignore`, etc) you will need to give special
   instructions on how to handle them. See the section on
   :ref:`build-third-party-other-files`, below.

.. _LSST GitHub organization: https://github.com/lsst
.. _the table file: https://github.com/lsst/lsst_thirdparty/blob/master/ups/lsst_thirdparty.table
.. _third party software: https://confluence.lsstcorp.org/display/DM/DM+Third+Party+Software

The :file:`ups/` Directory
--------------------------

EUPS Table File
^^^^^^^^^^^^^^^

The :file:`ups/` directory in your repository must contain an EUPS table file
named following the pattern :file:`packageName.table`. It specifies what other
packages your package depends on and environment variables that will be set
when you :command:`setup` your package.  Consider the table file for the
``sphgeom`` package, :file:`sphgeom.table`::

    setupRequired(base)
    setupRequired(sconsUtils)
    setupOptional(doxygen)

    envPrepend(LD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
    envPrepend(DYLD_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
    envPrepend(LSST_LIBRARY_PATH, ${PRODUCT_DIR}/lib)
    envPrepend(PYTHONPATH, ${PRODUCT_DIR}/python)

This tells EUPS that, in order to setup the ``sphgeom`` package, it must also
setup the packages ``base``, ``sconsUtils`` and ``doxygen``.  Furthermore, it
adds the location of the ``sphgeom`` package (stored in the environment
variable :envvar:`PRODUCT_DIR` at build time) to the environment variables
:envvar:`PYTHONPATH`, :envvar:`LD_LIBRARY_PATH`, :envvar:`DYLD_LIBRARY_PATH`,
:envvar:`LSST_LIBRARY_PATH`. These three environment variables are usually set
for any installed package. We use the pre-defined ``envPrepend`` command so
that the new :envvar:`PRODUCT_DIR` is prepended to the environment variables
and does not interfere with the non-stack system of libraries.

:file:`eupspkg.cfg.sh`
^^^^^^^^^^^^^^^^^^^^^^

:file:`eupspkg.cfg.sh` is an optional script in the :file:`ups/` directory
that customizes the installation of your package. Often, EUPS is smart enough
to figure out how to install your package just based on the contents of the
gzipped tarball in :file:`upstream/`. Sometimes, however, you will need to
pass some additional commands in by hand. A simple version of this can be seen
in the :file:`eupspkg.cfg.sh` for the `GalSim`_ package, which passes
instructions to the `SCons`_ build system using the :envvar:`SCONSFLAGS`
environment variable::

    export SCONSFLAGS=$SCONSFLAGS" USE_UNKNOWN_VARS=true TMV_DIR="$TMV_DIR" \
           PREFIX="$PREFIX" PYPREFIX="$PREFIX"/lib/python                   \
           EXTRA_LIB_PATH="$TMV_DIR"/lib EXTRA_INCLUDE_PATH="$TMV_DIR"/include"

The :file:`eupspkg.cfg.sh` for the stack-distributed anaconda package is more
complicated::

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

The :file:`eupspkg.cfg.sh` file allows you to customize any or all of these
steps for your package.  Above, we see that the prep and install steps have
been customized for the `Anaconda`_ package. More detailed documentation of the
purpose and capabilities of the :file:`eupspkg.cfg.sh` file can be found in the
source code file :file:`$EUPS_DIR/python/eups/distrib/eupspkg.py`.

.. _GalSim: https://github.com/GalSim-developers/GalSim/
.. _SCons: http://www.scons.org/
.. _Anaconda: https://www.continuum.io/why-anaconda

The :file:`patches/` Directory
------------------------------

Sometimes, it will be necessary to change the source code in the gzipped
tarball stored in :file:`upstream/` to make the package installable and
runnable with the stack.  If this is necessary, it is done using the
:command:`patch` command, which applies diffs to source code files. For each
change that needs to be made to the source code, generate a patch file using
the command::

    git diff -u originalFile correctedFile > someFileName.patch

Save the :file:`someFileName.patch` files in the :file:`patches/` directory of
the repository. EUPS will know to apply these patches after it unpacks the
gzipped tarball in :file:`upstream/`.

.. note::

   EUPS expects the patches to be formatted according to the output of
   :command:`git diff`, not the output of :command:`diff`.

.. _build-third-party-other-files:

Other Files
-----------

The form of package that has been constructed is referred to by EUPS as a
‘tarball-and-patch’ or ‘TaP’ package. Although these are standard for use in
LSST, they are not the only type of package EUPS supports.

When confronted with a source directory, EUPS attempts to determine what sort
of package it is dealing with. If it sees *any* files other than the
directories listed above, it concludes that the package in question is *not* a
TaP package.

Often, it is desirable to add other files to the package (for example,
:file:`README` or :file:`.gitignore`). EUPS will then misidentify the package
type, and the build will fail.

To account for this, it is necessary to explicitly flag this as a TaP package.
There are two mechanisms for this, depending of the `version of EUPS`_ being
used. At time of writing, LSST's :doc:`/build-ci/ci_overview` use a version of
EUPS which only supports the now-deprecated mechanism. Therefore, in the
interests of future proofing, both:

#. Add the line ``TAP_PACKAGE=1`` to the top of :file:`ups/eupspkg.cfg.sh`;
#. Add an empty file, :file:`.tap_package`, to the root directory of your
   package.

.. _version of EUPS: https://github.com/RobertLuptonTheGood/eups/blob/2.0.2/Release_Notes#L21

Testing the Package
===================

.. note::

   Development of a third party package should be handled identically to
   development of LSST software: work on a development branch and merge to
   master only after a successful build and a review.

Before finalizing the distribution, it is useful to be able to test that the
distribution as set up does, in fact, build. This can be accomplished using
the :command:`lsstsw` build tool: see its :doc:`detailed documentation
<lsstsw>` for the full story. Broadly, the steps are:

- Clone and set up the lsstsw package in its own directory using the
  instructions on the lsstsw documentation page pointed to above.

- In the :command:`lsstsw` package, use the command::

      ./bin/rebuild -r yourBranch yourPackage

  to build the development branch of your package.

- Ideally, you should try this process on at least two different machines (one
  running OSX and one running a Linux distribution) to make sure that you did
  not accidentally benefit from the system environment of your test machine
  when building.

Distributing the Package
========================

Once the package builds and passes review (or vice-versa), you need to tell
eups that it is available for distribution to the wide world.  To do this, add
an annotated tag to your package repository using::

    git tag -a versionNumber -m "Some comment."

The initial ``versionNumber`` should match the external package's version
number. If the package does not supply an appropriate version number, one can
be generated from an upstream git SHA1 or equivalent version control revision
number: use the format ``0.N.SHA1``, where ``N`` is ``1`` for the first
release of the package, ``2`` for the second, etc. Note that the version
number should never start with a letter, as EUPS regards that as semantically
significant.

If changes are required to the packaging (in the :file:`ups` or
:file:`patches` directories) but not the external package source (in the
:file:`upstream` directory), the string ``.lsst1`` (and ``.lsst2`` etc.
thereafter) should be appended to the external package's version number.
Merge your changes to ``master``, then push your changes to the remote
repository. Push your tags to the remote repository using::

    git push --tags

Now you must log onto ``lsst-dev`` as the user ``lsstsw`` (this will require
special permissions): see the :doc:`documentation on using this machine
<../services/lsst-dev>`. Once logged in as ``lsstsw``, the steps are:

- Build your package with the command::

      rebuild yourPackage

  This will cause ``lsst-dev`` to build your package and all of its
  dependencies.  This build will be assigned a build number formatted as
  ``bNNN````

- Once the build is complete, release it to the world using::

      publish -b bNNN yourPackage

  This will make your package installable using::

      eups distrib install yourPackage versionNumber

  If you wish to add a distribution server tag to your package, you can do so
  by changing the publish command to::

      publish -b bNNN -t yourTag yourPackage

  .. warning::

     Do not use the tag 'current' as that will overwrite all other packages
     marked as current and break the stack.  Let the people in charge of
     official releases handle marking things as 'current.'  it is not usually
     necessary to distribution-server-tag a particular third party package.

- Generally, if you're publishing a third party package, it should be because
  it is a dependency in the build of some (or all) top-level package(s). When
  the top-level package(s) are next published (and optionally tagged), your
  new package will be incorporated. If you need something sooner, you can do
  this publishing yourself using the steps above with the top-level package.
  In this case, a distribution-server-tag (something like ``qserv-dev``) is
  usually desirable.  That makes the top-level product (or any of its
  dependency components, including your third-party package) installable
  using::

      eups distrib install -t yourTag packageName

Updating the Package
====================

.. note::

   These instructions are still under construction.

To update the version of your external package after a new upstream release,
start with a copy of the LSST stack (`installed using the lsstsw tool`_).
Then:

- Create a ticket for the package update (and/or an :ref:`RFC
  <decision-making-rfc>`, if it may cause more trouble), and note the ticket
  number ``NNNN``.

- :command:`cd build/yourPackage`

- :command:`git checkout -b tickets/DM-NNNN` (where ``NNNN`` is the ticket number above)

- :command:`git clean -id`

- Download a copy of the tarball from wherever the external package is
  distributed. Don't unzip or untar it.

- :command:`git rm` the copy of the tarball that is currently in
  :file:`upstream/`. Copy the new version of the external tarball into
  :file:`upstream/` and :command:`git add` it.

- :command:`git commit`

- :command:`git push`

- See if the stack will build with your branch in :ref:`Jenkins
  <workflow-testing>`. For the branch name, specify the branch you created
  above (i.e. ``tickets/DM-NNNN``), leaving the rest of the fields as they
  are.

- While Jenkins is building, you can test whether the new package solves
  whatever issue caused you to need the upgrade. From within
  :file:`build/yourPackage`:

    - :command:`eupspkg -er -v 1 prep`
    - :command:`eupspkg -er -v 1 config`
    - :command:`eupspkg -er -v 1 build`
    - :command:`eupspkg -er -v 1 install`
    - :command:`eupspkg -er -v 1 decl`
    - :command:`eups list yourPackage` should now show a new version named
      ``tickets/DM-NNNN-gBLAHBLAH`` where ``gBLAHBLAH`` is the git has
      revision of the package.
    - :command:`setup lsst_apps -t YOURTAG`
    - :command:`setup yourPackage tickets/DM-NNNN-gBLAHBLAH`
    - Run your tests.

- Merge to master after tests pass.

.. _installed using the lsstsw tool: http://pipelines.lsst.io/en/latest/development/lsstsw_tutorial.html
