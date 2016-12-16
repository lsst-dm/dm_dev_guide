.. _publication-policy:

#################################
Publishing Papers and Proceedings
#################################

Papers and conference proceedings written on behalf of the LSST Project are subject to the LSST Project Publication Policy (:lpm:`162`) and are coordinated by the Publication Board.
This page provides pointers to Publication Board documentation.

.. note::

   While scientific publications and conference proceedings are subject to :lpm:`162`, many types of DM communication and documentation are not controlled, including:

   - User guides (software documentation).
   - Technical notes.
   - Design documentation (though LDMs are coordinated by the DM Technical Control Team, TCT).
   - Community forum posts.

Links
=====

- `Publication Board homepage <https://project.lsst.org/documents/publication-board>`__.
- `LPM-162: LSST Project Publication Policy <https://www.lsstcorp.org/docushare/dsweb/Get/LPM-162/>`__.
- `Publication Board JIRA Project (PUB) <https://jira.lsstcorp.org/browse/PUB>`__.
- `Document-13016: Project Publications Style Manual <https://docushare.lsstcorp.org/docushare/dsweb/Get/Document-13016/LSSTStyleManual.pdf>`__.
- `lsst-pst/LSSTreferences <https://github.com/lsst-pst/LSSTreferences>`__ GitHub project with citations for key LSST papers.

Citing DM Technical Notes and Design Documents
==============================================

Wherever possible, cite DM design documentation and technotes in addition to the core project papers.
Rather than linking to the document's URL in a footnote, you should use a proper BibTeX citation.

For technotes, it's better to cite the technote's DOI than its lsst.io URL alone.
The documentation engineering team is making DOIs on an as-needed basis at the moment.
Reach out to `#dm-docs <https://lsstc.slack.com/archives/dm-docs>`__ for additional DOIs.
We're working on automating DOI provisioning to make this easier in the future.

Example design document citation
--------------------------------

A BibTeX citation for a design document:

.. code-block:: text

   @misc{LDM-135,
     author       = {Jacek Becla and others},
     title        = {{LSST Database Design}},
     howpublished = {LDM-135, \url{http://ls.st/LDM-135}},
     year         = 2013,
   }

Note that the ``ls.st`` short link points to the official DocuShare-archived version of LDM-135.

Example technical note citation
-------------------------------

A technote citation, pointing to a Zenodo-backed DOI:

.. code-block:: text

   @techreport{slater_2016_192828,
     title        = {{False Positive Rates in the LSST Image 
                      Differencing Pipeline}},
     author       = {{Slater}, Colin and
                     {Jurić}, Mario and
                     {Ivezić}, Željko and
                     {Jones}, Lynne},
     institution  = {{LSST Data Management}},
     type         = {{LSST Data Management Technical Note}},
     number       = {{DMTN-006}},
     month        = mar,
     year         = 2016,
     doi          = {10.5281/zenodo.192828},
     url          = {https://doi.org/10.5281/zenodo.192828}
   }

.. note::

   Zenodo offers citations using the ``manual``, rather than ``techreport``, BibTeX type for technical reports, but the example above is likely more complete.
   The publisher, given their BibTeX style file, may have different guidance.
