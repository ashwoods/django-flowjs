django-flowjs
=============

This is an app for your Django project to enable large uploads using flow.js to chunk the files
client side and send chunks that are re-assembled server side.


.. image:: https://img.shields.io/pypi/v/django-flowjs.svg
   :alt: PyPi page
   :target: https://pypi.python.org/pypi/django-flowjs

.. image:: https://img.shields.io/travis/jazzband/django-flowjs.svg
    :alt: Travis CI Status
    :target: https://travis-ci.org/jazzband/django-flowjs

.. image:: https://img.shields.io/coveralls/jazzband/django-flowjs/master.svg
   :alt: Coverage status
   :target: https://coveralls.io/r/jazzband/django-flowjs

.. image:: https://readthedocs.org/projects/django-flowjs/badge/?version=latest&style=flat
   :alt: ReadTheDocs
   :target: http://django-flowjs.readthedocs.org/en/latest/

.. image:: https://img.shields.io/pypi/l/django-flowjs.svg
   :alt: License BSD

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband


Installation
------------

::

    pip install django-flowjs 


Configuration
-------------

-  Follow the configuration instructions for
   django-celery_
-  Add ``'django-flowjs'`` to your ``INSTALLED_APPS`` setting


.. _django-celery: https://github.com/ask/django-celery
.. _Celery:  http://celeryproject.org/
