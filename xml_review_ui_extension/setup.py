from setuptools import setup


PACKAGE = "xml_review_ui_extension"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="Sample Extension to Register a Review UI",
    author="Sampson Chen",
    packages=["xml_review_ui_extension"],
    entry_points={
        'reviewboard.extensions':
            '%s = xml_review_ui_extension.extension:XMLReviewUIExtension' % PACKAGE,
    },
    package_data={
        'xml_review_ui_extension': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/xml_review_ui_extension/*.txt',
            'templates/xml_review_ui_extension/*.html',
        ],
    }
)
