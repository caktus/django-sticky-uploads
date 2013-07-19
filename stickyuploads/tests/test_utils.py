from __future__ import unicode_literals

import shutil
import tempfile

from django.conf import settings
from django.core import signing
from django.core.files import File
from django.core.files.storage import FileSystemStorage, DefaultStorage
from django.test import SimpleTestCase
from django.utils import unittest

from .. import utils


class SerializeTestCase(unittest.TestCase):
    """Serialize a file along with its storage."""

    def test_serialize(self):
        """Serialize mapping of file and storage."""
        storage = FileSystemStorage()
        result = utils.serialize_upload('test.png', storage)
        expected = signing.dumps({
            'name': 'test.png',
            'storage': 'django.core.files.storage.FileSystemStorage',
        })
        self.assertEqual(result, expected)

    def test_lazy_storge(self):
        """Serialize lazy storage such as DefaultStorage."""
        storage = DefaultStorage()
        result = utils.serialize_upload('test.png', storage)
        expected = signing.dumps({
            'name': 'test.png',
            'storage': settings.DEFAULT_FILE_STORAGE,
        })
        self.assertEqual(result, expected)


class DeserializeTestCase(SimpleTestCase):
    """Deserialize a file along with its storage class."""

    def test_deserialize(self):
        """Deserialize mapping of file and storage."""
        storage = FileSystemStorage()
        value = utils.serialize_upload('test.png', storage)
        result = utils.deserialize_upload(value)
        expected = {
            'name': 'test.png',
            'storage': FileSystemStorage,
        }
        self.assertEqual(result, expected)

    def test_bad_signature(self):
        """Attempt to restore when SECRET_KEY has changed."""
        storage = FileSystemStorage()
        value = utils.serialize_upload('test.png', storage)
        with self.settings(SECRET_KEY='1234'):
            result = utils.deserialize_upload(value)
        expected = {
            'name': None,
            'storage': None,
        }
        self.assertEqual(result, expected)

    def test_unknown_storage(self):
        """Attempt to restore storage class which is no longer importable."""
        value = signing.dumps({
            'name': 'test.png',
            'storage': 'does.not.exist',
        })
        result = utils.deserialize_upload(value)
        expected = {
            'name': None,
            'storage': None,
        }
        self.assertEqual(result, expected)


class OpenStoredFileTestCase(SimpleTestCase):
    """Deserialize and open file from a storage."""

    def setUp(self):
        super(OpenStoredFileTestCase, self).setUp()
        self.temp_dir = tempfile.mkdtemp()
        _, self.temp_name = tempfile.mkstemp(dir=self.temp_dir)
        with open(self.temp_name, 'w') as f:
            f.write('X')

    def tearDown(self):
        super(OpenStoredFileTestCase, self).tearDown()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_open_file(self):
        """Restore and open file from storage."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            value = utils.serialize_upload(self.temp_name, storage)
            result = utils.open_stored_file(value)
            self.assertTrue(isinstance(result, File))
            self.assertEqual(result.name, self.temp_name)

    def test_bad_signature(self):
        """Attempt to open file when SECRET_KEY has changed."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            value = utils.serialize_upload(self.temp_name, storage)
            with self.settings(SECRET_KEY='1234'):
                result = utils.open_stored_file(value)
                self.assertIsNone(result)

    def test_unknown_storage(self):
        """Attempt to open file with storage class which is no longer importable."""
        value = signing.dumps({
            'name': self.temp_name,
            'storage': 'does.not.exist',
        })
        result = utils.open_stored_file(value)
        self.assertIsNone(result)

    def test_file_does_not_exist(self):
        """Restore file not found in the storage."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            value = utils.serialize_upload('test.png', storage)
            result = utils.open_stored_file(value)
            self.assertIsNone(result)