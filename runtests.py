#!/usr/bin/env python
import sys

import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'stickyuploads',
        ),
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        ROOT_URLCONF='stickyuploads.tests.urls',
    )
    if hasattr(django, 'setup'):
        django.setup()


from django.test.utils import get_runner


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['stickyuploads', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

