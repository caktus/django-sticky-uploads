Customizing the Client Side
================================================

The uploader has a number of hooks to add additional validation or
interactions in the browser.


Accessing the uploader
----------------------------------------------------------------------

When the uploader is bound to a file input, it is stored on the element as
a property named ``djangoUploader`` during django-stick-uploads' initialization.

.. code-block:: javascript

    var myfield = document.querySelector('input[type=file]#some_id');
    var uploader = myfield.djangoUploader;

The django-sticky-uploads initialization happens
after the DOM has been loaded. A good way to run your own code after that is to load your own
code after django-sticky-uploads, and arrange for it also to run after the DOM
has been loaded; it should then run after django-sticky-uploads.

You can check whether the uploader is enabled for the current browser with
the ``enabled`` function.

.. code-block:: javascript

    console.log(uploader.enabled());

(Being "enabled" means the current browser supports the standard features
for uploading files that django-sticky-uploads needs.)

AJAX Hooks
----------------------------------------------------------------------

There are 3 hooks for interacting with the uploader in the life cycle of a new
upload request: ``before``, ``success``, and ``failure``. All of these callbacks
are given the scope of the uploader. That is, ``this`` will access the uploader inside
of the callback. Each of these callbacks is set by assigning to
``uploader.options``.


``before``
______________________________________________________________________

The ``before`` function, if set, is called when the file input has been changed,
and is passed a single argument which is the file data. You may use this hook 
to do any validations on the file to be uploaded. If the ``before`` callback 
returns ``false``, it will prevent the upload. An example is given below:

.. code-block:: javascript

    var uploader = myfield.djangoUploader;
    uploader.options.before = function (file) {
        if (file.size > 1024 * 1024 * 2) {
            // This file is too big
            return false;
        }
    };

.. note::

    While this hook can be used to do some basic validations, since it
    is controlled on the client it can be circumvented by a truly malicious
    user. Any validations should be replicated on the server as well. This
    should primarily be used for warnings to the user that data they are about
    to submit is not going to be valid.


``success``
______________________________________________________________________

The ``success`` callback is called when the server has completed a successful
upload. Successful in this case means that the server gave a 2XX response which
could include the case where the server did not validate the file which was
uploaded. A successful server response will contain the following info:

.. code-block:: javascript

    {
        'is_valid': true, // Response was valid
        'filename': 'filename.txt', // File name which was uploaded
        'url': '', // URL (if any) where this file can be accessed
        'stored': 'XXXXXX' // Serialized stored value
    }

All callbacks should first check for ``is_valid`` before continuing any
other processing. The other keys are not included when the upload is not valid.

.. code-block:: javascript

    var uploader = myfield.djangoUploader;
    uploader.options.success = function (response) {
        if (response.is_valid) {
            // Do something
        } else {
            // Do something else
        }
    };


``failure``
______________________________________________________________________

The ``failure`` callback is called when the server has returned a 4XX or 5XX
response. This might be caused by the user not having permission to do the upload
or a server timeout. The callback is given the server response.

.. code-block:: javascript

    var uploader = myfield.djangoUploader;
    uploader.options.failure = function (response) {
        // Do something
    };


Handling the Form Submit
----------------------------------------------------------------------

Because the file is being uploaded in the background while the user processes
the rest of the form, there is a case where the file upload has not completed
but the user has submitted the form. In this case the default behavior of the
plugin is to abort upload request and submit the form as normal. This means
at least part of the file will have been uploaded twice and the effort
in the background upload is wasted.

If you choose, you can handle this case differently using the ``submit`` callback.
This callback is passed a single argument which is the form submit event. One
example of using this option is given below:

.. code-block:: javascript

    var uploader = myfield.djangoUploader;
    uploader.options.submit = function (event) {
        var self = this, callback;
        if (this.processing) {
            // Prevent submission
            event.preventDefault();
            var form = event.target;
            callback = function () {
                if (self.processing) {
                    // Wait 500 milliseconds and try again
                    setTimeout(callback, 500);
                } else {
                    // Done processing so submit the form
                    form.submit();
                }
            };
            // Wait 500 milliseconds and try again
            setTimeout(callback, 500);
        }
    };
