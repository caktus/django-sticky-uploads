from __future__ import unicode_literals

from django import forms
from django.core.exceptions import ValidationError

from stickyuploads.widgets import StickyUploadWidget

from .models import SavedUpload


class SavedUploadForm(forms.ModelForm):
    use_required_attribute = False

    # Allow user to choose whether the submission works or not.
    accept_submission = forms.BooleanField(
        widget=forms.CheckboxInput,
        label="Accept form submission",
        required=False,
    )

    class Meta:
        model = SavedUpload
        fields = ('name', 'accept_submission', 'upload', )
        widgets = {
            'upload': StickyUploadWidget
        }

    def clean_accept_submission(self):
        if not self.cleaned_data.get('accept_submission', False):
            raise ValidationError("This box must be checked for the form to be valid")
