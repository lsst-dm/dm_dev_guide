#######################################
Creating a compilation database
#######################################

``scons`` does not natively support the creation of a compilation database, instead the
``bear`` tool can be used (`bear repository  <https://github.com/rizsotto/Bear>`_) 
which is available on a number of Linux distributions (`bear packages <https://repology.org/project/bear/packages>`_) as well as
from conda-forge. A compilation database is a JSON file containing data on compiling each source code file in a project.

====================================
Install Bear from conda-forge
====================================
To install ``bear`` into an LSST Science Pipelines conda stack

.. code-block:: bash

    conda install -c conda-forge bear

=====================================================
Use Bear and Scons to create a compilation database
=====================================================

.. code-block:: bash

   bear -- scons

This will create ``compile_commands.json`` containing a list of all compilation commands that can be used in editors like :ref:`VSCode <vscode_extensions>` to analyze and navigate the code.
