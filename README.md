
# Potatoist

The project is a no-thrills easy to use issue tracking system that a developer like [Clark](docs/persona.md) can deploy on GAE.


## Getting started

- Run `./install_deps` (this will pip install requirements, and download the App Engine SDK)
- `python manage.py loaddata site`
- `python manage.py runserver`

The application is written using the [Djangae](http://djangae.readthedocs.org/en/latest/) project

To get the tests running:
- `python manage.py test`


## Development guidelines

Follow PEP8 best practises, this means (among other things):
- Four-space tabs are required
- Don’t use from package import *
- Do use descriptive lower_case_with_underscores variable names (understanding is much more important than brevity).
- Do put explanatory docstrings on all non-trivial classes and methods.
- If it isn’t covered by PEP 8, refer to [Idiomatic Python](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html)
or the [Python Guide](http://docs.python-guide.org/en/latest/), which is far more thorough.
- Don’t use print. Use Python’s built-in logging so that output can be structured for different use-cases. (Also it makes transition to Py3k much easier.)
- Always request a logger with log = logging.getLogger("project.app.module"). Take note of the logger naming structure so that output can be filtered.
- Organize imports in a logical manner: standard libraries first, then third-party libraries, then our own modules. Alphabetization within groups takes only a few seconds and makes removing cruft easier.
- When in doubt, remember import this. (PEP 20)


Django apps coding styles should follow the [Django Coding Style](https://docs.djangoproject.com/en/1.7/internals/contributing/writing-code/coding-style/)
 as a starting point. It's worth taking a look at the django source code, or other popular django 3rd party apps for reference.

We use pre-commit by Yelp hooks to ensure basic code conformity. In order to active in your git repository, make sure you
have installed the pip requirements and then do:

- `pre-commit install`

to install the projects git pre-commit hooks. Next time when you do git commit it will run flake, checks for pdb's and a few other `problems`.



## Issues & Branching policy

Issues and features are tracked on [github issues](https://github.com/ashwoods/potato/issues)
As the project is small we will use a relatively flat git feature branch policy with issues and features on
dev/(issue-number)-small-name-of-task branches. They should be merged with a staging branch will be deployed by the CI to
the staging server. The master branch is to be considered stable production code and we will not use tags for releases.

## DoD

This is an outline of our goal of DoD for Tasks:
- Code has been unit tested, pep8'd or flaked if it's python.
- Code has been peer reviewed to ensure code standards are being met
- Code has been checked in the task or user story branch for traceability
- Checked-in code doesn't break the build
- Task board has been updated.
- For fixing a bug, it has to have a test (regression test) clearly labeled for that bug.

## Trade-off options

We have negotiated with our client the following trade-off options:

- Scope: Fluid
- Resources: Fixed
- Schedule: Flexible






