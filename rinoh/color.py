# This file is part of RinohType, the Python document preparation system.
#
# Copyright (c) Brecht Machiels.
#
# Use of this source code is subject to the terms of the GNU Affero General
# Public License v3. See the LICENSE file or http://www.gnu.org/licenses/.

import binascii
import struct


__all__ = ['Color', 'HexColor', 'BLACK', 'WHITE', 'RED', 'GREEN', 'BLUE',
           'Gray', 'GRAY10', 'GRAY25', 'GRAY50', 'GRAY75', 'GRAY90']


class Color(object):
    def __init__(self, red, green, blue, alpha=1):
        for value in (red, green, blue, alpha):
            if not 0 <= value <= 1:
                raise ValueError('Color component values can range from 0 to 1')
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha

    def __repr__(self):
        rgba_bytes = struct.pack(4 * 'B', *(int(color * 255)
                                            for color in self.rgba))
        return '#' + binascii.hexlify(rgba_bytes).decode('ascii')

    @property
    def rgba(self):
        return self.r, self.g, self.b, self.a


class HexColor(Color):
    def __init__(self, string):
        try:
            string = string.encode('ascii')
        except AttributeError:
            pass
        if string.startswith(b'#'):
            string = string[1:]
        try:
            r, g, b = struct.unpack('BBB', binascii.unhexlify(string[:6]))
            if string[6:]:
                a, = struct.unpack('B', binascii.unhexlify(string[6:]))
            else:
                a = 255
        except (struct.error, binascii.Error):
            raise ValueError('Bad color string passed to ' +
                             self.__class__.__name__)
        super().__init__(*(value / 255 for value in (r, g, b, a)))


class Gray(Color):
    def __init__(self, luminance, alpha=1):
        super().__init__(luminance, luminance, luminance, alpha)


BLACK = Color(0, 0, 0)
WHITE = Color(1, 1, 1)
GRAY10 = Gray(0.10)
GRAY25 = Gray(0.25)
GRAY50 = Gray(0.50)
GRAY75 = Gray(0.75)
GRAY90 = Gray(0.90)
RED = Color(1, 0, 0)
GREEN = Color(0, 1, 0)
BLUE = Color(0, 0, 1)