from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from stickyuploads.widgets import StickyUploadWidget


class ExampleForm(forms.Form):
    upload = forms.FileField(widget=StickyUploadWidget)
    other = forms.BooleanField()


@login_required
def home(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.cleaned_data['upload']
            messages.success(request, 'You have successfully uploaded %s' % upload)
            return redirect('home')
    else:
        form = ExampleForm()
    return render(request, 'index.html', {'form': form})
