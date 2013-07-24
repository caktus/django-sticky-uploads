Release History
========================

v0.2.0 (Released TBD)
-----------------------------------

* Security issue related to client changing the upload url specified by the widget for the upload
* Added documentation for plugin extensions and callbacks
* *Backwards Incompatible*: The signatures of the internal ``UploadForm.stash``, ``serialize_upload``, ``deserialize_upload`` and ``open_stored_file`` now require the upload url


v0.1.0 (Released 2013-07-19)
-----------------------------------

Initial public release includes:

* ``StickyUploadWidget`` as replacement widget for any ``FileField``
* jQuery plugin to process uploads in the background
* Server-side code to process/store temporary uploads
* Full test suite with `Travis CI <https://travis-ci.org/caktus/django-sticky-uploads>`_ integration
* Documentation covering installation, customization and security notes on `Read the Docs <http://readthedocs.org/docs/django-django-sticky-uploads/>`_
* Example project