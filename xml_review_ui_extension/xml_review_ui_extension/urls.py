from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('xml_review_ui_extension.views',
    url(r'^$', 'dashboard'),
)
