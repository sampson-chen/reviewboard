# xml_review_ui_extension Extension for Review Board.
from reviewboard.extensions.base import Extension
from reviewboard.extensions.hooks import ReviewUIHook, \
                                         FileAttachmentThumbnailHook, \
                                         URLHook

from XMLReviewUI import XMLReviewUI
from XMLThumbnail import XMLMimetype


class XMLReviewUIExtension(Extension):
    def __init__(self, *args, **kwargs):
        super(XMLReviewUIExtension, self).__init__(*args, **kwargs)
        self.reviewui_hook = ReviewUIHook(self, [XMLReviewUI])
        self.thumbnail_hook = FileAttachmentThumbnailHook(self, [XMLMimetype])
