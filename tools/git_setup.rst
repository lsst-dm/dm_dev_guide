############################
Git Setup and Best Practices
############################

This page collects best practices for configuration and using Git for DM development.

*See also*:

- :doc:`/processes/workflow` for our :ref:`official Git user.email configuration requirement <git-setup>` as well as policies for `Git branch naming <git-branching>` and :ref:`merging <workflow-code-review-merge>`.
- :doc:`/tools/git_lfs`

.. _git-learning-resources:

Learning Git
============

If you're new to Git, there are many great learning resources, such as

* `Git's online docs <http://git-scm.com/doc>`_, and the associated online `Pro Git <http://git-scm.com/book/en/v2>`_ book by Scott Chacon and Ben Staubb.
* `GitHub Help <https://help.github.com>`_, which covers fundamental git usage too.
* `StackOverflow <http://stackoverflow.com/questions/tagged/git?sort=frequent&pageSize=15>`_.

.. _git-github-2fa:

Setup Two-Factor Authentication (2FA) for GitHub
================================================

We encourage you to enable `Two-Factor Authentication (2FA) for GitHub <https://help.github.com/articles/about-two-factor-authentication/>`_ through your `account security settings <https://github.com/settings/security>`_.
2FA means that you'll have to enter an authentication code when logging into GitHub.com from a new computer.
Apps like `1Password <https://agilebits.com/onepassword>`_ (see their `guide <https://guides.agilebits.com/1password-ios/5/en/topic/setting-up-one-time-passwords>`_), `Authy <https://www.authy.com>`_, and the Google Authenticator App can help you generate these authentication codes.
When pushing commits with a 2FA-enabled account, you'll use a personal access token instead of your password.
You can `create and revoke tokens from your GitHub settings page <https://github.com/settings/tokens>`_.
To help you automatically authenticate when pushing to GitHub, we encourage you to follow the next step and enable a credential helper.

.. _git-credential-helper:

Setup a Git credential helper
=============================

Rather than entering your GitHub username and password (or 2FA access token) every time you push, you can setup a Git credential helper to manage this for you.
A credential helper is especially important for working with our :doc:`Git LFS-backed repositories </tools/git_lfs>`.

**Mac users** can use the secure OS X keychain:

.. code-block:: bash

   git config --global credential.helper osxkeychain  

**Linux users** can use a credential *cache* to temporarily keep credentials in memory.
To have your credentials cached for 1 hour (3600 seconds):

.. code-block:: bash

   git config --global credential.helper 'cache --timeout=3600'

**Linux users can alternatively** have their `credentials stored on disk <http://git-scm.com/docs/git-credential-store>`_ in a :file:`~/.git-credentials` file.
Only do this for machines where you can ensure some level of security.

.. code-block:: bash

   git config credential.helper store

Once a credential helper is enabled, the next time you ``git push``, you will add your credentials to the helper.

Remember that if you have 2FA enabled, you will create and use a `personal access token <https://github.com/settings/tokens>`_ instead of your GitHub password.

The DM Git LFS documentation has further information about :ref:`authenticating with our LFS storage backend <git-lfs-auth>`.

.. _git-shell-setup:

Tune your shell for Git
=======================

You can build an effective development environment and workflow by tuning your Git setup.
Here are some ideas:

1. `Add git status to your prompt <http://git-scm.com/book/en/v2/Git-in-Other-Environments-Git-in-Bash>`_.
2. `Enable shell autocompletion <http://git-scm.com/book/en/v2/Git-in-Other-Environments-Git-in-Bash>`_
3. `Craft aliases for common workflows <http://git-scm.com/book/en/v2/Git-Basics-Git-Aliases>`_.
4. Use `hub <https://hub.github.com>`_ to interact with GitHub features from the command line.

.. _git-editor-setup:

Setup your editor
=================

You'll want to configure your preferred editor (or its command line hook) as your Git editor.
For example:

.. code-block:: text

   git config --global core.editor "vim"
   git config --global core.editor "emacs"
   git config --global core.editor "atom --wait"
   git config --global core.editor "subl -n -w"

See `GitHub's help for setting up Atom and Sublime Text as Git editors <https://help.github.com/articles/associating-text-editors-with-git/>`_.

.. _git-aliases:

Useful Git aliases and configurations
=====================================

You can craft custom Git commands (aliases) in your :file:`~/.gitconfig` to refine your workflow.
When you run an alias (``git <alias> [arguments]``) the alias's name is effectively replaced with the alias's content in the command line statement.

Here are some aliases try in :file:`~/.gitconfig`:

.. use quotes on alias contents to make Pygments highlighter happy

.. code-block:: ini

   [alias]
       # List things
       tags = "tag -l"
       branches = "branch -a"
       remotes = "remote -v"

       # Shorten common commands
       co = "checkout"
       st = "status"
       br = "branch"
       ci = "commit"
       d = "diff"

       # Log that shows titles of last 16 commits
       l = "log -16 --color=always --all --topo-order --pretty='%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"

       # Log that starts a pager with titles of all the commits in your tree
       ll = log --color=always --all --topo-order --pretty='%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

       # Log that shows the last 10 commits as a graph
       lg = "log -10 --color=always --all --graph --topo-order --pretty='%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative"

       # Log that shows all commits as a graph (using a pager)
       lgl = "log --color=always --all --graph --topo-order --pretty='%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

       # Show outgoing commits
       out = "log @{u}.."

       # Print the title of the current branch; sometimes useful for scripting
       currentbranch = "!git branch --contains HEAD | grep '*' | tr -s ' ' | cut -d ' ' -f2"

       # Better diffs for prose
       wdiff = "diff --color-words"

       # Safer pulls; don't do anything other than a fast forward on merge
       pull = "pull --ff-only"

       # Amend last commit without modifying commit message
       amend = "!git log -n 1 --pretty=tformat:%s%n%n%b | git commit -F - --amend"

       # Create a commit that will be automatically squashed as a fixup when you
       # run `git rebase --autosquash`
       fixup = "commit --fixup=HEAD"
