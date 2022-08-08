########################
SLAC Kubernetes Overview
########################

Operations activities will be carried out at the SLAC US Data Facility (USDF). Where possible, all USDF services will reside on top of a kubernetes platform.

SLAC operates a single large kubernetes cluster. The benefits of this are with increased scale (sharing of resources) and reduced management overhead. We run 'vanilla' kubernetes, deployed via `kubeadm <https://github.com/kubernetes/kubeadm>`__. On top of this, to provide segregation and project control we use `loft.sh's vcluster <https://github.com/loft-sh/vcluster>`__. The latter provides a virtual kubernetes cluster from which we can provide a similar experience to `openshift's projects <https://docs.openshift.com/container-platform/4.6/applications/projects/working-with-projects.html>`__ or `GKE's projects and folders <https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy>`__.


SLAC Virtual Clusters, aka "Projects"
=====================================

TODO: enumeration of vclusters, based upon established hierachy on IDF

- usdf-butler
- usdf-staffrsp-dev


Requesting a new Project
========================

Please send a request to the LSSTC's #ops-usdf slack channel. Alternatively email usdf-help@slac.stanford.edu.


Connecting and Authenticating
=============================

Generically:

- Determine the 'project' that you wish to access, eg usdf-butler
- Goto https://k8s.slac.stanford.edu/<project>
- Click 'Sign-In' to begin the authentication proceedure
- Enter your SLAC credentials into the login page, and possibly your Duo 2Factor if requested. This step may automatically skip if you already have valid single sign on credentials in place already.
- Click on 'Grant Access' to agree to register
- The next page will provide details on installing kubectl and relevant commands to run to register your kubectl to this project instance. You can use kubectl config to switch between different projects.

We currently provide kubernetes API access without the need for VPNs etc. ie you be able to connect from any machine anywhere (as long as it has internet access).


Miscellaneous
=============

- if you encounter an error like "Unable to connect to the server: No valid id-token, and cannot refresh without refresh-token" when running your kubectl, you will need to log back in via https://k8s.slac.stanford.edu/<project>. This is because our OIDC (dex) implementation does not and cannot generate refresh tokens from our SAML2 (windows ADFS) backend.

