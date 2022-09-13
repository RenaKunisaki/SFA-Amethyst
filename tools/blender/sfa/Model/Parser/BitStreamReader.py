# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations

class BitStreamReader:
    """Allows data to be read in arbitrary bit-lengths from a stream."""

    def __init__(self, buffer:bytes) -> None:
        self.buffer = buffer
        self.offset = 0
        self.length = len(buffer) * 8

    def _getU24(self) -> int:
        byteOffs = self.offset >> 3
        shift    = self.offset & 7
        b1, b2, b3 = 0, 0, 0
        try:
            b3 = self.buffer[byteOffs]
            b2 = self.buffer[byteOffs+1]
            b1 = self.buffer[byteOffs+2]
        except IndexError:
            pass
        return ((b1 << 16) | (b2 << 8) | b3) >> shift

    def read(self, size) -> int:
        """Read `size` bits from the stream and return them."""
        assert size <= 24
        val = self._getU24() & ((1 << size) - 1)
        self.offset += size
        return val

    def seek(self, offset, whence=0) -> int:
        if   whence in (0, 'set'): self.offset = offset
        elif whence in (1, 'cur'): self.offset += offset
        elif whence in (2, 'end'): self.offset = self.length - offset
        else: raise ValueError("Invalid `whence` parameter: %r" % whence)
        if self.offset < 0: self.offset = 0
        if self.offset >= self.length: self.offset = self.length - 1
        return self.offset

    def isEof(self) -> bool:
        return self.offset >= self.length

