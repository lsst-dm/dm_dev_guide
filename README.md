# LSST DM Developer Guide

This repository contains the base source material for the [LSST DM Developer Guide, http://developer.lsst.io](http://developer.lsst.io).

Documentation is written in reStructuredText, built using [Sphinx](http://sphinx-doc.org), and hosted by [readthedocs.org](http://readthedocs.org).
Changes to the `master` branch are automatically deployed to http://developer.lsst.io.

## Contributing

### Resources for writing reStructuredText

See the [Writing Documentation](#) section of the Developer Guide for an overview of writing reStructuredText.

Since this is a Git repository, we recommend following the standard [DM development workflow](#) with JIRA tickets, ticket branches, and code review.
For very small changes the review process can be by-passed, through review is tremendously beneficial for larger changes.
Formally there is not requirement to review documentation changes.

### Installing and building these docs Locally

You can get the source for the LSST DM Developer Guide by cloning the [GitHub repo](https://github.com/lsst-sqre/dm_dev_guide).

```
git clone https://github.com/lsst-sqre/dm_dev_guide.git
cd dm_dev_guide
```

Create a [Python virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for this project using your tool of choice: [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) or [pyvenv](https://docs.python.org/3.5/library/venv.html) (for Python 3).

Install Python dependencies by running

```
pip install -r requirements.txt
```

Compile the HTML by running

```
make html
```

The site will be built in the `_build/html` directory.

## Licensing

Copyright 2015-2016 AURA/LSST

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
![Creative Commons License](https://cdn.rawgit.com/lsst-sqre/lsst_stack_docs/master/_static/cc-by_large.svg?raw=true)
</a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">LSST Stack Handbook</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://docs.lsst.codes" property="cc:attributionName" rel="cc:attributionURL">LSST Project</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>
