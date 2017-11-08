from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SavedUploadForm


@login_required
def home(request):
    if request.method == 'POST':
        form = SavedUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save()
            messages.success(request, 'You have successfully uploaded %s' % upload)
            return redirect('home')
    else:
        form = SavedUploadForm()
    return render(request, 'index.html', {'form': form})
