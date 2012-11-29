import logging

from django.utils.encoding import force_unicode
import pygments

from reviewboard.reviews.ui.base import FileAttachmentReviewUI


class XMLReviewUI(FileAttachmentReviewUI):
    """ReviewUI for XML mimetypes"""
    supported_mimetypes = ['application/xml', 'text/xml']
    template_name = 'xml_review_ui_extension/xml.html'
    object_key = 'xml'

    def render(self):
        data_string = ""
        f = self.obj.file

        try: 
            f.open()
            data_string = f.read()
        except (ValueError, IOError), e:
            logging.error('Failed to read from file %s: %s' % (self.obj.pk, e))

        f.close()
        return pygments.highlight(
            force_unicode(data_string),
            pygments.lexers.XmlLexer(),
            pygments.formatters.HtmlFormatter())
