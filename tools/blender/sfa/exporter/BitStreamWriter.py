import struct

class BitStreamWriter:
    """Packs data of arbitrary bit-lengths into a stream."""
    def __init__(self) -> None:
        self.data = b''

        self._curByte = 0
        self._curShift = 0

    def addBits(self, nBits:int, val:int):
        """Add a value to the stream.

        :param nBits: Number of bits.
        :param val: Value to add.
        """
        for i in range(nBits-1, -1, -1):
            self._curByte = (self._curByte << 1) | ((val >> i) & 1)
            self._curShift += 1
            if self._curShift >= 8:
                self.data += struct.pack('>B', self._curByte)
                self._curByte = 0
                self._curShift = 0

    def finish(self) -> bytes:
        if self._curShift > 0:
            self.data += struct.pack('>B', self._curByte)
        return self.data
