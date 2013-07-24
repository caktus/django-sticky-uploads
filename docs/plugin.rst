Customizing the Client Side
================================================

The jQuery plugin has a number of hooks to add additional validation or
interactions in the browser.


Accessing the Plugin
----------------------------------------------------------------------

How you access the plugin depends on slightly on how you've included the
JS. If you are using the bundled version (such as in the admin) then you
must use the ``djUp`` namespaced jQuery. If you are using an existing version
of jQuery then you can use the common ``$`` or ``jQuery``. The examples below
will all use ``$``. You can handle these cases by wrapping your code in
a executing anonymous function such as:

.. code-block:: javascript

    var djUp = djUp || jQuery;
    (function ($) {
        // Code would go here
    })(djUp);

When the plugin is bound to a file input it is stored in the element's jQuery
data under the key ``djangoUploader``.

.. code-block:: javascript

    var plugin = $('#myfield').data('djangoUploader');

You can then check whether the plugin is enabled for the current browser with
the ``enabled`` function.

.. code-block:: javascript

    console.log(plugin.enabled());


AJAX Hooks
----------------------------------------------------------------------

There are 3 hooks for interacting with the plugin in the life cycle of a new
upload request: ``before``, ``success``, ``failure``. All of these callbacks
are given the scope of the plugin, that is ``this`` will access the plugin inside
of the callback. Each of these callbacks are set by assigning them to the
``plugin.options``.


``before``
______________________________________________________________________

The ``before`` function, if set, is called one the file input has been changed
and is passed a single argument which is the file data. You may use this hook 
to do any validations on the file to be uploaded. If the ``before`` callback 
returns ``false`` then it will prevent the upload. An example is given below:

.. code-block:: javascript

    var plugin = $('#myfield').data('djangoUploader');
    plugin.options.before = function (file) {
        if (file.size > 1024 * 1024 * 2) {
            // This file is too big
            return false;
        }
    };

.. note::

    That while this hook can be used to do some basic validations, since they
    are controlled on the client they can be circumvented by a truly malicious
    user. Any validations should be replicated on the server as well. This
    should primarily be used for warnings to the user that data they are about
    to submit is not going to be valid.


``success``
______________________________________________________________________

The ``success`` callback is called when the server has completed a successful
upload. Successful in the case means that the server gave a 20X response which
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

    var plugin = $('#myfield').data('djangoUploader');
    plugin.options.success = function (response) {
        if (response.is_valid) {
            // Do something
        } else {
            // Do something else
        }
    };


``failure``
______________________________________________________________________

The ``failure`` callback is called when the server has returned a 40X or 50X
response. This might be caused by the user not having permission to do the upload
or a server timeout. The callback is given the server response.

.. code-block:: javascript

    var plugin = $('#myfield').data('djangoUploader');
    plugin.options.failure = function (response) {
        // Do something
    };


Handling the Form Submit
----------------------------------------------------------------------

Because the file is being uploaded in the background while the user processes
the rest of the form, there is a case where the file upload has not completed
but the user has submitted the form. In this case the default behavior of the
plugin is to abort upload request and submit the form as normal. This means
the at least part of the file will have been uploaded twice and the effort
in the background upload is wasted.

If you chose you can handle this case differently using the ``submit`` callback.
This callback is passed a single argument which is the form submit event. One
example of using this option is given below:

.. code-block:: javascript

    var plugin = $('#myfield').data('djangoUploader');
    plugin.options.submit = function (event) {
        var self = this, callback;
        if (this.processing) {
            // Prevent submission
            event.preventDefault();
            callback = function () {
                if (self.processing) {
                    // Wait 500 milliseconds and try again
                    setTimeout(callback, 500);
                } else {
                    // Done processing so submit the form
                    self.$form.submit();
                }
            };
            // Wait 500 milliseconds and try again
            setTimeout(callback, 500);
        }
    };