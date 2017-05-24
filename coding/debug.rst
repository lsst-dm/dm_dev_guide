##################################
Debugging Tasks with ``lsstDebug``
##################################

.. note::

   See also the `Doxygen documentation on lsstDebug <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/base_debug.html>`_.

In your ``Task`` code, if you ``import lsstDebug`` then call::

   debug = lsstDebug.Info(__name__)

(with ``__name__`` being the name of the current ``Task``), you are given a “debug object”.
By default that will simply give you a ``False`` for any attribute you access.
Thus::

   >>> debug.foo
   False

   >>> debug.bar
   False

   >>> debug.display
   False

The aim is to customize the behaviour of ``debug`` to meet your particular needs.
In this, you want to define a function that, when called with ``__name__``, as an argument will provide non-``False`` values for certain combinations of ``__name__`` and attribute.
Thus, you can do things like::

   >>> debug = lsstDebug.Info(__name__)  # __name__ selects the current task
   >>> debug.display
   True

Then you can write your task to optionally enable a display (or whatever) by doing something like::

   if debug.display:
      afwDisplay.getDisplay()....
   else:
      self.log.debug("I would show you a pretty picture here if you enabled debugging.")

Refer to the `task documentation <http://doxygen.lsst.codes/stack/doxygen/x_masterDoxyDoc/group___l_s_s_t__task__documentation.html>`_ and look for “debug variables” to discover what debugging options are available for existing ``Task``\s.

In order to load your specific debugging configuration, create a ``debug.py`` in your working directory, and put something like this in it::

   import lsstDebug
   def DebugInfo(name):
       debug = lsstDebug.getInfo(name)
       if name == "lsst.meas.astrom.astrometry":
           debug.display = True
       return debug

   lsstDebug.Info = DebugInfo

That should enable debugging the ``display`` attribute when you are running inside ``lsst.meas.astrom.astrometry``, and disable it elsewhere.
Of course, you can also return arbitrarily more complex objects, doing things like specifying the frame to display on etc.

You must use the ``--debug`` command line argument to ask a command line task to import your :file:`debug.py` file.
