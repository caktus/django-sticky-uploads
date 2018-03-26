from __future__ import unicode_literals

import django
from django import forms
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
try:
    # Older django versions
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse
from django.test import SimpleTestCase
from django.utils.encoding import python_2_unicode_compatible

from ..utils import serialize_upload
from ..widgets import StickyUploadWidget
from .base import TempFileMixin


@python_2_unicode_compatible
class FakeFieldFile(object):
    """
    Quacks like a FieldFile (has a .url and unicode representation), but
    doesn't require us to care about storages etc.
    """

    url = 'something'

    def __str__(self):
        return self.url


class ClearableFileInputWidgetTestCase(TempFileMixin, SimpleTestCase):
    """
    Make sure the widget we're subclassing doesn't change its behavior across Django versions, etc.
    """

    def setUp(self):
        super(ClearableFileInputWidgetTestCase, self).setUp()
        self.widget = forms.ClearableFileInput()
        self.url = reverse('sticky-upload-default')

    def test_render(self):
        """Default render of the widget without any value."""
        actual_html = self.widget.render('myfile', None)
        expected_html = '<input name="myfile" type="file" />'
        self.assertHTMLEqual(expected_html, actual_html)

    def test_render_with_initial(self):
        """Render with standard FieldFile."""
        value = FakeFieldFile()
        expected_html = '''Currently: <a href="something">something</a> <input id="myfile-clear_id" name="myfile-clear" type="checkbox" /> <label for="myfile-clear_id">Clear</label><br />Change: <input name="myfile" type="file" />'''
        actual_html = self.widget.render('myfile', value)
        self.assertHTMLEqual(expected_html, actual_html)

    def test_value_from_files(self):
        """Get uploaded file from the FILES as normal."""
        f = SimpleUploadedFile('something.txt', b'content')
        value = self.widget.value_from_datadict(data={}, files={'myfile': f}, name='myfile')
        self.assertEqual(value, f)


class StickyUploadWidgetTestCase(TempFileMixin, SimpleTestCase):
    """Customized file widget which restored values from the serialized store."""

    def setUp(self):
        super(StickyUploadWidgetTestCase, self).setUp()
        self.widget = StickyUploadWidget()
        self.url = reverse('sticky-upload-default')

    def test_render(self):
        """Default render of the widget without any value."""
        self.assertHTMLEqual(self.widget.render('myfile', None),
            '<input type="file" name="myfile" data-upload-url="/sticky-uploads/default/" />' +
            '<input type="hidden" name="_myfile" />')

    def test_render_with_initial(self):
        """Render with standard FieldFile."""
        value = FakeFieldFile()
        self.assertHTMLEqual(self.widget.render('myfile', value),
            'Currently: <a href="something">something</a> ' +
            '<input id="myfile-clear_id" name="myfile-clear" type="checkbox" />' +
            '<label for="myfile-clear_id"> Clear</label><br />' +
            'Change:<input type="file" name="myfile" data-upload-url="/sticky-uploads/default/" />' +
            '<input type="hidden" name="_myfile" />')

    def test_render_with_restored_file(self):
        """Render with File which has been restored."""
        with open(self.temp_name) as temp:
            if django.VERSION >= (1, 11):
                # The widget markup changed in Django 1.11
                expected_html = (
                    'Currently: <a href="#">{0}</a>\n'
                    '<input type="checkbox" name="myfile-clear" id="myfile-clear_id" />\n'
                    '<label for="myfile-clear_id">Clear</label><br />\n'
                    'Change:\n'
                    '<input type="file" name="myfile" data-upload-url="/sticky-uploads/default/" />\n'
                    '<input type="hidden" name="_myfile" value="1234" />').format(self.temp_name)
            else:
                expected_html = (
                    'Currently: {0} ' +
                    '<input id="myfile-clear_id" name="myfile-clear" type="checkbox" />' +
                    '<label for="myfile-clear_id"> Clear</label><br />' +
                    'Change:<input type="file" name="myfile" data-upload-url="/sticky-uploads/default/" />' +
                    '<input type="hidden" name="_myfile" value="1234" />').format(self.temp_name)

            value = File(temp)
            setattr(value, '_seralized_location', '1234')
            self.assertHTMLEqual(self.widget.render('myfile', value), expected_html)

    def test_value_from_files(self):
        """Get uploaded file from the FILES as normal."""
        f = SimpleUploadedFile('something.txt', b'content')
        value = self.widget.value_from_datadict(data={}, files={'myfile': f}, name='myfile')
        self.assertEqual(value, f)

    def test_value_from_post(self):
        """Get uploaded file by restoring value from the POST."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage, self.url)
            value = self.widget.value_from_datadict(data={'_myfile': stored}, files={}, name='myfile')
            self.assertTrue(isinstance(value, File))
            self.assertEqual(value._seralized_location, stored)

    def test_value_from_wrong_urls(self):
        """Widget should not restore a value from a url other than the one specified."""
        with self.settings(MEDIA_ROOT=self.temp_dir):
            storage = FileSystemStorage()
            stored = serialize_upload(self.temp_name, storage, '/some-other/url/')
            value = self.widget.value_from_datadict(data={'_myfile': stored}, files={}, name='myfile')
            self.assertIsNone(value)
