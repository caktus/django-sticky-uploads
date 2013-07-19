"""Utitilies for writing tests manipulating temporary files/directories."""

import shutil
import tempfile


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