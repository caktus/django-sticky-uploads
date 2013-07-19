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

django-sticky-uploads includes views for accepting the AJAX file uploads. To
get working you'll need to include these in your url patterns.

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

The enhanced upload widget requires a small piece of JS to handle the background
upload. This is a simple jQuery plugin which requires jQuery 1.7+ or higher. Depending
on your project you may wish to use a fully bundled version of the plugin or simply
include the plugin itself. Each of the cases assume that you are using ``contrib.staticfiles``
to manage static dependencies.


Already using jQuery 1.7+
______________________________________________________________________

If you have already included jQuery 1.7+ in your project then you can use the
minified plugin code without the included jQuery. To include this you should
add the following script tag to any page which will use the widget.

.. code-block:: html
    
    {% load static from staticfiles %}
    <script type="text/javascript" src="{% static 'stickyuploads/js/django-uploader.min.js' %}"></script>


No jQuery or jQuery < 1.7
______________________________________________________________________

If your project does not include jQuery or you are currently using a version of
jQuery older than 1.7 you can still use django-sticky-uploads by including a bundled
version of the plugin code.

.. code-block:: html
    
    {% load static from staticfiles %}
    <script type="text/javascript" src="{% static 'stickyuploads/js/django-uploader.bundle.min.js' %}"></script>

This version includes the plugin code as well as jQuery v1.10.2 together.


In the Django Admin
______________________________________________________________________

The Django admin currently ships with jQuery 1.4.2 which makes it too old to use
the widget. django-sticky-uploads will automatically include the bundled version of
the plugin when used in the admin so there is no additional files to include to
use the widget in the admin.


Adding the Widget
----------------------------------------------------------------------

The final step to use django-sticky-uploads is to use the widget on an existing
form with a ``FileField``. The ``StickyUploadWidget`` is drop-in replacement for
the default ``ClearableFileInput`` and can be used on any Django ``Form`` including
``ModelForm``s.

.. code-block:: python

    from django import forms

    from stickyuploads.widgets import StickyUploadWidget


    class ExampleForm(forms.Form):
        upload = forms.FileField(widget=StickyUploadWidget)

Note that to make use of the background upload, the user must be authenticated so
the ``StickyUploadWidget`` should only be used on forms/views where the user is
authenticated.


Next Steps
----------------------------------------------------------------------

There are hooks on both the client side and server side for customizing the
behavior of the uploads. Continue reading to see how you can adjust the default
settings to fit your needs.