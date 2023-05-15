#############
Using Astropy
#############

.. note::

   Changes to this document must be approved by the System Architect (`RFC-24 <https://jira.lsstcorp.org/browse/RFC-24>`_).
   To request changes to these policies, please file an :doc:`RFC </communications/rfc>`.

.. _cpp_using_astropy:

Integration of Astropy core into the LSST software stack is an ongoing process that will evolve over time as we work on enhancing interoperability of the current codebase with Astropy.
This document is not discussing Astropy affiliated packages, use of which must go through the standard :doc:`RFC </communications/rfc>` process.
Not all Astropy core packages can be used by default.

The following packages can be used internally in packages if they do not leak into public APIs:

* :mod:`astropy.coordinates`
* :mod:`astropy.time`
* :mod:`astropy.table`
* :mod:`astropy.units`
* :mod:`astropy.units.quantity`
* :mod:`astropy.constants`
* :mod:`astropy.cosmology`
* :mod:`astropy.visualization`

For reading and writing files in FITS format, both :mod:`astropy.io.fits` and `fitsio`_ are allowed.
These libraries differ in the features available and in performance (with the latter usually surpassing the former).
Developers must evaluate which works best for their use case and choose one accordingly.

.. _fitsio: https://github.com/esheldon/fitsio

.. warning::

    ``lsst.afw.fits`` must not be used in any new Python code, as it is not considered memory safe.

The interaction of Astropy with LSST C++ classes providing related functionality should be carefully monitored.
If the code is already using ``afw`` it is strongly preferred that ``afw`` equivalents be used until such time as specific ``afw`` interfaces are deprecated.
:mod:`astropy.table` views into ``afw.table`` tables can be used if required.

Changing public APIs to use the above Astropy packages requires prior permission and possibly an :doc:`RFC </communications/rfc>`.

These items have functionality that is similar to that provided in LSST packages:

* :mod:`astropy.modeling`
* :mod:`astropy.convolution`
* :mod:`astropy.wcs`
* :mod:`astropy.stats`
* :mod:`astropy.nddata`

They are not allowed to be used in LSST code without special permission, such as submitting an :doc:`RFC </communications/rfc>`.

This advice will evolve as interoperability with Astropy develops.
