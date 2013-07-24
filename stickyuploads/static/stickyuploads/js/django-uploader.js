/*
 * django-sticky-uploads widget
 * Source: https://github.com/caktus/django-sticky-uploads
 * Docs: http://django-sticky-uploads.readthedocs.org/
 *
 * Depends:
 *   - jQuery 1.7+
 *
 * Copyright 2013, Caktus Consulting Group, LLC
 * BSD License
 *
*/
var djUp = djUp || jQuery;
(function ($, window, document, undefined) {
    var pluginName = "djangoUploader",
        defaults = {
            url: "",
            before: null,
            success: null,
            failure: null,
            submit: null,
            csrfCookieName: "csrftoken"
        };

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function getCookie(name) {
        var cookieValue = null,
            i = 0, cookies, cookie;
        if (document.cookie && document.cookie !== "") {
            cookies = document.cookie.split(";");
            for (i = 0; i < cookies.length; i++) {
                cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function DjangoUploader(element, options) {
        this.element = element;
        this.$element = $(element);
        this.options = $.extend({}, defaults, options);
        this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }

    DjangoUploader.prototype = {

        init: function () {
            this.processing = false;
            this.options.url = this.$element.data("uploadUrl");
            this.$hidden = $(":input[type=hidden][name=_" + this.$element.attr("name")  + "]");
            this.$form = this.$element.parents("form").eq(0);
            if (this.enabled()) {
                this.$element.on("change", $.proxy(this.change, this));
                this.$form.on("submit", $.proxy(this.submit, this));
            }
        },

        change: function (event) {
            var formData = new FormData(),
                file;
            if (this.element.files.length === 0) {
                return;
            }
            file = this.element.files[0];
            if (this.before(file) !== false) {
                formData.append("upload", file);
                this.abort();
                this.processing = $.ajax({
                    url: this.options.url,
                    type: "POST",
                    data: formData,
                    crossDomain: false,
                    beforeSend: $.proxy(this._add_csrf_header, this),
                    processData: false,
                    contentType: false
                }).done(
                    $.proxy(this.done, this)
                ).fail(
                    $.proxy(this.fail, this)
                ).always(
                    $.proxy(this.always, this)
                );
            }
        },

        before: function (file) {
            // Runs before the AJAX call.
            // Returning false will abort the call.
            var result = true;
            if (this.options.before) {
                result = this.options.before.apply(this, [file]);
            }
            return result;
        },

        always: function (response) {
            // Runs after the AJAX call regardless of success or failure.
            this.processing = false;
        },

        done: function (response) {
            // Runs on a successful (200) response
            if (response.is_valid && response.stored) {
                this.$hidden.val(response.stored);
            } else {
                this.$hidden.val("");
            }
            if (this.options.success) {
                this.options.success.apply(this, [response]);
            }
        },

        fail: function (response) {
            // Runs on a error (40X-50X) response
            this.$hidden.val("");
            if (this.options.failure) {
                this.options.failure.apply(this, [response]);
            }
        },

        submit: function (event) {
            // Hijacked form submission
            if (this.options.submit) {
                this.options.submit.apply(this, [event]);
            } else {
                // Cancel current request and file will be submitted normally
                this.abort();
            }

            if (this.$hidden.val()) {
                // Don't submit the file since its already on the server
                this.$element.prop("disabled", true);
            }
        },

        abort: function () {
            // Abort the current upload if any
            if (this.processing) {
                this.processing.abort();
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

        _add_csrf_header: function (xhr, settings) {
            var csrftoken = "";
            if (!csrfSafeMethod(settings.type)) {
                csrftoken = getCookie(this.options.csrfCookieName);
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    };

    $.fn[pluginName] = function (options) {
        return this.each(function () {
            if (!$.data(this, pluginName)) {
                $.data(this, pluginName, new DjangoUploader(this, options));
            }
        });
    };

    $(document).ready(function () {
        // Auto-bind file inputs with data-upload-url attributes
        $(":input[type=file][data-upload-url]").djangoUploader();
    });

})(djUp, window, document);