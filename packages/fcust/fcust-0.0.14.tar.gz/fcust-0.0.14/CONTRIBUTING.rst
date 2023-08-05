.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/Iolaum/fcust/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Folder Custodian could always use more documentation, whether as part of the
official Folder Custodian docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/Iolaum/fcust/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Get Started!
------------

Ready to contribute? Here's how to set up `fcust` for local development.

1. Fork the `fcust` repo on GitHub.
2. Clone your fork locally. ::

    $ git clone git@github.com:your_name_here/fcust.git
    $ cd fcust

3. From the root of the repository create a python virtual environment to use for our project.
   Install the project in editable mode along with developer dependencies. ::

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -e .[dev]

4. Create a branch for local development. ::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass code quality checks
   and tests. ::

    $ make code
    $ make test

6. Commit your changes and push your branch to GitHub. ::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.9, for PyPy and Fedora. Check
   https://travis-ci.com/Iolaum/fcust/pull_requests
   and make sure that the tests pass for all supported Python versions.


Developing on Fedora Silverblue
-------------------------------

If developing on Fedora Silverblue the following set up is suggested:

# Crete new toolbox
$ toolbox create dev
# Add toolbox entry to /etc/hosts to avoid
# warning: Could not canonicalize hostname: toolbox
$ sudo nano /etc/hosts
# 127.0.0.1 ... toolbox
$ toolbox enter dev
# Following commands are inside the toolbox
$ sudo su $USER # This is to bypass https://github.com/containers/toolbox/issues/608
$ cd $source_code_root_repository
$ sudo dnf install make fedpkg python3-wheel python3-devel python3-sphinx python3-click
$ make code
$ make test
$ make fedpkg


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
