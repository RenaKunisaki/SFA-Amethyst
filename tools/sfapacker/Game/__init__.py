import os.path
import struct
from .dol import DOL
from .TextureManager import TextureManager
from .MapManager import MapManager
from sfapacker.BinaryFile import BinaryFile

class Game:
    """Represents the entire game ISO."""
    # in future maybe this could accept actual ISO file
    # instead of only unpacked dir

    # boot.bin offset 7 is game version (XXX verify)
    # and offset 0 is game ID
    # and 0x20 is title, to tell demo from final

    # XXX get this from the XML files in the data browser
    addresses = {
        'U0': {
            # translates map dir IDs to map IDs (index into MAPINFO.bin)
            'mapIdXltnTbl': {'addr':0x802CBCD0, 'count':0x4B},
            # pointers to map asset dirs
            'mapDirNames':  {'addr':0x802CBBAC, 'count':0x49},
            # pointers to map romlist file names
            'mapName':      {'addr':0x802CB940, 'count':0x75},
            # array of map dir ID => parent dir ID
            'parentMapId':  {'addr':0x802CBDFC, 'count':0x4B},
        },
    }
    """List of various useful addresses in main.dol versions."""

    rootDir: str = None
    """Path to ISO root directory."""

    texMgr: TextureManager = None
    mapMgr: MapManager     = None

    def __init__(self, rootDir:str):
        pDol = os.path.join(rootDir, '..', 'sys', 'main.dol')
        self.rootDir = rootDir
        self.dol     = DOL(pDol)
        self.version = 'U0' # XXX
        self.addrs   = self.addresses[self.version]
        self.texMgr  = TextureManager(self)
        self.mapMgr  = MapManager(self)

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
