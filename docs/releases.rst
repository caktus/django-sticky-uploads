Release History
========================


v0.5.0 (Released 2017-11-01)
----------------------------

* Add support for Python 3.5, 3.6
* Drop support for Python 3.2, 3.3
* Add support for Django 1.10, 1.11
* Drop support for Django 1.9 and Django older than 1.8

v0.4.0 (Released 2015-06-15)
-------------------

* Do not display link for temporary uploads (supported on Django 1.6+)
* Dropped testing support for Python 2.6
* Added testing for Django 1.8
* Updated bundled jQuery version to 1.11.3


v0.3.0 (Released 2014-05-23)
-----------------------------------

* Added upload progress indicator
* Fixed support for Django 1.7
* Upgraded bundled jQuery version to 1.11.1


v0.2.0 (Released 2013-07-23)
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
