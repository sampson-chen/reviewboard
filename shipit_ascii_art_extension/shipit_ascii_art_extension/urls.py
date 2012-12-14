from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('shipit_ascii_art_extension.views',
    url(r'^$', 'dashboard'),
)
