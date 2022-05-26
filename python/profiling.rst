############################
Python performance profiling
############################

It is important to generate a profile of code performance to understand where to focus optimization efforts.
A useful guide to optimization of python code in general, and SciPy/NumPy in particular, is: http://scipy-lectures.github.io/advanced/optimizing/.

Function-level profiling
========================

Consider the code in :file:`mosaic.py`.
To profile it:

.. code-block:: bash

   python -m cProfile -o cprofile-mosaic.dat `which mosaic.py` \
       /data3a/work/price/SUPA-MIT/rerun/cosmos --id field=COSMOS \
       filter=W-S-I+ expTime=120.0 --clobber-config

Then, in a Python session:

.. code-block:: python

   import pstats
   p = pstats.Stats("cprofile-mosaic.dat")
   p.sort_stats("cumulative").print_stats(30) # Print top 30 cumulative

The results are:

.. code-block:: text

   n calls (6698794 primitive calls) in 36.536 seconds

     Ordered by: cumulative time
     List reduced from 4671 to 30 due to restriction <30>

     ncalls  tottime  percall  cumtime  percall filename:lineno(function)
          1    0.004    0.004   36.538   36.538 /home/price/hsc/meas_mosaic/bin/mosaic.py:3(<module>)
          1    0.000    0.000   34.707   34.707 /data1a/ana/products2.1/Linux64/pipe_base/HSC-2.4.1a_hsc/python/lsst/pipe/base/cmdLineTask.py:243(parseAndRun)
          1    0.000    0.000   34.324   34.324 /data1a/ana/products2.1/Linux64/pipe_base/HSC-2.4.1a_hsc/python/lsst/pipe/base/cmdLineTask.py:87(run)
         30    0.000    0.000   34.317    1.144 {map}
          1    0.000    0.000   34.303   34.303 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:45(__call__)
          1    0.073    0.073   34.303   34.303 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:1112(run)
          1    0.176    0.176   34.230   34.230 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:950(mosaic)
          1    2.404    2.404   25.686   25.686 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:268(readCatalog)
        360    0.740    0.002   20.289    0.056 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:205(getAllForCcd)
       1008    0.012    0.000   13.592    0.013 /data1a/ana/products2.1/Linux64/daf_persistence/HSC-2.1.2a_hsc/python/lsst/daf/persistence/butlerSubset.py:171(get)
       1008    0.025    0.000   13.579    0.013 /data1a/ana/products2.1/Linux64/daf_persistence/HSC-2.1.2a_hsc/python/lsst/daf/persistence/butler.py:209(get)
        648    0.007    0.000   12.235    0.019 /data1a/ana/products2.1/Linux64/daf_persistence/HSC-2.1.2a_hsc/python/lsst/daf/persistence/butler.py:239(<lambda>)
        648    0.014    0.000   12.228    0.019 /data1a/ana/products2.1/Linux64/daf_persistence/HSC-2.1.2a_hsc/python/lsst/daf/persistence/butler.py:386(_read)
        324    0.001    0.000   10.380    0.032 /home/price/hsc/afw/python/lsst/afw/table/tableLib.py:7836(readFits)
        324   10.379    0.032   10.379    0.032 {_tableLib.SourceCatalog_readFits}
          1    0.121    0.121    7.344    7.344 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:318(mergeCatalog)
          1    0.000    0.000    6.680    6.680 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicLib.py:1400(kdtreeSource)
          1    6.680    6.680    6.680    6.680 {_mosaicLib.kdtreeSource}
        360    0.001    0.000    2.248    0.006 /home/price/hsc/afw/python/lsst/afw/image/imageLib.py:8635(makeWcs)
        360    2.137    0.006    2.248    0.006 {_imageLib.makeWcs}
        648    0.331    0.001    2.148    0.003 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:173(selectStars)
     153718    0.679    0.000    1.899    0.000 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicLib.py:776(__init__)
        324    0.001    0.000    1.779    0.005 /home/price/hsc/afw/python/lsst/afw/table/tableLib.py:6266(readFits)
        324    1.779    0.005    1.779    0.005 {_tableLib.BaseCatalog_readFits}
       2916    0.178    0.000    1.450    0.000 /home/price/hsc/afw/python/lsst/afw/table/tableLib.py:726(find)
        360    0.000    0.000    1.128    0.003 /data1a/ana/products2.1/Linux64/daf_persistence/HSC-2.1.2a_hsc/python/lsst/daf/persistence/butler.py:236(<lambda>)
        360    0.001    0.000    1.127    0.003 /data1a/ana/products2.1/Linux64/daf_butlerUtils/HSC-2.2.0c_hsc/python/lsst/daf/butlerUtils/cameraMapper.py:315(<lambda>)
        360    0.001    0.000    1.126    0.003 /home/price/hsc/afw/python/lsst/afw/image/imageLib.py:1159(readMetadata)
        360    1.126    0.003    1.126    0.003 {_imageLib.readMetadata}
          1    0.004    0.004    1.036    1.036 /home/price/hsc/meas_mosaic/python/lsst/meas/mosaic/mosaicTask.py:3(<module>)

It is often most useful to look at the ``cumtime`` column, which is the time spent in that function and what it calls.
The results here show that 10/36 = 28% is being spent in ``readFits``, but 26/36 = 72% is devoted to I/O (``readCatalog``).
That might suggest that some Python code should get pushed down to C++.
If you do:

.. code-block:: python

   p.print_callees("readCatalog")
   p.print_callees("getAllForCcd")

you can see that the **cumtime** column doesn't add up to the **cumtime** values in the above, so the remaining time is time spent within those functions doing work.

For more details on pstats and python profiling in general see http://docs.python.org/library/profile.html.

`snakeviz <https://jiffyclub.github.io/snakeviz/>`_ is a web interface for visualizing the python profile output files, installable via ``pip``: pass it the profile output file you wish to visualize to open an interactive browser window.
If you run a pipeline with the ``--profile somefile.prof`` option :ref:`documented below<stack_profiling>`, you can run ``snakeviz somefile.prof`` on your local computer to get an interactive view of the entire profile in a web browser.

Another useful tool for visualising the call graph is `gprof2dot <https://github.com/jrfonseca/gprof2dot>`_:

.. code-block:: bash

    gprof2dot -f pstats -e 0.01 cprofile-mosaic.dat | dot -Tpng -o cprofile-mosaic.png

.. _stack_profiling:

Stack profiling
===============

The LSST stack contains some support for obtaining a python profile easily:

* ``pipetask`` supports a ``--profile somefile.prof`` command-line argument to write the full run profile to the specified filename (``somefile.prof`` in this case).
* ``BatchCmdLineTask`` (the front-end to scripts such as ``singleFrameDriver.py`` in pipe_drivers) supports a ``--batch-profile`` command-line argument switch. The profile is written to ``profile-<job>-<hostname>-<pid>.dat``.
* `ci_hsc <http://github.com/LSST/ci_hsc>`_ (an integration test package, driven by SCons) supports a ``--enable-profile`` command-line argument specifying a base filename for the profiles (default is ``profile``). The profiles are written to ``<base>-<sequenceNumber>-<script>.pstats``. This is useful for profiling the entire stack.

All of the above profile outputs can be read using ``pstats``, ``snakeviz``, or other tools that support the ``cProfile`` output format.

.. _timing_decorator:

Note that our timing decorator--``lsst/utils/timer.py:timeMethod``, used to generate timing metrics metdata for Tasks--will result in a call graph that is difficult to interpret, due to every ``run()`` method being called by ``timeMethod_wrapper()``.
`DM-34978 <https://jira.lsstcorp.org/browse/DM-34978>`_ gives a plan for a workaround of this; until that is merged, you can try the branch of ``utils`` described on `DM-34881 <https://jira.lsstcorp.org/browse/DM-34881>`_ to disable the timer during your profiling run.

Line profiling
==============

Having found the particular function that's consuming all the time, you may want finer granularity.
For this, use `line profiler <https://pypi.python.org/pypi/line_profiler>`_.
Installation is a simple matter of:

.. code-block:: bash

   pip install line_profiler

Put an ``@profile`` decorator on the function of interest, and run:

.. code-block:: bash

   kernprof.py -l -v /path/to/script.py <arguments>
