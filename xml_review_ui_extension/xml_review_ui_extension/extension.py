# xml_review_ui_extension Extension for Review Board.
from django.conf.urls.defaults import patterns, include

from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewUIHook, URLHook

from XMLReviewUI import XMLReviewUI


class XMLReviewUIExtension(Extension):
    def __init__(self, *args, **kwargs):
        super(XMLReviewUIExtension, self).__init__(*args, **kwargs)
        pattern = patterns('', (r'^xml_review_ui_extension/',
                           include('xml_review_ui_extension.urls')))
        self.url_hook = URLHook(self, pattern)
        self.reviewui_hook = ReviewUIHook(self, [XMLReviewUI])
