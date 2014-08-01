from __future__ import unicode_literals

import django
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
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
            currently_html = 'Currently: {0} '.format(self.temp_name)
            #Django does not allow overriding url_markup_template before 1.6
            # remove when 1.4, 1.5 support is dropped
            if django.VERSION < (1, 6):
                currently_html = 'Currently: <a href="#">{0}</a> '.format(self.temp_name)
            value = File(temp)
            setattr(value, '_seralized_location', '1234')
            self.assertHTMLEqual(self.widget.render('myfile', value),
                currently_html +
                '<input id="myfile-clear_id" name="myfile-clear" type="checkbox" />' +
                '<label for="myfile-clear_id"> Clear</label><br />' +
                'Change:<input type="file" name="myfile" data-upload-url="/sticky-uploads/default/" />' +
                '<input type="hidden" name="_myfile" value="1234" />')

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
