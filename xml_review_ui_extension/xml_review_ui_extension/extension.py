# xml_review_ui_extension Extension for Review Board.
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import DashboardHook, ReviewUIHook, URLHook

from XMLReviewUI import XMLReviewUI

class XMLReviewUIExtensionURLHook(URLHook):
    def __init__(self, extension, *args, **kwargs):
        pattern = patterns('', (r'^xml_review_ui_extension/',
                            include('xml_review_ui_extension.urls')))
        super(XMLReviewUIExtensionURLHook, self).__init__(extension, pattern)


class XMLReviewUIExtensionDashboardHook(DashboardHook):
    def __init__(self, extension, *args, **kwargs):
        entries = [{
            'label': 'XML Review UI Extension',
            'url': settings.SITE_ROOT + 'xml_review_ui_extension/',
        }]
        super(XMLReviewUIExtensionDashboardHook, self).__init__(extension,
                entries=entries, *args, **kwargs)


class XMLReviewUIHook(ReviewUIHook):
    """Hook responsible for registering XMLReviewUI into RB"""
    def __init__(self, extension, *args, **kwargs):
        review_uis = [XMLReviewUI]
        super(XMLReviewUIHook, self).__init__(extension, review_uis)


class XMLReviewUIExtension(Extension):
    is_configurable = True
    def __init__(self, *args, **kwargs):
        super(XMLReviewUIExtension, self).__init__()
        self.url_hook = XMLReviewUIExtensionURLHook(self)
        self.dashboard_hook = XMLReviewUIExtensionDashboardHook(self)
        self.reviewui_hook = XMLReviewUIHook(self)
