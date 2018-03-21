########################################
Emacs Configuration for LSST Development
########################################

This page will help you configure Emacs to be consistent with LSST's coding standards and development practices.

..
  The config repo mentioned in this section does not exist.

  .. _emacs-cpp-mode:

  C++
  ===

  There is an Emacs mode to help you write code that conforms to the DM coding style..
  At present, it only knows about C++.
  Fetch it from the repository:

  .. code-block:: bash

     git clone git://git.lsstcorp.org/LSST/DMS/devenv/build.git

  Look for :file:`editors/lsst.el`.
  There are also some handy functions defined in :file:`editors/lsst-utils.el` as well; activate them in your :file:`~/.emacs` resource file:

  .. code-bock:: text

     (load "lsst")
     (load "lsst-utils")
     (let ( (lsst t) (width 110) )
       (if lsst
           (lsst-c++-default))

       (if (and lsst window-system)
           (progn
             (set-default 'fill-column width)
             (set-frame-width default-minibuffer-frame (1+ width))
             ;; ` quotes, but evaluates ,width
             (add-hook 'after-make-frame-functions
                       `(lambda (frame)
                          (set-frame-width frame (1+ ,width))))
             ))
       )

     (add-hook 'lsst-c++-mode-hook
               '(lambda ()
                  (define-key c-mode-base-map "\e\C-a" 'c-beginning-of-defun)
                  (define-key c-mode-base-map "\e\C-e" 'c-end-of-defun)))
     (add-hook 'lsst-c++-mode-hook
               '(lambda ()
                  (define-key c-mode-base-map "\C-c>" 'indent-region)
                  (define-key c-mode-base-map "\C-c<" 'indent-region)))

.. _emacs-python-mode:

Python
======

The standard python-mode works well, but here are some potentially useful customizations for your :file:`~/.emacs`.
Some are also useful in other languages, and so are implemented globally.

.. _emacs-python-whitespace:

Whitespace
----------

In python it's especially important to turn off *TABs*; but they're annoying generally, so to turn them off globally:

.. code-block:: text

   ;; Use spaces instead of tabs
   (setq-default indent-tabs-mode nil)

It's handy to be able to see annoying whitespace (TABs and trailing whitespace):

.. code-block:: text

   ;; Highlight trailing whitespace
   (setq-default show-trailing-whitespace t)

   ;; Show tabs in Python; adapted from http://www.emacswiki.org/emacs/ShowWhiteSpace
   (defface nasty-tab-face
     '((t (:background "red"))) "Used for tabs.")
   (defvar nasty-tab-keywords
     '(("\t" . 'nasty-tab-face)))
   (add-hook 'python-mode-hook
             (lambda () (font-lock-add-keywords nil nasty-tab-keywords)))

   (custom-set-faces
    ;; Your init file should contain only one instance of custom-set-faces.
    ;; If there is more than one, they won't work right.
    '(trailing-whitespace ((t (:background "misty rose"))))
   )

If there are :file:`TABs` in your file, you can get rid of them with this function:

.. code-block:: text

   ;; Remove tabs from files, from http://www.jwz.org/doc/tabs-vs-spaces.html
   (defun code-untabify ()
     (save-excursion
       (goto-char (point-min))
       (while (re-search-forward "[ \t]+$" nil t)
         (delete-region (match-beginning 0) (match-end 0)))
       (goto-char (point-min))
       (if (search-forward "\t" nil t)
       (untabify (1- (point)) (point-max))))
     nil)

.. _emacs-python-pdb:

Python debugger: pdb
--------------------

It's common to want to insert a :command:`pdb` trigger in the code (i.e., you get a :command:`pdb` prompt when the code hits the trigger).
The following snippet allows you to do this with the function key (:kbd:`F8`):

.. code-block:: text

   ;; Insert pdb trigger
   (defun insert-pdb () (interactive)
     (newline-and-indent)
     (newline-and-indent)
     (newline-and-indent)
     (insert "import pdb;pdb.set_trace()\n")
     (newline-and-indent)
     (newline-and-indent)
     )
   (add-hook 'python-mode-hook
             (lambda () (define-key python-mode-map [f8] 'insert-pdb))
             )

It's most easily undone by :kbd:`Control _`.

.. _emacs-python-pyflakes:

Pyflakes
--------

`pyflakes <https://github.com/pyflakes/pyflakes/>`_ validates python files, allowing you to find problems before you run your script in earnest.
Having installed pyflakes (:command:`pip install pyflakes`), add the following to your :file:`~/.emacs` resource file so you can run pyflakes on the current buffer (by hitting :kbd:`F5`).

.. code-block:: text

   ;; pyflakes (https://pypi.python.org/pypi/pyflakes) for validating python
   (defun pyflakes-run-delete (filename) (interactive)
     (compile (format "pyflakes %s ; rm %s" filename filename))
     )
   (defun pyflakes-thisbuffer () (interactive)
     (let* ((buffer (current-buffer))
            (filename (buffer-file-name (current-buffer)))
            (tempname (concat filename "flakes"))
            )
       (with-temp-file tempname
         (insert-buffer buffer)
         (if (tramp-handle-file-remote-p tempname)
             (with-parsed-tramp-file-name tempname pyflakes
               (pyflakes-run-delete pyflakes-localname)
               )
           (pyflakes-run-delete tempname)
           )
         )
       )
     )

   (define-minor-mode pyflakes-mode
       "Toggle pyflakes mode.
       With no argument, this command toggles the mode.
       Non-null prefix argument turns on the mode.
       Null prefix argument turns off the mode."
       ;; The initial value.
       nil
       ;; The indicator for the mode line.
       " pyflakes"
       ;; The minor mode bindings.
       '( ([f5] . pyflakes-thisbuffer) )
   )
   (add-hook 'python-mode-hook (lambda () (pyflakes-mode t)))

*Actually, the above snippet is slightly buggy: run it twice to get it to work once...*

.. _emacs-python-jedi:

Jedi
----

`Jedi <http://jedi.jedidjah.ch/en/latest/>`_ provides auto-completion and documentation popups for python.
It seems a little buggy: at least, the relation between jedi itself and the auto-complete module isn't clear, and some features like the popup window are actually coming from auto-complete.
Installing it is a bit more complicated than usual:

1. Ensure that the emacs Package module is set up; :ref:`see instructions below <emacs-general-package>`.
2. In :command:`emacs`, do

   .. code-block:: text

      M-x package-refresh-contents <RET>
      M-x package-install <RET>
      jedi <RET>

3. Once that's built, you need to install the python dependencies:

   .. code-block:: text

      pip install -r ~/.emacs.d/elpa/jedi-0.1.2/requirements.txt

Then activate and configure it in your :file:`~/.emacs`:

.. code-block:: text

   ;; Auto-Complete: required for Jedi
   (require 'auto-complete)
   (add-hook 'python-mode-hook 'auto-complete-mode)
   (setq ac-auto-show-menu nil);3.0)
   (define-key ac-mode-map (kbd "<C-tab>") 'auto-complete)

   ;; Jedi: https://github.com/tkf/emacs-jedi for python auto-completion
   (setq jedi:setup-keys t)
   (add-hook 'python-mode-hook 'jedi:setup)
   ;(setq jedi:complete-on-dot t)
   (setq jedi:key-complete (kbd "C-`")) ; Keybind for command jedi:complete (C-TAB)
   ;(setq jedi:key-goto-definition (kbd "C-.")); Keybind for command jedi:goto-definition (C-.)
   ;(setq jedi:goto-definition-pop-marker (kbd "C-,")) ; Goto the last point where goto-definition was called. (C-,
   (setq jedi:key-show-doc (kbd "C-/")) ; Keybind for command jedi:show-doc (C-C d)
   ;(setq jedi:key-related-names (kbd "C-c r")); Keybind for command helm-jedi-related-names or anything-jedi-related-names (C-c r)

Besides the auto-completion feature, this provides four potentially useful commands:

:kbd:`C-TAB`
   Popup a window with multiple autocomplete suggestions
:kbd:`C-.`
   Open a window with the definition of the symbol under the cursor (easier and faster than TAGS)
:kbd:`C-,`
   Having done the above, go back to where you were
:kbd:`C-/`
   Show documentation for the symbol under the cursor.

See the `Jedi docs <http://tkf.github.io/emacs-jedi/#jedi:tooltip-method>`_ and `auto-complete docs <https://github.com/auto-complete/auto-complete/blob/master/doc/manual.md>`_ for further configuration options, and be prepared to spend some time tweaking it.

.. _emacs-general:

General
=======

Here are some miscellaneous additions to your :file:`~/.emacs` file that may be useful.

.. _emacs-general-uniquify:

Uniquify
--------

Makes buffer names unique, not by the usual method of appending ``<2>``, etc., but by appending a path element.
That way, you've got some chance of knowing what's what.

.. code-block:: text

   (load "uniquify")
   (custom-set-variables
    ;; Your init file should contain only one instance of custom-set-variables.
    ;; If there is more than one, they won't work right.
    '(uniquify-after-kill-buffer-p t)
    '(uniquify-buffer-name-style (quote post-forward) nil (uniquify))
   )

.. _emacs-general-tramp:

Tramp
-----

`Tramp <http://www.gnu.org/software/tramp/>`_ allows you to edit remote files on a local emacs.
For example, open file :file:`/remotemachine:/path/to/file.txt` (replacing ``remotemachine`` with the appropriate machine name).
There are ways to specify different user names and passwords, but no need if you've set that up via an ssh config file.

.. code-block:: text

   ;; Tramp (http://www.emacswiki.org/emacs/TrampMode) for remote files
   (require 'tramp)
   (add-to-list 'tramp-remote-path 'tramp-own-remote-path) ;; ensure PATH is set correctly, for compiling etc.
   (setq tramp-default-method "ssh")
   ;; Backup (file~) disabled and auto-save (#file#) locally to prevent delays in editing remote files
   (add-to-list 'backup-directory-alist
                (cons tramp-file-name-regexp nil))
   (setq tramp-auto-save-directory temporary-file-directory)
   ;;(setq tramp-verbose 10) ;; useful for debugging tramp

.. _emacs-general-package:

Package
-------

Emacs has a module library called `ELPA <http://tromey.com/elpa/>`_ (similar to PyPI for python and CPAN for perl; there are actually several different module libraries that share a common interface).
The package installer is distributed with Emacs 24, but if you have an earlier version, you'll need to `install it yourself <http://tromey.com/elpa/install.html>`_.
Then set it up and configure it:

.. code-block:: text

   ;; Emacs package installer
   (require 'package)
   (add-to-list 'package-archives
       '("marmalade" .
         "http://marmalade-repo.org/packages/"))
   (package-initialize)

.. _emacs-general-paren-matching:

Paren matching
--------------

While there are modules (e.g., `autopair <https://github.com/capitaomorte/autopair>`_) that will automatically insert a matching close paren when you type an open paren (or quotes) you might prefer to type it yourself, and just be informed where the matching one is (so you can be sure you're closing the correct one).

.. code-block:: text

   ; paren-matching
   (setq show-paren-delay 0.3)         ; how long to wait?
   (show-paren-mode t)                 ; turn paren-mode on
   (setq show-paren-style 'mixed)      ; 'expression', 'parenthesis' and 'mixed'
   ;(set-face-background 'show-paren-match-face "#aaaaaa")
   ;(set-face-attribute 'show-paren-match-face nil
   ;        :weight 'bold :underline nil :overline nil :slant 'normal)
   ;(set-face-foreground 'show-paren-mismatch-face "red")
   ;(set-face-attribute 'show-paren-mismatch-face nil
   ;                    :weight 'bold :underline t :overline nil :slant 'normal)
   (defun paren-match ()
     "Tries to jump to the matching parenthesis to the one currently
      under the point. Useful if the matching paren is out of sight. "
     (interactive)
     (cond ((looking-at "[{\[\(]") (forward-sexp 1) (backward-char))
           ((looking-at "[]})]") (forward-char) (backward-sexp 1))
           (t (message "Point not at a parenthesis."))))
   (global-set-key "\C-xp" 'paren-match)

.. _clang_format_emacs_integration:

Clang-format integration
------------------------

There is an integration for Emacs. It can be found at ``clang/tools/clang-format/clang-format.el`` and used by adding this to your ``.emacs``:

.. code-block:: text

  (load "<path-to-clang>/tools/clang-format/clang-format.el")
  (global-set-key [C-M-tab] 'clang-format-region)

This binds the function ``clang-format-region`` to ``C-M-tab``, which then formats the current line or selected region.

