Example project
---------------

The source tree contains an example Django project using django-sticky-uploads
in the examples directory. It's a quick way to try out django-sticky-uploads.

* Clone the repository locally and change directories into the source tree::

    $ git clone https://github.com/caktus/django-sticky-uploads
    $ cd django-sticky-uploads

* Create a virtualenv::

    $ mkvirtualenv sticky-example

* Install django-sticky-uploads and django::

    $ add2virtualenv .
    $ pip install Django

* Change into the 'example' directory::

    $ cd example

* Run migrations::

    $ python manage.py migrate

* Create a user::

    $ python manage.py createsuperuser

* Run the server::

    $ python manage.py runserver

* Visit `http://127.0.0.1:8000/ <http://127.0.0.1:8000/>`_ in a browser.

* Login

* Experiment with the file upload form

* Use the admin at `http://127.0.0.1:8000/admin/main/savedupload/ <http://127.0.0.1:8000/admin/main/savedupload/>`_
  to see the files uploaded in the background, and look for them in the ``media/uploads`` directory.
