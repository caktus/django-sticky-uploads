from django.conf.urls import url

from .views import UploadView

urlpatterns = [
    url(r'^default/$', UploadView.as_view(), name='sticky-upload-default'),
]
