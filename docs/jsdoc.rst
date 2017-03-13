########################################
Documenting JavaScript APIs with JSDoc
########################################



.. _jsdoc-useful-tags: 

Frequently used tags 
^^^^^^^^^^^^^^^^^^^^

@desc <some description>
    This tag provides a general description of the symbol or method.

@func [<functionName>]
    This tag marks an object as being a function with a given name.

@ignore
    The ignore tag indicates that a symbol in your code should never
    appear in the documentation. This tag takes precedence over all
    other tags.

    For most JSDoc templates, including the default template, the @ignore tag has the following effects:

    - If you use the @ignore tag with the @class or @module tag, the entire class or module will be omitted from the documentation.
    - If you use the @ignore tag with the @namespace tag, you must also add the @ignore tag to any child classes and namespaces. Otherwise, your documentation will show the child classes and namespaces, but with incomplete names.

@memberof module:<parentNamePath\|moduleName>

@memberof <namespace>
    This tag tells a member symbol that belongs to a parent symbol.

@module [<type>] <moduleName>
    This tag marks the current file as being its own module. All symbols in the file are assumed to be members of the module unless documented otherwise.

@namespace
    This tag indicates that an object creates a namespace for its
    members. You can also write a virtual JSDoc comment that defines a namespace used by your code.

    Note: You can not define more than one namespace in one jsdoc block like this:

    /\*\* 

    \*\@namespace firefly

    \*\@namespace firefly.util

    \*\@namespace firefly.action

    \*/

    The jsdoc will only document firefly.action, the last one in the
    block. To define more than one namespaces in one file you need to:

    /\*\*\@namespace firefly\*/

    /\*\*\@namespace firefly.action\*/

    /\*\*\@namespace firefly.ui\*/

@param

    This tag requires you to specify the name of the parameter you are
    documenting. You can also include the parameter's type, enclosed in
    curly brackets, and a description of the parameter. You can use \|
    to specify more than one type such as {type1\|type2\|type3}.

@static

    This tag indicates that a symbol is contained within a parent and
    can be accessed without instantiating the parent.

@summary

    This tag is a shorter version of the full description. It can be
    added to any doclet.

@typedef [<type>] <namepath>

    This tag is useful for documenting custom types, particularly if you
    wish to refer to them repeatedly. These types can then be used
    within other tags expecting a type, such
    as \@type or \@param.

    NOTE: I used @global in each @typedef object. Thus, the typedef
    object can be referred throughout the documentation.

When to use @func
^^^^^^^^^^^^^^^^^^^^

By default, the jsdoc documents all the exported members by
``export.functionName``. To document them as static members of a namespace,
you use @func <functionName>. For methods and constants are defined
without export, you don’t need to use @func <functionName>. **Note: The
behavior in namespace is opposite to module.**

When to use @memberof
^^^^^^^^^^^^^^^^^^^^^^

For methods or constants, you have to use @memberof <namespace> to
group them under the <namespace>. Without @memberof tag, all the methods
and constants will appear under the global category.

Known issues:
^^^^^^^^^^^^^^^^^^^^^^

1. There is more than one way to produce the same output using the tags.

2. Depending on the templates, the tags may not work exactly as they are
   described. The default template came with JSDoc is located in the
   jsdoc directory

3. Note: the following two tags worked for minami template. But the
   docstrap template seems not recognizing them correctly.

    @private

    The @private tag marks a symbol as private, or not meant for general
    use. Private members are not shown in the generated output unless
    JSDoc is run with the -a/--private command-line option or specifying
    the option in the configuration. The @private tag is equivalent
    to @access private.

    @public

    The @public tag indicates that a symbol should be documented as if
    it were public. By default, JSDoc treats all symbols as public, so
    using this tag does not normally affect the generated documentation.
    However, you may prefer to use the @public tag explicitly so it is
    clear to others that you intended to make the symbol public.
    However, @public does not change the symbol’s scope. The @public tag
    is the same as @access public.


Start from scratch:
^^^^^^^^^^^^^^^^^^^^^^

1. Add the dependent libraries to package.json

    .. code-block:: json

       "eslint-plugin-jsx-a11y": "^0.6.2",

       "jsdoc-jsx": "^0.1.0",

       "ink-docstrap": "^1.2.1"

2. Build your libraries, for example,

    .. code-block:: bash

       gradle :firefly:war

       gradle :firefly:deploy

3. Use jsdoc\_config.json located in firefly/src/firefly directory or create your own configuration file.

4. Add proper tags in each source file.

5. JSDoc comments should generally be placed immediately before the code being documented. It must start with a /\*\* sequence in order to be recognized by the JSDoc parser.

6. Generate the javascript documentation at /hydra/cm/firefly directory
   by running:

   .. code-block:: bash

      ./node\_modules/.bin/jsdoc –c path/to/your-configuration-file


    (Note. Use any command line options to override the options defined in the configuration file.)

7. To check the available command line options:

   .. code-block:: bash

      ./node\_modules/.bin/jsdoc -h

References:
^^^^^^^^^^^^^^^^^^^^^^

    http://usejsdoc.org/

    https://github.com/jsdoc3/jsdoc/blob/master/README.md
