from setuptools import setup


PACKAGE = "shipit_ascii_art_extension"
VERSION = "0.1"

setup(
    name=PACKAGE,
    version=VERSION,
    description="An extension that adds ascii art to Review Board's ship-it reviews",
    author="Sampson Chen",
    packages=["shipit_ascii_art_extension"],
    entry_points={
        'reviewboard.extensions':
            '%s = shipit_ascii_art_extension.extension:AsciiArt' % PACKAGE,
    },
    package_data={
        'shipit_ascii_art_extension': [
            'htdocs/css/*.css',
            'htdocs/js/*.js',
            'templates/shipit_ascii_art_extension/*.txt',
            'templates/shipit_ascii_art_extension/*.html',
        ],
    }
)
