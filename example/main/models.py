from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


@python_2_unicode_compatible
class SavedUpload(models.Model):
    """Simple saved upload."""

    name = models.CharField(max_length=100)
    upload = models.FileField(upload_to='uploads/')
    added = models.DateTimeField(default=now)

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.upload)