from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^sticky-uploads/', include('stickyuploads.urls')),
)