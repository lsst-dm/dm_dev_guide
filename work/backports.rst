#######################################
Backporting Tickets to a Release Branch
#######################################

So you have a ticket that you think should be backported to ``v23.0.0`` and/or be used for DP0.2.
What next?

1) First, add the label "backport-v23" to your jira ticket.
   This will flag it for review by both the CCB and the DP0.2 campaign managers.
   Continue merging your ticket to the default branch (``main``) and mark the ticket ``Done`` per instructions in the normal :doc:`flow`.

2) Wait for approval. The ticket will gain the label "backport-approved."  A comment will be posted on the ticket that you may start the backporting process.

3) Checkout the release branch, ``v23.0.x``, for each repo affected by your ticket.

   .. code-block:: bash

      git checkout v23.0.x

   If the repo does not already have a ``v23.0.x`` branch, you need to create one based on ``v23.0.0.rc1`` (not the latest rcN, although that should be identical):

   .. code-block:: bash

      git checkout v23.0.0.rc1
      git checkout -b v23.0.x
      git push -u origin v23.0.x

   Now treat ``v23.0.x`` same as you would the default branch (``main``).

4) Create a copy of your ticket branch called ``tickets/DM-XXXXX-v23``.

   .. code-block:: bash

      git checkout tickets/DM-XXXXX
      git checkout -b tickets/DM-XXXXX-v23
      git rebase --onto v23.0.x <sha_of_last_commit_before_your_branch>


   In a new clone, this branch may not exist anymore if you have already merged your PR because merged branches may be automatically deleted.
   In this case, you can branch ``tickets/DM-XXXXX-v23`` from ``v23.0.x``, and cherry-pick the ticket commits.

   .. code-block:: bash

      git checkout v23.0.x
      git checkout -b tickets/DM-XXXXX-v23
      git cherry-pick <ticket commit>

   The following may help you find your hash[es] from ``main``:
   ``git show --quiet $(git log --oneline | grep 'Merge.*DM-XXXXX' | cut -d' ' -f1)^2``

5) Resolve any rebase or cherry-pick problems depending on your method.
   Check that it cleanly builds via scons. There should be a latest shared v23.0.0.rcN stack on lsst-devl.
   Run Jenkins. When running Jenkins, build against the release branch and rc1 even if later rcNs exist:

   .. code-block:: bash

      REFS: tickets/DM-XXXXX-v23 v23.0.x v23.0.0.rc1
      PRODUCTS: lsst_distrib lsst_ci ci_imsim ci_hsc

   You may find that the ticket cannot be cleanly backported without first backporting another ticket.

6) When it passes, merge to ``v23.0.x`` using the same procedure outlined in :doc:`flow` including creating a PR.
   If the backport was clean, you may self-review.
   When merged to ``v23.0.x``, label your Jira ticket ``backport-done``.


Interaction between v23 and DP0.2
---------------------------------
Before the full-scale data release processing of step1 commences for DP0.2, a new rcN release will be built on approximately weekly cadence.
This weekly cadence follows the weekly review of backport requests.

After step1 begins and 23.0.0 is released, the current plan is to increment the release versions.
This backporting process will remain the same, but with evolving release tags and release branch numbers.
