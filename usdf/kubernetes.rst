########################
SLAC Kubernetes Overview
########################

Operations activities will be carried out at the SLAC US Data Facility (USDF). Where possible, all USDF services will reside on top of a kubernetes platform.

SLAC operates a single large kubernetes cluster. The benefits of this are with increased scale (sharing of resources) and reduced management overhead. We run 'vanilla' kubernetes, deployed via `kubeadm <https://github.com/kubernetes/kubeadm>`__. On top of this, to provide segregation and project control we use `loft.sh's vcluster <https://github.com/loft-sh/vcluster>`__. The latter provides a virtual kubernetes cluster from which we can provide a similar experience to `openshift's projects <https://docs.openshift.com/container-platform/4.6/applications/projects/working-with-projects.html>`__ or `GKE's projects and folders <https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy>`__.


SLAC Virtual Clusters, aka "Projects"
=====================================

- rubin-jenkins-control
- rubin-jenkins-workers
- usdf-alert-stream-broker-dev
- usdf-butler
- usdf-butler-dev
- usdf-cm
- usdf-cm-dev
- usdf-consdb
- usdf-consdb-dev
- usdf-embargo-dmz
- usdf-embargo-dmz-dev
- usdf-fts3-dev
- usdf-ingestd
- usdf-lfa
- usdf-lsst-camera
- usdf-maf
- usdf-minor-planet-survey
- usdf-opensearch
- usdf-panda
- usdf-panda-dev
- usdf-pg-catalogs
- usdf-prompt-processing
- usdf-prompt-processing-dev
- usdf-qserv
- usdf-rapid-analysis
- usdf-rapid-analysis-dev
- usdf-rsp
- usdf-rsp-dev
- usdf-rsp-int
- usdf-rubintv-broadcaster-cleanroom
- usdf-rucio
- usdf-rucio-dev
- usdf-summitdb
- usdf-tel-rsp

Requesting a new Project
========================

Please send a request to the LSSTC's #ops-usdf slack channel. Alternatively email usdf-help@slac.stanford.edu.

Requesting access to an existing Project
========================================

Ideally, have the project owner send a request to usdf-help@slac.stanford.edu.  Or you can send a request, and the project owner will be contacted.

Connecting and Authenticating
=============================

Generically:

- Determine the 'project' that you wish to access, eg usdf-butler
- Go to https://k8s.slac.stanford.edu/<project>
- Click 'Sign-In' to begin the authentication procedure
- Enter your SLAC credentials into the login page, and possibly your Duo 2Factor if requested. This step may automatically skip if you already have valid single sign on credentials in place already.
- Click on 'Grant Access' to agree to register
- The next page will provide details on installing kubectl (only needed once, if you don't already have it available via some other means) and, in the second box, relevant commands to run to register your kubectl to this project instance. Each box has a useful "Copy" button in the upper-right corner that you can access by hovering over the box. You can use kubectl config to switch between different projects.
- On the USDF interactive nodes, kubectl is already installed.  You may need to activate it with ``module load kubectl``.

We currently provide kubernetes API access without the need for VPNs etc. i.e. you should be able to connect from any machine anywhere (as long as it has internet access).


Miscellaneous
=============

- if you encounter an error like "Unable to connect to the server: No valid id-token, and cannot refresh without refresh-token" when running your kubectl, you will need to log back in via https://k8s.slac.stanford.edu/<project>, re-executing the commands in the second box. This is because our OIDC (dex) implementation does not and cannot generate refresh tokens from our SAML2 (windows ADFS) backend. (Actually, only the ``set-credentials`` command is needed, but it doesn't hurt to execute them all.)

Kubernetes secrets are usually held in Vault (vault.slac.stanford.edu).  The vault command is available on USDF interactive nodes.  You may need to activate it with ``module load vault``.  Then login using the commands ``export VAULT_ADDR=https://vault.slac.stanford.edu; vault login -method=ldap`` with your SLAC Windows password.  You can then use ``vault kv list -mount=secret rubin[/PATH]`` and ``vault kv get -mount=secret PATH/TO/SECRET`` to access secrets for which you have permission.
