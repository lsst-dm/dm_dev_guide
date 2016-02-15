######################################
Vim Configuration for LSST Development
######################################

This page will help you configure Vim to be consistent with LSST's coding standards and development practices.

C++ filetype configuration
==========================

The following configuration file should be placed in :file:`~/.vim/ftplugin/c.vim`:

.. code-block:: text

   setlocal shiftwidth=4
   setlocal softtabstop=4
   setlocal expandtab
   setlocal textwidth=110
   setlocal cino=:0,l1,g0,(0,u0,W2s
   setlocal comments^=s2:/**,mb:*,ex:*/
   syntax match cTodo /\todo/

You may also need to tell vim to indent according to your filetype plugins by adding the following to :file:`~/.vimrc`:

.. code-block:: text

   filetype plugin indent on

Explanation
-----------

``setlocal shiftwidth=4``
   Sets the autoindent spacing to 4 spaces.
   ``setlocal`` to limit this to the current (C++) buffer.

``setlocal softtabstop=4``
   Sets the spacing for tab characters to 4 spaces.

``setlocal expandtab``
   Always use spaces; never use tab characters.

``setlocal textwidth=110``
   Limit the length of a line to 110 characters (see :ref:`4-6 of the C++ Style Guide <style-guide-cpp-4-6>`)

``setlocal cino=:0,l1,g0,(0,u0,W2s``
   Set the C indent configuration.
   
   - ``:0``: align case labels with the enclosing switch.
   - ``l1``: indent statements relative to the case label, not anything following.
   - ``g0``: align C++ scope (private/public) labels with the enclosing class.
   - ``(0``: align lines after "(foo" next to the unclosed parenthesis.
   - ``u0``: same as above for the next level of parentheses deeper.
   - ``W2s``: indent lines following a line-terminating unclosed parenthesis by two shiftwidths (8 spaces).

``setlocal comments^=s2:/**,mb:*,ex:*/``
   Allow comments to start with two asterisks for Doxygen.

``syntax match cTodo /\todo/``
   Highlights lines using the Doxygen ``\todo``.
