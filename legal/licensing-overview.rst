#########################################
Licensing LSST DM source code and content
#########################################

This page provides background information to help you appropriately license source code, documentation, and other types of content that is produced on behalf of LSST Data Management.

.. _choose-a-source-license:

Choosing a source code license
==============================

All source code created by LSST DM is publicly-available open source.
As such, LSST DM code must carry an `Open Source Initiative (OSI)-approved license`_.

Stack packages
--------------

A substantial amount of DM development is in the EUPS-managed "Stack," including the LSST Science Pipelines, Qserv, and DAX.
Stack packages are licensed under the `GNU Public License version 3.0 (GPL-3.0)`_ license.
Because of the interconnected nature of the Stack and how the `GPL-3.0`_ license works, you cannot create a new Stack package distributed with EUPS that is licensed under a different license.

.. seealso::

   :doc:`/stack/license-and-copyright`.

Standalone projects
-------------------

If your project is not part of the Stack, you have flexibility to choose a different `OSI-approved license`_.

For example, PyPI-distributed Python packages made by SQuaRE are licensed under the simpler and more-flexible MIT_ and `Apache 2.0`_ licenses.

To choose a license, you'll want to consider the norms of the open source community your project resides in.
The `choosealicense`_ site is useful for understanding the important qualities of different open source licenses.

Always consult with your manager before setting the license for a project to ensure it aligns with the project's goals.

.. _choose-a-doc-license:

Choosing a documentation license
================================

Documentation is often licensed differently from source code to make it easier to adapt and reuse in non-code contexts.

In general, all DM user documentation and technical notes are licensed under the `Creative Commons Attribution 4.0 International (CC-BY-4.0)`_.
This license balances the need for LSST DM to get attribution for content, while allowing the community to freely reproduce and adapt the information.

.. _apply-a-license:

Applying a license to a repository
==================================

When you create a new repository on GitHub you have the option of adding a :file:`LICENSE` in the initial set up.
You can also add a license later `through the GitHub UI <https://help.github.com/articles/adding-a-license-to-a-repository/>`__.
Not all OSI-approved licenses are available through the GitHub UI, though.

Alternatively, you can always apply a license by manually creating and committing a :file:`LICENSE` file in the root of the source code repository.
The content of the :file:`LICENSE` file should be the license text itself, without additions or alterations.

The easiest way to get the content of a license is by going to choosealicense_, finding the license's page, and clicking the **Copy license text to clipboard** button.

Some licenses include a copyright section.
See :doc:`copyright-overview` for details on how to properly record copyrights for DM software.

The package management ecosystems for many languages, including PyPI and NPM, provide metadata fields for recording license information.
These aren't legally binding, but you should make sure the package metadata are consistent with the :file:`LICENSE` file.

GitHub also includes license metadata for repositories that is determined automatically from the content of the :file:`LICENSE` file.
See :ref:`github-license-metadata`, below, for more information.

.. seealso::

   The `GPL-3.0`_ license used by Stack packages also require preambles in each source code file.
   See :doc:`/stack/license-and-copyright` for details.

.. _github-license-metadata:

Details on GitHub's license detection
=====================================

GitHub can detect a repository's license by matching the content of the :file:`LICENSE` file to known licenses in the choosealicense_ corpus.
When GitHub confidently detects a license, it displays the license on the repository's page.

Not only is this license badge a nice feature for the community, it also helps us validate our :file:`LICENSE` files to be sure that the :file:`LICENSE` we publish is in fact the license we think it is.
If the :file:`LICENSE` file is modified, aside from copyright lines, GitHub will not positively identify the license and will not show a license badge on the repository homepage.

If you have a repository where GitHub is not detecting a license, you can debug it by running GitHub's detection software on your own computer.
Install licensee_ and follow the `documentation <https://github.com/benbalter/licensee/blob/master/docs/command-line-usage.md>`__ to run it against your repository.

.. note::

   licensee_ looks at `multiple files, including COPYRIGHT <https://github.com/benbalter/licensee/blob/master/docs/what-we-look-at.md>`__, when it detects a license.
   If these files have conficting information, GitHub will not positively detect a license.
   Be aware of this issue when working with repositories that have both :file:`COPYRIGHT` and :file:`LICENSE` files.

.. note::

   GitHub may not properly detect the :file:`LICENSE` in repositories that have multi-institution :file:`COPYRIGHT` files.
   SQuaRE is aware of this issue and is working to resolve it.
   See licensee `issue #285 <https://github.com/benbalter/licensee/issues/285>`__ for background.

.. _`OSI-approved license`:
.. _`Open Source Initiative (OSI)-approved license`: https://opensource.org/licenses
.. _`GPL-3.0`:
.. _`GNU Public License version 3.0 (GPL-3.0)`: https://choosealicense.com/licenses/gpl-3.0/
.. _`Creative Commons Attribution 4.0 International (CC-BY-4.0)`: https://choosealicense.com/licenses/cc-by-4.0/
.. _`MIT`: https://choosealicense.com/licenses/mit/
.. _`Apache 2.0`: https://choosealicense.com/licenses/apache-2.0/
.. _choosealicense: https://choosealicense.com/
.. _licensee: https://github.com/benbalter/licensee
