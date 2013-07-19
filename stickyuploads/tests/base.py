"""Utitilies for writing tests manipulating temporary files/directories."""

import shutil
import tempfile

from mock import Mock


class MockStorage(Mock):

    def save(self, name, upload):
        return name

    def url(self, name):
        return '/uploads/{0}'.format(name)

    def get_valid_name(self, name):
        return name


mockstorage = MockStorage()


class TempFileMixin(object):

    def setUp(self):
        super(TempFileMixin, self).setUp()
        self.temp_dir = tempfile.mkdtemp()
        _, self.temp_name = tempfile.mkstemp(dir=self.temp_dir)
        with open(self.temp_name, 'w') as f:
            f.write('X')

    def tearDown(self):
        super(TempFileMixin, self).tearDown()
        shutil.rmtree(self.temp_dir, ignore_errors=True)