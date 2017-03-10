Orchestration FAQ
=================

Q.  Why am I get the following error when I try and setup ctrl_execute?

    .. code-block:: shell

       $ setup ctrl_execute
       Unable to find an acceptable version of ctrl_execute

A.  You're using a stack that includes only the **lsst_apps** distribution. The
packages required to use **ctrl_execute**, **ctrl_orca**, etc. are included in
the **lsst_distrib** distribution.  You can install the latest version here:
 
.. prompt:: bash

   eups distrib install -t w_2015_40 lsst_distrib

.. note::

   Note that w_2015_40 is the most current version as of this writing.
 
.. note::

   The distribution tagged v11_0 does not contain the most current version of
   ctrl_orca;  if you try and use that version, you'll get the error shown in
   the next question...

Q.  I received the following error when I tried to execute the "runOrca.py"
command in the v11_0 lsst_distrib install.  What happened?

.. code-block:: shell

   Traceback (most recent call last):
     File "/ssd/srp/lsstsw/Linux64/ctrl_orca/11.0/bin/Logger.py", line 80, in <module>
       receiver = events.EventReceiver(broker, events.EventLog.LOGGING_TOPIC, "RUNID='%s'" % runid)
   AttributeError: 'module' object has no attribute 'EventLog'

A.  The cutoff for v11.0 of the stack during the time when updates to the
``ctrl_orca`` package were in review.  The master branch of ``ctrl_orca`` has
the version you need to use.  You can get it by installing

.. prompt:: bash

   eups distrib install -t w_2015_40 lsst_distrib

or by installing

.. code-block:: shell
 
   ctrl_execute         11.0-1-ga3bec3e+1
   ctrl_orca            11.0-1-g0f12d57+10

Please note that if you still encounter this error, it's likely you've
overridden the setup of **ctrl_orca** by setting up **ctrl_execute**
afterwards.  Using the ``-j`` option, and setting ctrl_orca last will set up
that package and leave other dependencies in place.
