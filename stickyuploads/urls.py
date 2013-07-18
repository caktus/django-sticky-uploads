from django.conf.urls import patterns, url

from .views import UploadView

urlpatterns = patterns('',
    url(r'^default/$', UploadView.as_view(), name='sticky-upload-default'),
)