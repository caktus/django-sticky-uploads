from django.conf.urls import include, url


urlpatterns = [
    url(r'^sticky-uploads/', include('stickyuploads.urls')),
]
