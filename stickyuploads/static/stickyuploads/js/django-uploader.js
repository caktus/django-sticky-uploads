/*
 * django-sticky-uploads widget
 * Source: https://github.com/caktus/django-sticky-uploads
 * Docs: http://django-sticky-uploads.readthedocs.org/
 *
 *
 * Copyright 2013-2017, Caktus Consulting Group, LLC
 * BSD License
 *
*/

/* Polyfill for Element.matches (https://developer.mozilla.org/en-US/docs/Web/API/Element/matches) */
if (!Element.prototype.matches) {
    Element.prototype.matches =
        Element.prototype.msMatchesSelector ||
        Element.prototype.webkitMatchesSelector;
}

(function (window, document, undefined) {
    "use strict";
    var pluginName = "djangoUploader",
        defaults = {
            url: "",
            before: null,
            success: null,
            failure: null,
            submit: null,
            csrfCookieName: "csrftoken"
        };

    const DONE = 4;

    function getCookie(name) {
        var cookieValue = null,
            i = 0, cookies, cookie;
        if (document.cookie && document.cookie !== "") {
            cookies = document.cookie.split(";");
            for (i = 0; i < cookies.length; i++) {
                cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Some helpers, similar to features of jQuery
    function closest(elt, selector) {
        if (elt.matches(selector)) {
            return elt;
        }
        var parent = elt.parentElement;
        if (parent !== null) {
            return closest(parent, selector);
        }
        return undefined;
    }

    function insertAfter(elt_to_insert, elt_to_insert_it_after) {
        var parent = elt_to_insert_it_after.parentElement;
        // insert before the node we really want to insert after
        parent.insertBefore(elt_to_insert, elt_to_insert_it_after);
        // then swap them
        parent.insertBefore(elt_to_insert_it_after, elt_to_insert);
    }

    function DjangoUploader(element, options) {
        this.element = element;
        this.options = Object.assign({}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    DjangoUploader.prototype = {

        init: function () {
            this.processing = false;
            this.options.url = this.element.getAttribute("data-upload-url");
            this.form = closest(this.element, "form");
            var hidden_selector = "input[type=hidden][name=_" + this.element.getAttribute("name")  + "]";
            this.hidden = this.form.querySelectorAll(hidden_selector)[0];
            if (this.enabled()) {
                this.element.addEventListener("change", this.change.bind(this));
                this.form.addEventListener("submit", this.submit.bind(this));
                this.progress = document.createElement('span');
                this.progress.setAttribute('class', 'progress-label');
                insertAfter(this.progress, this.element);
            }
        },

        change: function (event) {
            var formData = new FormData(),
                file;
            if (this.element.files.length === 0) {
                return;
            }
            file = this.element.files[0];
            if (this.options.before) {
                if (!this.options.before.apply(this, [file])) {
                    return;
                }
            }
            formData.append("upload", file);
            this.abort();
            this.start_upload(formData);
        },

        onProgress: function(evt) {
            if (evt.lengthComputable) {
                var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
                // Increase the progress progress label until 100%
                this.progress.textContent = percentLoaded + '%';
            }
        },

        onReadyStateChange: function() {
            const xhr = this.xhr;

            if (xhr.readyState === DONE) {
                const response = JSON.parse(xhr.response);

                if (xhr.status >= 200 && xhr.status < 300) {
                    // Runs on a successful (2XX) response
                    if (response.is_valid && response.stored) {
                        // hidden is an input element https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement
                        this.hidden.value = response.stored;
                    } else {
                        this.hidden.value = "";
                    }
                    if (this.options.success) {
                        this.options.success.apply(this, [response]);
                    }
                }
                else if (xhr.status >= 400 && xhr.status < 600) {
                    // Runs on an error (4XX-5XX) response
                    this.hidden.value = "";
                    if (this.options.failure) {
                        this.options.failure.apply(this, [response]);
                    }
                }
                this.processing = false;
                this.xhr = undefined;
                this.progress.textContent = '';

            }
        },

        start_upload: function(formData) {
            const xhr = new XMLHttpRequest();
            this.xhr = xhr;
            xhr.onreadystatechange = this.onReadyStateChange.bind(this);
            xhr.upload.addEventListener("progress", this.onProgress.bind(this));
            this.progress.textContent = "Uploading...";

            xhr.open("POST", this.options.url, true);
            xhr.setRequestHeader("X-CSRFToken", getCookie(this.options.csrfCookieName));
            xhr.send(formData);
        },

        submit: function (event) {
            // Hijacked form submission
            if (this.options.submit) {
                this.options.submit.apply(this, [event]);
            } else {
                // Cancel current request and file will be submitted normally
                this.abort();
            }

            if (this.hidden.value) {
                // Don't submit the file since its already on the server
                this.element.disabled = true;
            }
        },

        abort: function () {
            // Abort the current upload if any
            if (this.processing) {
                this.xhr.abort();
                this.processing = false;
                this.xhr = undefined;
            }
        },

        enabled: function () {
            // Checks for necessary browser support
            var xhr2 = false,
                fileApi = false,
                xhr = new XMLHttpRequest();
            if (typeof xhr.upload !== "undefined") {
                xhr2 = true;
            }
            if (window.FormData) {
                fileApi = true;
            }
            return xhr2 && fileApi;
        },

    };

    function init_sticky_uploads() {
        // Auto-bind file inputs with data-upload-url attributes
        var i, inputs = document.querySelectorAll("input[type=file][data-upload-url]");
        for (i=0; i < inputs.length; i++) {
            // For each input field, create an uploader object, and stash it
            // as a property so it can be accessed later.
            inputs[i].djangoUploader = new DjangoUploader(inputs[i]);
        }
    }

    // Run setup when ready.
    if (document.readyState === 'loading') {
        // Run when loading is done
        document.addEventListener('DOMContentLoaded', init_sticky_uploads);
    } else {
        // It's already loaded, we can run now.
        init_sticky_uploads();
    }

})(window, document);
