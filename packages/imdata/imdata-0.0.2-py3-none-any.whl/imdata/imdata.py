import codecs # use codecs to encode or decode a string or a bytes
import base64 # turn all bytes into ascii codes
import zlib # compress the bytes in
import math # for auto choosing the size
import re # for split the bytes
import os.path # check for the path
from collections import deque # deque for the faster list to append items

import numpy as np # the array for the im
import imageio # to save the image


class ImData:
    "A class to save the string data by img, can format in tiff, tif, png type."

    def __init__(self, ctx: bytes=b'', fmt='png', size='auto', encode='utf-8'):
        self.ctx = ctx
        self.__old = ctx
        fmt = self.to_string(fmt)
        if fmt in 'tif tiff png'.split():
            self.fmt = '.{}'.format(fmt)
        else:
            raise FormatError('Format does not support')
        self.encode = encode
        self.size = size

    @property
    def pix(self):
        if not hasattr(self, '_pix') or self.__old != self.ctx:
            self._pix = self.bytes_pix(self.ctx, self.size, self.encode)
        return self._pix

    @pix.setter
    def pix(self):
        raise TypeError('pix attribute doesn\'t support to modify')

    @property
    def bytes(self):
        return self.ctx

    @bytes.setter
    def bytes(self, val):
        self.__old, self.ctx = self.ctx, val
        return self.ctx

    def save(self, uri, size=None):
        uri = os.path.abspath(uri)
        if not uri.endswith(self.fmt):
            raise FormatError('File name does not match with the format (%s) give in' % self.fmt)
        self.size = size if size else (self.size if self.size else 'auto')
        return imageio.imsave(uri, self.pix)

    @staticmethod
    def to_bytes(s, encode='utf-8'):
        "Change param s into bytes, according to encode(default 'utf-8')"
        if isinstance(s, bytes):
            return s # if it's bytes, return the raw arg
        try:
            return codecs.encode(s, encode) # try to encode the string according to given encode
        except TypeError:
            try:
                return codecs.encode(s, 'utf-8') # use default encode to try again
            except:
                pass
            try:
                return bytes(s) # just use bytes to turn it into bytes
            except:
                raise TypeError('Not a right object to change into bytes') # Final error

    @staticmethod
    def to_string(b, encode='utf-8'):
        "Change param b into string, according to encode(default 'utf-8')"
        if isinstance(b, str):
            return b # if it's str, return the raw string
        try:
            return codecs.decode(b, encode) # try to decode the bytes according to gievn encode
        except TypeError:
            try:
                return codecs.decode(b, 'utf-8') # use default encode to try again
            except TypeError:
                try:
                    return str(b) # Just use str to turn it
                except:
                    raise TypeError("Not a right object to change into string") # final error

    def _byte_pix(self, bs, encode='utf-8'):
        "turn bytes into pixel deque list"
        base = base64.b85encode(zlib.compress(self.to_bytes(bs, encode))) # change to base85 string, only use ascii letters
        de = deque(base)
        return de, len(base)

    def bytes_pix(self, bs, size = (400, 600), encode='utf-8'):
        "return bytes into pixel info, param bs can be a list of bytes"
        de = deque()
        if isinstance(bs, (bytes, str)):
            de, length = self._byte_pix(bs, encode)
        else:
            length = 0
            for b in iter(bs):
                pix, l = self._byte_pix(b, encode)
                de.extend(pix)
                de.extend([0,0,0])
                length += l+3
        size = (*size, 3) if size != 'auto' else self._autosize(length)
        _s = self._size(size)
        if len(de) > _s:
            raise SizeError("size {} doesn't enough for data {}".format(size, length), size, length)
        de.extend([0] * (_s - len(de)))
        return np.array(de).reshape(size).astype('uint8')

    @staticmethod
    def _size(size):
        "get the pixel numbers"
        arr = np.zeros(size)
        return arr.size

    def pix_bytes(self, pix):
        row = pix.reshape(-1)
        stri = ''.join((chr(code) if code else ' ')  for code in row[:])
        bzde = lambda s:  zlib.decompress(base64.b85decode(s.encode()))
        stri = stri.strip()
        its = stri.split()
        return [bzde(i) for i in its if i]
    
    @staticmethod
    def _autosize(length, las = (3, 4)):
        a, b = las
        length = (length / 3)
        # img size as a, b
        m = length / (a * b)
        cell = math.sqrt(m)
        size = (cell * a, cell * b, 3)
        return tuple(math.ceil(i) for i in size)

class SizeError(Exception):
    def __init__(self, ctx, need=None, has=None):
        super(SizeError, self).__init__(ctx)
        self.need = need
        self.has = has

    def __repr__(self):
        return "Size Error, need {}, has {}".format(self.need, self.has)

class FormatError(Exception): pass
