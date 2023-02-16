#######################################
Backporting Tickets to a Release Branch
#######################################

So you have a ticket that you think should be backported to a previous release.
What next?

1) First, add the label "backport-v23" to your jira ticket, replacing "23" here and elsewhere on this page with the actual release you're targeting.
   To backport to multiple releases, add multiple labels.

   This will flag it for review by the DM-CCB.
   Continue merging your ticket to the default branch (``main``) and mark the ticket ``Done`` per instructions in the normal :doc:`flow`.

2) Wait for approval.
   The ticket will gain the label "backport-approved."
   A comment will be posted on the ticket that you may start the backporting process.
   Backports are approved for all requested releases together.

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
   Continue using the same procedure outlined in :ref:`review-preparation`.
   Check that it cleanly builds via scons. There should be a latest shared v23.0.0.rcN stack on lsst-devl.
   Run Jenkins. When running Jenkins, build against the release branch and rc1 even if later rcNs exist.
   The default ``SPLENV_REF`` value (the rubin-env conda metapackage version) may no longer be appropriate for ``v23.0.x``.
   If you are unsure of the recommended env for the release, see the :external+pipelines:ref:`release documentation page <release_history>` or check with the release manager.

   .. code-block:: bash

      REFS: tickets/DM-XXXXX-v23 v23.0.x v23.0.0.rc1
      PRODUCTS: lsst_distrib lsst_ci ci_imsim ci_hsc
      SPLENV_REF: 0.8.0

   You may find that the ticket cannot be cleanly backported without first backporting another ticket.

6) When it passes, merge to ``v23.0.x`` using the same procedure outlined in :ref:`workflow-code-review-merge`,
   including creating a pull request.
   On your pull request, remember to change the base branch to ``v23.0.x``.
   If the backport was clean, you may self-review.
   If the backport was not clean and you would like another pair of eyes, you may ask someone to hit the "Approved" button on GitHub,
   but please *do not* put your ticket status back into ``In Review`` on Jira.

7) When a ticket has been backported to all requested releases, label your Jira ticket ``backport-done``.
