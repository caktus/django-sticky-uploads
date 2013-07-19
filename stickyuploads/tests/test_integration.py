"""Test integration of StickyUploadWidget with full Forms and ModelForms."""
from __future__ import unicode_literals

from django import forms
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, SimpleTestCase

from ..utils import serialize_upload
from ..widgets import StickyUploadWidget
from .base import TempFileMixin


class TestForm(forms.Form):
    name = forms.CharField()
    upload = forms.FileField(widget=StickyUploadWidget)


class FormIntegrationTestCase(TempFileMixin, SimpleTestCase):
    """Using StickyUploadWidget in a Form class."""

    def test_valid_from_files(self):
        """Fallback functionality to get file from passed FILES."""
        data = {'name': 'foo'}
        files = {'upload': SimpleUploadedFile('something.txt', b'content')}
        form = TestForm(data=data, files=files)
        self.assertTrue(form.is_valid())

    def test_valid_from_post(self):
        """Restore file from serialized value."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage)
            data = {'name': 'foo', '_upload': stored}
            form = TestForm(data=data, files={})
            self.assertTrue(form.is_valid())

    def test_keep_value_on_failure(self):
        """Hidden input should keep serialized value when the form is not valid."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage)
            data = {'name': '', '_upload': stored}
            form = TestForm(data=data, files={})
            self.assertFalse(form.is_valid())
            expected = 'value="{0}"'.format(stored)
            self.assertIn(stored, form.as_p())