Django Sticky Uploads
========================

django-sticky-uploads is a progressively enhanced file input widget for Django 
which uploads the file in the background and also retains value on form errors.

.. image::
    https://secure.travis-ci.org/caktus/django-sticky-uploads.png?branch=master
    :alt: Build Status
        :target: https://secure.travis-ci.org/caktus/django-sticky-uploads


Requirements/Installing
-----------------------------------

django-sticky-uploads requires requires Django 1.11 or 2.0, and a Python
that is supported by the chosen version of Django.

The easiest way to install django-sticky-uploads is using `pip <http://www.pip-installer.org/>`_::

    pip install django-sticky-uploads


Browser Support
-----------------------------------

This project makes use of `progressive enhancement <http://en.wikipedia.org/wiki/Progressive_enhancement>`_
meaning that while all browsers are supported, they will not all have the same user-experience. If
the browser does not support the necessary client-side features then it will fall back to the
default file upload behavior.

The primary HTML5 dependencies are `File API <http://caniuse.com/fileapi>`_ and
`XHR2 <http://caniuse.com/xhr2>`_ meaning that the following desktop/mobile browsers should get the enhanced
experience:

* Chrome 13+
* Firefox 4+
* Internet Explorer 10+
* Safari 6+
* Opera 12+
* iOS Safari 6+
* Android Brower 3+
* Blackberry Broswer 10+
* Opera Mobile 12+
* Chrome for Android 27+
* Firefox for Android 22+


Documentation
-----------------------------------

Additional documentation on using django-sticky-uploads is available on 
`Read The Docs <http://django-sticky-uploads.readthedocs.io/en/latest/>`_.


Running the Tests
------------------------------------

You can run the tests with via::

    tox

(Possibly after installing ``tox`` with ``pip install tox`` or alternative.)

License
--------------------------------------

django-sticky-uploads is released under the BSD License. See the 
`LICENSE <https://github.com/caktus/django-sticky-uploads/blob/master/LICENSE>`_ file for more details.

Contributing
--------------------------------------

If you think you've found a bug or are interested in contributing to this project
check out `django-sticky-uploads on Github <https://github.com/caktus/django-sticky-uploads>`_.

Development sponsored by `Caktus Consulting Group, LLC
<http://www.caktusgroup.com/services>`_.
