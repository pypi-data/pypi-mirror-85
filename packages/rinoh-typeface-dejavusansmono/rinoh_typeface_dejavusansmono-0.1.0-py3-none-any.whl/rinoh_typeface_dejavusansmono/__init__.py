from os import path

from rinoh.font import Typeface
from rinoh.font.opentype import OpenTypeFont


__all__ = ['typeface']


def otf(style):
    filename = 'DejaVuSansMono{}.ttf'.format(style)
    return OpenTypeFont(path.join(path.dirname(__file__), filename))


typeface = Typeface('DejaVu Sans Mono',
                    otf(''),
                    otf('-Oblique'),
                    otf('-Bold'),
                    otf('-BoldOblique'))
