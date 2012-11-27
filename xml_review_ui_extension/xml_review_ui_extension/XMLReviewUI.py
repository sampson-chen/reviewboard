from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter

from reviewboard.reviews.ui.base import FileAttachmentReviewUI


class XMLReviewUI(FileAttachmentReviewUI):
    """ReviewUI for XML mimetypes"""
    supported_mimetypes = ['application/xml', 'text/xml']
    template_name = 'xml_review_ui_extension/xml.html'
    object_key = 'xml'

    def render(self):
        f = self.obj.file
        f.open()
        code = f.read()
        f.close()
        return highlight(code, XmlLexer(), HtmlFormatter())
