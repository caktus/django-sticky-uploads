STATIC_DIR = ./stickyuploads/static/stickyuploads
UPLOADER = ${STATIC_DIR}/js/django-uploader.js

dist: lint-js build-js test
	python setup.py sdist
	python setup.py bdist_wheel --universal

build-js: $(UPLOADER)
	# Build minified JS
	# Requires uglifyjs
	uglifyjs ${UPLOADER} > ${STATIC_DIR}/js/django-uploader.min.js

lint-js:
	# Check JS for any problems
	# Requires jshint
	jshint ${STATIC_DIR}/js/django-uploader.js

test:
	tox

clean: ${STATIC_DIR}/js/django-uploader.min.js
	rm $^

.PHONY: lint-js clean build-js dist test
