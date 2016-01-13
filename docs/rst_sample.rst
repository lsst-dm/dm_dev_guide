#######################
ReStructuredText Sample
#######################

ReStructuredText is an *extensible* markup language used by `LSST`_.

.. _LSST: http://lsst.org

ReStructuredText provides basic *italic*, **bold** and ``monospaced``
typesetting.  There is also the concept of **roles** that provide sophisticated
typsetting, such as :math:`\mu = -2.5 \log_{10}(\mathrm{DN} / A) + m_0`, and
:ref:`referencing <rst-internal-links>`.

.. _label-for-subsection-label:

Sectioning
----------

Sections are formed with underlining the headline text. We use :ref:`a
conventional sequence of underline symbols <rst-sectioning>` to indicate
different levels of hierarchy.

Directives
----------

Besides **roles** that are used for inline markup, reStructuredText has the
concept of **directives** to markup *blocks* of content. One example is the is
the ``code-block`` directive:

.. code-block:: python

   print('hello world!')
