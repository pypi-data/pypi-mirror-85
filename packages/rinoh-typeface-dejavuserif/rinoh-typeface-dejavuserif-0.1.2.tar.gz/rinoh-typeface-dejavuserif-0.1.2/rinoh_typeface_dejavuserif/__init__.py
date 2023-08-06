from os import path

from rinoh.font import Typeface
from rinoh.font.opentype import OpenTypeFont


__all__ = ['typeface']


def otf(style):
    filename = 'DejaVuSerif{}.ttf'.format(style)
    return OpenTypeFont(path.join(path.dirname(__file__), filename))


typeface = Typeface('DejaVu Serif',
                    otf(''),
                    otf('-Italic'),
                    otf('-Bold'),
                    otf('-BoldItalic'),
                    otf('Condensed'),
                    otf('Condensed-Italic'),
                    otf('Condensed-Bold'),
                    otf('Condensed-BoldItalic'))
