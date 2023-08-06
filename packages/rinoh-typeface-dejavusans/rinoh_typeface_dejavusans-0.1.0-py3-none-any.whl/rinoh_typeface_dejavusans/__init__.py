from os import path

from rinoh.font import Typeface
from rinoh.font.opentype import OpenTypeFont


__all__ = ['typeface']


def otf(style):
    filename = 'DejaVuSans{}.ttf'.format(style)
    return OpenTypeFont(path.join(path.dirname(__file__), filename))


typeface = Typeface('DejaVu Sans',
                    otf(''),
                    otf('-Oblique'),
                    otf('-Bold'),
                    otf('-ExtraLight'),
                    otf('-BoldOblique'),
                    otf('Condensed'),
                    otf('Condensed-Oblique'),
                    otf('Condensed-Bold'),
                    otf('Condensed-BoldOblique'))
