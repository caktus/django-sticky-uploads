"""Test integration of StickyUploadWidget with full Forms and ModelForms."""
from __future__ import unicode_literals

from django import forms

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase, SimpleTestCase

from ..utils import serialize_upload
from ..widgets import StickyUploadWidget
from . import Example
from .base import TempFileMixin, mockstorage


class TestForm(forms.Form):
    name = forms.CharField()
    upload = forms.FileField(widget=StickyUploadWidget)


class FormIntegrationMixin(object):
    """Tests for form compatibility."""

    form_class = None
    url_conf = 'stickyuploads.tests.urls'

    def setUp(self):
        super(FormIntegrationMixin, self).setUp()
        self.url = reverse('sticky-upload-default')

    def test_valid_from_files(self):
        """Fallback functionality to get file from passed FILES."""
        data = {'name': 'foo'}
        files = {'upload': SimpleUploadedFile('something.txt', b'content')}
        form = self.form_class(data=data, files=files)
        self.assertTrue(form.is_valid())

    def test_valid_from_post(self):
        """Restore file from serialized value."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage, self.url)
            data = {'name': 'foo', '_upload': stored}
            form = self.form_class(data=data, files={})
            self.assertTrue(form.is_valid())

    def test_keep_value_on_failure(self):
        """Hidden input should keep serialized value when the form is not valid."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage, self.url)
            data = {'name': '', '_upload': stored}
            form = self.form_class(data=data, files={})
            self.assertFalse(form.is_valid())
            expected = 'value="{0}"'.format(stored)
            self.assertIn(stored, form.as_p())


class FormIntegrationTestCase(TempFileMixin, FormIntegrationMixin, SimpleTestCase):
    """Using StickyUploadWidget in a Form class."""

    form_class = TestForm


class ExampleForm(forms.ModelForm):

    class Meta:
        model = Example
        fields = ('name', 'upload', )
        widgets = {
            'upload': StickyUploadWidget
        }


class ModelFormIntegrationTestCase(TempFileMixin, FormIntegrationMixin, TestCase):
    """Using StickyUploadWidget in a ModelForm class."""

    form_class = ExampleForm

    def test_save(self):
        """Save the model from the valid model form."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage, self.url)
            data = {'name': 'foo', '_upload': stored}
            form = self.form_class(data=data, files={})
            self.assertTrue(form.is_valid())
            instance = form.save()
            self.assertTrue(instance.upload)
