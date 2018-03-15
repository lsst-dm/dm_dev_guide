#########################
C++ performance profiling
#########################

It is important to generate a profile of code performance to understand where to focus optimization efforts.

igprof
======

Profiling C++ code can be done with `igprof <http://igprof.org>`_:

.. code-block:: bash

   igprof -pp -z -o igprof-mosaic.pp.gz python `which mosaic.py` /data3a/work/price/SUPA-MIT/rerun/cosmos --id field=COSMOS filter=W-S-I+ expTime=120.0 --clobber-config
   igprof-analyse -d -v -g igprof-mosaic.pp.gz > igprof-mosaic.pp.txt

That provides the cumulative profile (top) and then the caller/callee profiles further down (see http://igprof.org/text-output-format.html).
There is a fancy ``cgi-bin`` setup for browsing the profiles, but it requires setting up your Apache server.
This may or may not be worth the trouble.

Note that there is a `bug in igprof <https://github.com/igprof/igprof/issues/17>`_ (or its dependency, libunwind) that sometimes causes the process to hang.
The recommended workaround is "to make sure you have a hot cache for your libraries (``cat *.so >/dev/null``)".
A slightly more complete command is

.. code-block:: bash

   (export IFS=:; while true ; do for DIR in $LD_LIBRARY_PATH ; do find $DIR -name "*.so" -exec cat {} > /dev/null \; ; done; sleep 5; done) &

sprof
=====

sprof is part of glibc, so should be available on most Linux systems.
Unlike its cousin, gprof, it does not require recompilation and it works on shared libraries, so can be used with your current stack setup, whatever that may be.
Unfortunately, it allows profiling only one shared library at a time, but generally the shared library of interest can be identified using Python profiling.
Here's an example using sprof to profile the CModel code in meas_modelfit (which is exercised by ``measureCoaddSources.py``):

.. code-block:: bash

    export LD_PROFILE=libmeas_modelfit.so
    export LD_PROFILE_OUTPUT=`pwd`
    measureCoaddSources.py /scratch/pprice/ci_hsc/DATA --rerun ci_hsc --id patch=5,4 tract=0 filter=HSC-I
    sprof -p -q libmeas_modelfit.so libmeas_modelfit.so.profile > libmeas_modelfit.so.profile.txt

The output of sprof contains a cumulative profile at the top, followed by the caller/callee profiles.
