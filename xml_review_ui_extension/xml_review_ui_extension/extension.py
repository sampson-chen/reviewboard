# XMLReviewUIExtension Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import DashboardHook, URLHook

class XMLReviewUIExtensionURLHook(URLHook):
    def __init__(self, extension, *args, **kwargs):
        pattern = patterns('', (r'^xml_review_ui_extension/',
                            include('xml_review_ui_extension.urls')))
        super(XMLReviewUIExtensionURLHook, self).__init__(extension, pattern)


class XMLReviewUIExtensionDashboardHook(DashboardHook):
    def __init__(self, extension, *args, **kwargs):
        entries = [{
            'label': 'XML Review UI',
            'url': settings.SITE_ROOT + 'xml_review_ui_extension/',
        }]
        super(XMLReviewUIExtensionDashboardHook, self).__init__(extension,
                entries=entries, *args, **kwargs)

class XMLReviewUIExtension(Extension):
    def __init__(self, *args, **kwargs):
        super(XMLReviewUIExtension, self).__init__()
        self.url_hook = XMLReviewUIExtensionURLHook(self)
        self.dashboard_hook = XMLReviewUIExtensionDashboardHook(self)
