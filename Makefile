STATIC_DIR = ./stickyuploads/static/stickyuploads
JQUERY_VERSION = 1.10.2

build-js:
	# Build bundled and minified JS
	# Requires uglifyjs
	@echo ";var djUp = jQuery.noConflict(true);" > ${STATIC_DIR}/js/jquery.init.js
	@cat ${STATIC_DIR}/js/jquery-${JQUERY_VERSION}.js ${STATIC_DIR}/js/jquery.init.js > ${STATIC_DIR}/js/jquery.bundle.js
	@cat ${STATIC_DIR}/js/jquery.bundle.js ${STATIC_DIR}/js/django-uploader.js > ${STATIC_DIR}/js/django-uploader.bundle.js
	uglifyjs ${STATIC_DIR}/js/django-uploader.bundle.js > ${STATIC_DIR}/js/django-uploader.bundle.min.js
	uglifyjs ${STATIC_DIR}/js/django-uploader.js > ${STATIC_DIR}/js/django-uploader.min.js