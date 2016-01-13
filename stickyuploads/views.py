from __future__ import unicode_literals

import json

from django.core.files.storage import get_storage_class
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import View

from .forms import UploadForm


class UploadView(View):
    """Base view class for accepting file uploads."""

    form_class = UploadForm
    storage_class = 'stickyuploads.storage.TempFileSystemStorage'

    def post(self, *args, **kwargs):
        """Save file and return saved info or report errors."""
        if self.upload_allowed():
            form = self.get_upload_form()
            result = {}
            if form.is_valid():
                storage = self.get_storage()
                result['is_valid'] = True
                info = form.stash(storage, self.request.path)
                result.update(info)
            else:
                result.update({
                    'is_valid': False,
                    'errors': form.errors,
                })
            return HttpResponse(json.dumps(result), content_type='application/json')
        else:
            return HttpResponseForbidden()

    def get_storage(self):
        """Get storage instance for saving the temporary upload."""
        return get_storage_class(self.storage_class)()

    def upload_allowed(self):
        """Check if the current request is allowed to upload files."""
        return self.request.user.is_authenticated()

    def get_upload_form(self):
        """Construct form for accepting file upload."""
        return self.form_class(self.request.POST, self.request.FILES)