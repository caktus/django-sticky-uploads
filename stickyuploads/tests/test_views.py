from __future__ import unicode_literals

import os
import json
import shutil
import tempfile

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..compat import get_user_model
from ..storage import TempFileSystemStorage
from ..utils import serialize_upload
from .base import TempFileMixin


class UploadViewTestCase(TempFileMixin, TestCase):
    """View to handle background AJAX upload."""

    url_conf = 'stickyuploads.tests.urls'

    def setUp(self):
        super(UploadViewTestCase, self).setUp()
        User = get_user_model()
        self.user = User.objects.create_user(**{User.USERNAME_FIELD: 'test', 'password': 'test'})
        self.client.login(username='test', password='test')
        self.url = reverse('sticky-upload-default')

    def test_upload(self):
        """Handle a new file upload."""
        with open(self.temp_name, 'rb') as f:
            data = {'upload': f}
            response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        filename = os.path.basename(self.temp_name)
        # We can't test stored value because there are unknowns
        self.assertIn('stored', result)
        expected = {
            'is_valid': True,
            'filename': filename,
            'url': None,
            'stored': result['stored'],
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
        self.assertEqual(result, {'is_valid': False, 'errors': {'upload': ['The submitted file is empty.']}})
