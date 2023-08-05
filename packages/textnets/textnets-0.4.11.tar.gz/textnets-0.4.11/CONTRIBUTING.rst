.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

There are many ways you can contribute.

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/jboynyc/textnets/issues.

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

Textnets could always use more documentation, whether as part of the
official Textnets docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/jboynyc/textnets/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up **textnets** for local development.

1. Fork the ``textnets`` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/textnets.git

3. Install your local copy into a virtual environment. This is how you set up
   your fork for local development::

    $ cd textnets/
    $ python -m venv ENV # create the virtualenv
    $ source ENV/bin/activate # activate it
    $ python setup.py develop

   If you use `nix <https://nixos.org/nix>`__, you can also invoke
   ``nix-shell`` in the repository to quickly create a development environment
   with the included ``default.nix`` file.

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, format and lint your changes and run the
   unit tests::

    $ make lint
    $ make test
    $ make test-all # optional: to test other Python versions with tox

   To get flake8 and tox, just pip install them into your virtualenv.

6. Commit your changes::

    $ git add .
    $ git commit -m "Your detailed description of your changes."

7. Push you changes and submit a pull request through GitHub::

    $ git push origin name-of-your-bugfix-or-feature

   Alternately, if you'd rather avoid using GitHub, email a patch to the
   maintainer. See https://git-send-email.io/ for instructions.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add
   illustrative code examples to the tutorial.
3. The pull request should work for Python 3.7 and 3.8. Check
   https://travis-ci.org/github/jboynyc/textnets/pull_requests and make sure
   that the tests pass.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run::

$ bump2version patch # possible: major / minor / patch
$ git push
$ git push --tags

Travis will then deploy to PyPI if tests pass.
