STATIC_DIR = ./stickyuploads/static/stickyuploads
JQUERY_VERSION = 1.11.3
JQUERY = ${STATIC_DIR}/js/jquery-${JQUERY_VERSION}.js
JQUERY_INIT = ${STATIC_DIR}/js/jquery.init.js
JQUERY_BUNDLE = ${STATIC_DIR}/js/jquery.bundle.js
UPLOADER_BUNDLE = ${STATIC_DIR}/js/django-uploader.bundle.js
UPLOADER = ${STATIC_DIR}/js/django-uploader.js

$(JQUERY):
	wget http://code.jquery.com/jquery-${JQUERY_VERSION}.js -O ${JQUERY}

$(JQUERY_INIT):
	@echo ";var djUp = jQuery.noConflict(true);" > ${JQUERY_INIT}

$(JQUERY_BUNDLE): $(JQUERY) $(JQUERY_INIT)
	@cat $^ > $@
	# @cat ${JQUERY} ${JQUERY_INIT} > ${JQUERY_BUNDLE}

$(UPLOADER_BUNDLE): $(JQUERY_BUNDLE) $(UPLOADER)
	@cat $^ > $@
	# @cat ${JQUERY_BUNDLE} ${UPLOADER} > ${UPLOADER_BUNDLE}

build-js: $(UPLOADER_BUNDLE) $(UPLOADER)
	# Build bundled and minified JS
	# Requires uglifyjs
	uglifyjs ${UPLOADER_BUNDLE} > ${STATIC_DIR}/js/django-uploader.bundle.min.js
	uglifyjs ${UPLOADER} > ${STATIC_DIR}/js/django-uploader.min.js

lint-js:
	# Check JS for any problems
	# Requires jshint
	jshint ${STATIC_DIR}/js/django-uploader.js

clean: $(JQUERY_INIT) $(JQUERY_BUNDLE) $(UPLOADER_BUNDLE)
	rm $^

.PHONY: lint-js clean
