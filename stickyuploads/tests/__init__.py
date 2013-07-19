from django.db import models

from .base import mockstorage

class Example(models.Model):
    name = models.CharField(max_length=100)
    upload = models.FileField(storage=mockstorage, upload_to='test/')


from .test_forms import UploadFormTestCase
from .test_integration import FormIntegrationTestCase, ModelFormIntegrationTestCase
from .test_utils import SerializeTestCase, DeserializeTestCase, OpenStoredFileTestCase
from .test_views import UploadViewTestCase
from .test_widgets import StickyUploadWidgetTestCase