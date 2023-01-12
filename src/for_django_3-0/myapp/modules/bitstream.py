#!/usr/bin/env python

import unittest

class Bitstream(object):
    """
    This is a class that represents an arbitrary bit-stream.
    """
    def __init__(self):
        Bitstream.initialize(self, byte_array=None)

    def initialize(self, byte_array=None, size=0):
        if byte_array is None:
            self.__raw = bytearray([0xFF] * size)
        elif size != 0:
            raise ValueError('size attribute to initialize method only valid if byte_array not specified')
        else:
            self.__raw = byte_array

    def size(self):
        return len(self.__raw)

    def append(self, byte_array=None, size=0):
        if byte_array is None:
            if size <= 0:
                raise ValueError('size attribute to append method is <= 0')
            else:
                self.__raw += bytearray([0]*size)
        elif size != 0:
                raise ValueError('size attribute to append method only valid if byte_array not specified')
        else:
            self.__raw += byte_array

    def get_raw_byte_array(self):
        return self.__raw

    def get_raw_value(self, offset, size, endianness='little'):
        assert (offset + size <= self.size())
        raw_byte_array = self.get_raw_byte_array()

        if endianness == 'big':
            return raw_byte_array[offset:offset + size][::-1]
        else:
            return raw_byte_array[offset:offset + size]

    def set_raw_value(self, byte_array, offset, endianness='little'):
        sz = len(byte_array)
        assert (offset + sz <= self.size())

        if endianness == 'big':
            self.__raw[offset:offset + sz] = byte_array[0:sz][::-1]
        else:
            self.__raw[offset:offset + sz] = byte_array[0:sz]

    def write(self, fp):
        fp.write(self.get_raw_byte_array())

    def read(self, fp):
        if fp.closed:
            return
        self.append(byte_array=bytearray(fp.read()))


if __name__ == '__main__':
    unittest.main()
