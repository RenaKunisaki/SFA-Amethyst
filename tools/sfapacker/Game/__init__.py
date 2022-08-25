import os.path
import struct
from .TextureManager import TextureManager
from sfapacker.BinaryFile import BinaryFile

class Game:
    """Represents the entire game ISO."""
    # in future maybe this could accept actual ISO file
    # instead of only unpacked dir

    rootDir: str = None
    """Path to ISO root directory."""

    texMgr: TextureManager = None

    def __init__(self, rootDir:str):
        self.rootDir = rootDir
        self.texMgr  = TextureManager(self)

    def openFile(self, path:str, mode:str='rb') -> BinaryFile:
        """Open a file in the ISO."""
        inPath = os.path.join(self.rootDir, path)
        return BinaryFile(inPath, mode)

    def openMapFile(self, map:str, name:str, mode:str='rb') -> BinaryFile:
        """Open a file belonging to a particular map."""
        inPath = os.path.join(self.rootDir, map, name)
        return BinaryFile(inPath, mode)

    def _makeTableFile(self, entries:list[int]) -> bytes:
        """Build .tab file contents from list of entries.

        :param entries: Table entries.
        :return: Table file contents.

        Only useful for tables that have 32-bit entries.
        Adds the appropriate padding and checksums.
        """
        data = b''.join(map(lambda n: struct.pack('>I', n), entries))
        cksum = sum(data)
        data += b'\xFF\xFF\xFF\xFF' # EOF marker

        # pad to multiple of 32 bytes
        pad = 32 - (len(data) & 0x1F)
        if pad >= 32: pad = 0
        if pad > 0: data += b'\0' * pad

        # write checksum and pad to 32 bytes again
        # (this is weird but seems to be how the original
        # files were generated)
        data += struct.pack('>I', cksum)
        pad = 32 - (len(data) & 0x1F)
        if pad >= 32: pad = 0
        if pad > 0: data += b'\0' * pad

        return data
