Getting Started with django-sticky-uploads
================================================

This will walk you through the basics of getting started with django-sticky-uploads.
It assumes that you have already installed django-sticky-uploads via::

    pip install django-sticky-uploads

and have an existing project using a compatible version of Django and Python.


Necessary Settings
----------------------------------------------------------------------

After installing you should include ``stickyuploads`` in your ``INSTALLED_APPS``
setting. To use the default upload view you must also be using ``contrib.auth``
to manage users.

.. code-block:: python

    INSTALLED_APPS = (
        # Required by stickyuploads
        'django.contrib.auth',
        # Required by contrib.auth
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        # Other apps go here
        'stickyuploads',
    )

This is required so that the built-in ``contrib.staticfiles`` can find the JS
included in the django-sticky-uploads distribution. If you are not using
``contrib.staticfiles`` then this step is not required but you are on your
own to ensure the static files are included correctly.


Including the URLs
----------------------------------------------------------------------

django-sticky-uploads includes views for accepting the AJAX file uploads.
You'll need to include these in your url patterns:

.. code-block:: python

    from django.conf.urls import patterns, include, url


    urlpatterns = patterns('',
        # Other url patterns go here
        url(r'^sticky-uploads/', include('stickyuploads.urls')),
    )

The ``sticky-uploads/`` is there for example purposes and you are free to
change it to suit your own needs.


Including the JS
----------------------------------------------------------------------

The enhanced upload widget requires a small piece of JavaScript to handle the background
upload. Each of the cases assume that you are using ``contrib.staticfiles``
to manage static dependencies.

First, you can add the following script tag to any page which will use the widget.

.. code-block:: html
    
    {% load static from staticfiles %}
    <script type="text/javascript" src="{% static 'stickyuploads/js/django-uploader.js' %}"></script>

Alternatively, you can minimize the JavaScript and load that, or bundle it with other JavaScript
for the page.

Yet another option is to include ``{{ form.media }}``, where ``form`` is whatever form
is using the upload widget. The widget includes an
`inner Media class <https://docs.djangoproject.com/en/stable/topics/forms/media/>`_
that lists ``'stickyuploads/js/django-uploader.js'`` as a dependency, and including
``{{ form.media }}`` in the template will produce the necessary markup to load it.


Adding the Widget
----------------------------------------------------------------------

The final step to use django-sticky-uploads is to use the widget on an existing
form with a ``FileField``. The ``StickyUploadWidget`` is a drop-in replacement for
the default ``ClearableFileInput`` and can be used on any Django ``Form`` including
``ModelForm``s.

.. code-block:: python

    from django import forms

    from stickyuploads.widgets import StickyUploadWidget


    class ExampleForm(forms.Form):
        upload = forms.FileField(widget=StickyUploadWidget)

Note that to make use of the background upload, the user must be authenticated, so
the ``StickyUploadWidget`` should only be used on forms/views where the user is
authenticated.


Next Steps
----------------------------------------------------------------------

There are hooks on both the client side and server side for customizing the
behavior of the uploads. Continue reading to see how you can adjust the default
settings to fit your needs.
