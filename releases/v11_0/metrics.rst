#################################
Characterization Metrics for 11.0
#################################

Starting from Summer 2015, administrative ("cycle") releases are
accompanied by a measurements report characterising the current
performance. Metrics included in these reports are expected to increase
in number and sophistication at subsequent releases. This brief report
describe measurements of interest that were carried out.

Summary of Photometric Repeatability Measurements
=================================================

*Submitted by Jim Bosch*

This dataset is a selection of i-band HyperSuprime-Cam engineering data
taken in the SDSS Stripe 82 region. This dataset consists of 30s
exposures, so it is somewhat similar to projected LSST data in depth.
Our current calibration approach has many limitations relative to what
we ultimately plan to implement for LSST:

-  There's currently no relative calibration being run at all.
-  We have only limited correction for chromatic effects.
-  There's's currently no allowance for zeropoint variations smaller
   than the scale of a CCD
-  We also use a much simpler sample selection than that proposed by the
   SRD

*   * Annotated code to compute the metrics can be found at
https://github.com/lsst/afw/blob/tickets/DM-3896/examples/repeatability.ipynb.

+------------------------------------------+-----------------------------------------------------------+-------------+------------------+------------------------------------------------------------------------------+
| Metric Characterised                     | Metric Ref                                                | Target      | Measured Value   | Measurement Method                                                           |
+==========================================+===========================================================+=============+==================+==============================================================================+
| Photometric repeatability (procCalRep)   | `DLP-307 <https://jira.lsstcorp.org/browser/DLP-307>`__   | ≤ 13 mmag   | 10.6 mmag        | `DM-3338 <https://jira.lsstcorp.org/browse/DM-3338>`__ (using i band data)   |
+------------------------------------------+-----------------------------------------------------------+-------------+------------------+------------------------------------------------------------------------------+
| Photometric repeatability (PA1gri)       | `DLP-315 <https://jira.lsstcorp.org/browse/DLP-315>`__    | ≤ 13 mmag   | 10.6 mmag        | `DM-3338 <https://jira.lsstcorp.org/browse/DM-3338>`__                       |
+------------------------------------------+-----------------------------------------------------------+-------------+------------------+------------------------------------------------------------------------------+
| Photometric repeatability (PA1uzy)       | `DLP-316 <https://jira.lsstcorp.org/browse/DLP-316>`__    | ≤ 13 mmag   | 10.6 mmag        | `DM-3338 <https://jira.lsstcorp.org/browse/DM-3338>`__ (using i band data)   |
+------------------------------------------+-----------------------------------------------------------+-------------+------------------+------------------------------------------------------------------------------+

Summary of Algorithmic Performance Measurements
===============================================

*Submitted by John Swinbank*

The i-band HSC engineering data (described above) was used where
possible and the same caveats apply. Consult the tickets in the
Measurement Method column for more details.

+-----------------------------------------------+----------------------------------------------------------+------------+------------------+----------------------------------------------------------+
| Metric Characterised                          | Metric Ref                                               | Target     | Measured Value   | Measurement Method                                       |
+===============================================+==========================================================+============+==================+==========================================================+
| Residual PSF Ellipticity Correlations (TE1)   | `DLP-290 <https://jira.lsstcorp.org/browse/DLP-290>`__   | ≤ 5e-3     | 6e-5             | `DM-3040 <https://jira.lsstcorp.org/browse/DM-3040>`__   |
+-----------------------------------------------+----------------------------------------------------------+------------+------------------+----------------------------------------------------------+
| Residual PSF Ellipticity Correlations (TE2)   | `DLP-290 <https://jira.lsstcorp.org/browse/DLP-290>`__   | ≤ 5e-3     | 2e-5             | `DM-3047 <https://jira.lsstcorp.org/browse/DM-3047>`__   |
+-----------------------------------------------+----------------------------------------------------------+------------+------------------+----------------------------------------------------------+
| Relative Astrometry (AM1)                     | `DLP-310 <https://jira.lsstcorp.org/browse/DLP-310>`__   | < 60 mas   | 12.49 mas        | `DM-3057 <https://jira.lsstcorp.org/browse/DM-3057>`__   |
+-----------------------------------------------+----------------------------------------------------------+------------+------------------+----------------------------------------------------------+
| Relative Astrometry (AM2)                     | `DLP-311 <https://jira.lsstcorp.org/browse/DLP-311>`__   | < 60 mas   | 12.19 mas        | `DM-3064 <https://jira.lsstcorp.org/browse/DM-3064>`__   |
+-----------------------------------------------+----------------------------------------------------------+------------+------------------+----------------------------------------------------------+

Summary of Computational Performance Measurements
=================================================

*Submitted by John Swinbank and Simon Krughoff*

At this point of Construction, the computational performance
measurements are a combination of precursor data processing and
extrapolation from R&D assumptions.

DECam/HITS data was used for the OTT1 estimate and for the diffim and
single-frame measurement of the Alert Production Computational Budget in
combination with data from the `3rd Data
Challenge <https://dev.lsstcorp.org/trac/wiki/DC3bPT1_1>`__.

For the Data Release Production of the computational budget, we used
DECam/HITS data for estimating diffim performance, HSC-I for assembling
and measuring coadds and for forced measurement, estimates from FDR for
multifit, and data from the 3rd Data Challenge for SDQA. Calculations
for the DRP computational budget used `this iPython
notebook <https://github.com/lsst-dm/kpm/blob/29c053f7b832e8bd999527e012681826fc0c201c/DLP-314:%20DRP%20Computational%20Budget/LSST%20DRP%20Computational%20Budget.ipynb>`__.

+----------------------------+----------------------------------------------------------+----------------+------------------+----------------------------------------------------------+
| Metric Chracterised        | Metric Ref                                               | Target         | Measured Value   | Measurement Method                                       |
+============================+==========================================================+================+==================+==========================================================+
| OTT1                       | `DLP-328 <https://jira.lsstcorp.org/browse/DLP-328>`__   | ≤ 240 sec      | 200-250 sec      | `DM-3724 <https://jira.lsstcorp.org/browse/DM-3724>`__   |
+----------------------------+----------------------------------------------------------+----------------+------------------+----------------------------------------------------------+
| AP Computational Budget    | `DLP-329 <https://jira.lsstcorp.org/browse/DLP-329>`__   | ≤ 231 TFLOPS   | 34-39 TFLOPS     | `DM-3267 <https://jira.lsstcorp.org/browse/DM-3267>`__   |
+----------------------------+----------------------------------------------------------+----------------+------------------+----------------------------------------------------------+
| DRP Computational Budget   | `DLP-314 <https://jira.lsstcorp.org/browse/DLP-314>`__   | ≤ 645 TFLOPS   | 318 TFLOPS       | `DM-3083 <https://jira.lsstcorp.org/browse/DM-3083>`__   |
+----------------------------+----------------------------------------------------------+----------------+------------------+----------------------------------------------------------+

