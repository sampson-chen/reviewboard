from reviewboard.signals import initializing


def _register_mimetype_handlers(**kwargs):
    """Registers all bundled Mimetype Handlers."""
    from reviewboard.attachments.mimetypes import register_mimetype_handler
    from reviewboard.attachments.mimetypes import MimetypeHandler
    from reviewboard.attachments.mimetypes import ImageMimetype
    from reviewboard.attachments.mimetypes import TextMimetype
    from reviewboard.attachments.mimetypes import ReStructuredTextMimeType
    from reviewboard.attachments.mimetypes import MarkDownMimeType

    register_mimetype_handler(MimetypeHandler)
    register_mimetype_handler(ImageMimetype)
    register_mimetype_handler(TextMimetype)
    register_mimetype_handler(ReStructuredTextMimeType)
    register_mimetype_handler(MarkDownMimeType)


initializing.connect(_register_mimetype_handlers)
