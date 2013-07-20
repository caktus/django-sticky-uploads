Customizing the Server Side
================================================

django-sticky-uploads ships with a default view for handling the background file
uploads but you may need or want to customize the behavior such as where files
are stored or which users are allowed to upload files.


Changing the Storage
----------------------------------------------------------------------

For managing the file uploads, django-sticky-uploads uses the `File storage
API <https://docs.djangoproject.com/en/stable/ref/files/storage/>`_. This allows
you to use any valid storage backend for handing the files. By default the
view will use ``stickyuploads.storage.TempFileSystemStorage``. This is a subclass
of the built-in default ``FileSystemStorage`` with a few changes. First the files
are stored in ``/tmp`` (or OS equivalent temp directory) rather than ``MEDIA_ROOT``.
This storage does not expose a url to serve the temporarily uploaded files. 

.. note::

    If you are using a multi-server environment this default will not work for you
    unless you are able have the load balancer pin the consecutive requests to
    the same backend server or have the temp directory mounted on a network share
    available to all backend servers.

The storage used by the upload view is configured by the ``storage_class`` attribute. This
should be the full Python path to the storage class. This can be changed by
either sub-classing ``stickyuploads.views.UploadView`` or by passing it as a parameter
to ``as_view``.

.. code-block:: python
    
    # New view to use S3BotoStorage from django-storages

    from stickyuploads.views import UploadView

    urlpatterns = patterns('',
        url(r'^custom/$', 
            UploadView.as_view(storage_class='storages.backends.s3boto.S3BotoStorage'),
            name='sticky-upload-custom'),
    )

.. note::
    
    The storage backend you use should not take any arguments in the ``__init__`` or
    should be able to be used with the default arguments.


Changing Allowed Users
----------------------------------------------------------------------

By default the ``UploadView`` will only allow authenticated users to use the background
uploads. If you would like to change this restriction then you can subclass ``UploadView``
and override the ``upload_allowed`` method.

.. code-block:: python

    from stickyuploads.views import UploadView


    class StaffUploadView(UploadView):
        """Only allow staff to use this upload."""

        def upload_allowed(self):
            return self.request.user.is_authenticated() and self.request.user.is_staff


Pointing the Widget to the Customized View
----------------------------------------------------------------------

By default the ``StickyUploadWidget`` will use a view named ``sticky-upload-default``
for its uploads. If you want to change the url used you can pass the url to
the widget.

.. code-block:: python

    from django import forms
    from django.core.urlresolvers import reverse_lazy

    from stickyuploads.widgets import StickyUploadWidget


    class ExampleForm(forms.Form):
        upload = forms.FileField(widget=StickyUploadWidget(url=reverse_lazy('sticky-upload-custom')))

You may also choose to not use the default url patterns and name your own view
``sticky-upload-default`` in which case that url will be used by default.