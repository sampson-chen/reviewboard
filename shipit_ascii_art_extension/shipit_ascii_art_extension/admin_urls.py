from django.conf.urls.defaults import patterns, url

from shipit_ascii_art_extension.extension import AsciiArt


urlpatterns = patterns('shipit_ascii_art_extension.views',
    url(r'^$', 'configure'),
)
