from __future__ import unicode_literals

from django import forms

from stickyuploads.widgets import StickyUploadWidget

from .models import SavedUpload


class SavedUploadForm(forms.ModelForm):

    class Meta:
        model = SavedUpload
        fields = ('name', 'upload', )
        widgets = {
            'upload': StickyUploadWidget
        }