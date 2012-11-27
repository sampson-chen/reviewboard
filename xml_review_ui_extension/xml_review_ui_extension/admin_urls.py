from django.conf.urls.defaults import patterns, url

from xml_review_ui_extension.extension import XMLReviewUIExtension


urlpatterns = patterns('xml_review_ui_extension.views',
    url(r'^$', 'configure'),
)
