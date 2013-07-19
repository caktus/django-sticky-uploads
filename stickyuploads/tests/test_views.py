from __future__ import unicode_literals

import os
import json
import shutil
import tempfile

from django.core.urlresolvers import reverse
from django.core.files.storage import DefaultStorage
from django.test import TestCase
from django.test.utils import override_settings

from ..compat import get_user_model
from ..utils import serialize_upload


@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage',
    MEDIA_ROOT=tempfile.gettempdir(),
    MEDIA_URL='/test-media/',
)
class UploadViewTestCase(TestCase):
    """View to handle background AJAX upload."""

    url_conf = 'stickyuploads.tests.urls'

    def setUp(self):
        super(UploadViewTestCase, self).setUp()
        User = get_user_model()
        self.user = User.objects.create_user(**{User.USERNAME_FIELD: 'test', 'password': 'test'})
        self.client.login(username='test', password='test')
        self.temp_dir = tempfile.mkdtemp()
        _, self.temp_name = tempfile.mkstemp(dir=self.temp_dir)
        with open(self.temp_name, 'w') as f:
            f.write('X')
        self.url = reverse('sticky-upload-default')

    def tearDown(self):
        super(UploadViewTestCase, self).tearDown()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_upload(self):
        """Handle a new file upload."""
        with open(self.temp_name, 'rb') as f:
            data = {'upload': f}
            response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        storage = DefaultStorage()
        filename = os.path.basename(self.temp_name)
        expected = {
            'is_valid': True,
            'filename': filename,
            'url': '/test-media/' + filename,
            'stored': serialize_upload(filename, storage),
        }
        self.assertEqual(result, expected)

    def test_upload_not_allowed(self):
        """User must be authenticated for the default upload."""
        self.client.logout()
        with open(self.temp_name, 'rb') as f:
            data = {'upload': f}
            response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 403)

    def test_empty_file(self):
        """Uploading an empty file is not valid."""
        with open(self.temp_name, 'w') as f:
            f.write('')
        with open(self.temp_name, 'rb') as f:
            data = {'upload': f}
            response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertEqual(result, {'is_valid': False})