[![Web site](https://img.shields.io/badge/developer-lsst.io-brightgreen.svg)](https://developer.lsst.io)
[![GitHub Actions](https://github.com/lsst-dm/dm_dev_guide/workflows/CI/badge.svg)](https://github.com/lsst-dm/dm_dev_guide/actions?query=workflow%3A%22CI%22)

# LSST DM Developer Guide

This repository contains the content for the [LSST DM Developer Guide, https://developer.lsst.io](http://developer.lsst.io).

Everyone in LSST DM is encouraged to not only *use* this guide, but also *contribute* to it.
The contribution process is outlined below.

Documentation is written in reStructuredText, built using [Sphinx](http://sphinx-doc.org), and hosted with our in-house platform, [LSST the Docs](https://sqr-006.lsst.io).

**Changes to the `main` branch are automatically deployed to https://developer.lsst.io.**
Other branches are also deployed: find them at https://developer.lsst.io/v.

## Contributing

1. Clone this repository: `git clone https://github.com/lsst-dm/dm_dev_guide && cd dm_dev_guide`.

2. Create a branch. This can either be an informal user branch or a full-fledged ticket branch tracked in JIRA. See the [DM Workflow guide](https://developer.lsst.io/work/flow.html#git-branching) for details.

3. Make and commit your edits. Content is written in reStructuredText. Our [reStructuredText Style Guide](https://developer.lsst.io/restructuredtext/style.html) covers the syntax you'll need.

4. Push your development branch to GitHub and make a pull request. The pull request page will help you track the publishing and testing status of your branch. 

5. If your build on [GitHub Actions](https://github.com/lsst-dm/dm_dev_guide/actions?query=workflow%3A%22CI%22) is successful, your branch will be published with LSST the Docs. **Find your branch listed at https://developer.lsst.io/v.**

6. Once you're done, press the green button on your pull request to merge to `main`. Your changes are automatically published to the main URL: https://developer.lsst.io. Don't worry about messing things up, GitHub branch protections will ensure that your edits build successfully, and that your branch is up-to-date with `main`.

### Installing and building these docs locally

Although LSST the Docs will publish your development branch, you might want to build this documentation locally.

Assuming you've cloned the docs (following the guide above):

1. Create a [Python virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for this project using your tool of choice: [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) or [pyvenv](https://docs.python.org/3/library/venv.html) (for Python 3).

2. Install dependencies

   ```
   pip install -r requirements.txt
   ```

3. Compile the HTML by running

   ```
   make html
   ```

The built site is in the `_build/html` directory.

### Editing entirely on GitHub

If you're in a hurry, you don't need to worry about cloning the Developer Guide; you can do everything on GitHub.com. See [GitHub's documentation](https://help.github.com/articles/github-flow-in-the-browser/) on editing files and creating branches entirely from GitHub.com.

Remember to preview your published branch by finding it at https://developer.lsst.io/v (see Step #5 of § *Contributing*, above).

## License

Copyright 2015-2019 Association of Universities for Research in Astronomy, Inc. (AURA).

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">LSST DM Developer Guide</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://www.lsst.org" property="cc:attributionName" rel="cc:attributionURL">Association of Universities for Research in Astronomy, Inc.</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/lsst_dm/dm_dev_guide" rel="dct:source">https://github.com/lsst_dm/dm_dev_guide</a>.
