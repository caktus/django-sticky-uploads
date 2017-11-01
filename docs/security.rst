Security Considerations
================================================

Any time you allow users to upload files to your web server, you have a potential security hole. This
is the case whether you use django-sticky-uploads or not. Below are some things to keep
in mind when setting up your project to use django-sticky-uploads. Additionally you
should read the notes on `Unrestricted File Uploads <https://www.owasp.org/index.php/Unrestricted_File_Upload>`_
from the `OWASP project <https://www.owasp.org/>`_ for more information on the potential
risks and mitigations.


Project Internals
----------------------------------------------------------------------

By default django-sticky-uploads takes the follow steps to avoid some of the largest
problems with unrestricted file uploads. First, it only allows authenticated users to
upload files through the background API. Second, it leverages the existing CSRF protections
in Django to help ensure that a user's credentials cannot be used to upload files without
their knowledge. Additionally, the temporary uploaded files are stored in the system
temp directory and should not be exposed by the webserver until the original form
has had a chance to validate the file.

The serialization used for the stored file references uses the
`cryptographic signing <https://docs.djangoproject.com/en/stable/topics/signing/>`_ utilities
included in Django. This prevents the client from manipulating the value when it is available
on the client. This relies on keeping your ``SECRET_KEY`` a secret. In the case that your
``SECRET_KEY`` is changed it will invalidate any serialized references used by django-sticky-uploads.


External Measures
----------------------------------------------------------------------

In addition to the builtin protections provided by Django and django-sticky-uploads,
you can also take steps in configuring your webserver to mitigate possible attacks. These
include:

* Limiting the file size of the allowed uploads
* Rate-limiting how often a user is allowed to upload files
* Do not allow "execute" permissions in the uploaded directory
* Installing a virus scanner on the server

More details can be found on the OWASP site.
