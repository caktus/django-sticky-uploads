from __future__ import unicode_literals

from django.contrib import admin

from .forms import SavedUploadForm
from .models import SavedUpload


class SavedUploadAdmin(admin.ModelAdmin):
    form = SavedUploadForm


admin.site.register(SavedUpload, SavedUploadAdmin)
