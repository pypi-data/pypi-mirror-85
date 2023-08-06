Zero-Configuration Django Projects
==================================

*This is a work in progress. It's used in production, but it may, or may not fit your needs. Also, things can change without warnings.*

Create modern web applications using python, django, jinja2, whitenoise, webpack, bootstrap, ... without having to
configure anything. No magic included, you can unplug/customize anything afterward.

Django Zero is a wrapper around the Django Framework (2+) that allows to create full-featured projects with (nearly)
zero configuration.

Out of the box, you get:

* **Jinja2** templating.
* **Webpack**, **Bootstrap**, **Sass** for assets.
* **Honcho** for process management.
* **Docker** images.
* **Allauth** for user authentication (with jinja2 templates).
* **Debug toolbar** and **django extensions** in development mode.
* **Cookiecutter** for scaffolding.
* **Mondrian** for logging.
* **Gunicorn** for production server.
* **Pytest** for... tests!

And more to come.

Everything is used explicitely and you can unplug any feature you don't like.

Quick start
===========

You need Python3.5+, Node.js LTS and Yarn. We advise to stick to latest stable python 3.

Install the project, and build node modules required for development.

.. code-block:: shell-session

    $ pip install django-zero[dev]
    $ django-zero install

Create an empty project:

.. code-block:: shell-session

    $ django-zero init project my-web-app

Run the dev server (with webpack watching assets):

.. code-block:: shell-session

    $ cd my-web-app
    $ django-zero start


