.. _stack-dev-workflow:

###############################
LSST Stack Development Workflow
###############################

This page describes a complete workflow for developing the LSST Stack:

1. Obtaining a development stack with lsstsw,
2. Creating a ticket on JIRA,
3. Publishing your code changes with git,
4. Testing your code with Jenkins,
5. Code review and merging, and
6. Maintaining your development stack with lsstsw.

.. _obtaining-lsstw-stack:

Obtaining a development stack with lsstsw
=========================================

Developing for The LSST Stack is exceptional in that code is distributed across many git repositories.
`lsstsw <https://github.com/lsst/lsstsw>`_ is a tool that automates the processing of cloning all of these repositories of development and building that development stack for testing.

.. code-block:: bash

   git clone git@github.com:lsst/lsstsw.git
   cd lsstsw

Edit the file lsstsw/etc/repos.yaml to change all instances of `https://github.com/lsst` to `git@github.com:lsst`. This will allow you to more easily push your changes to any GitHub package.

.. code-block:: bash

   ./bin/deploy

.. code-block:: bash

   export LSSTSW=<where you've set it up>
   export EUPS_PATH=$LSSTSW/stack
   . $LSSTSW/bin/setup.sh

.. code-block:: bash

   rebuild lsst_apps

.. code-block:: bash

   eups tags --clone bNNNN current
