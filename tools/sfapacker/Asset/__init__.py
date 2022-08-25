import zlib
import struct
import xml.etree.ElementTree as ET
from ctypes import Structure
from enum import Enum
import warnings
from .. import BinaryFile

class Asset:
    """Base class for game assets."""
    name: str
    """The filename"""

    id: int
    """The asset ID used in the game"""

    def __init__(self, name=None, id=None) -> None:
        self.name  = name
        self.id    = id

    def toXml(self) -> ET.Element:
        """Make XML element for this asset."""
        raise NotImplementedError


    def _compress(self, data:bytes, fmt='ZLB', **kw) -> bytes:
        """Compress the given data.

        :param data: Data to compress.
        :param fmt: Compression format to use.
        """
        if fmt == 'ZLB': return self._compressZLB(data, **kw)
        else: raise NotImplementedError("Unsupported compression format")


    def _compressZLB(self, data:bytes, level=9, wbits=13):
        """Compress the given data using ZLB format.

        :param data: Data to compress.
        :param level: level parameter for Zlib.
        :param wbits: wbits parameter for Zlib.
        """
        comp  = zlib.compressobj(level=level,wbits=wbits)
        cData = comp.compress(data) + comp.flush()
        return (
            b'ZLB\0' + b'\0\0\0\x01' + # magic, version
            struct.pack('>II', len(data), len(cData)) +
            cData)


    def _decompress(self, file:BinaryFile, offset:int=None):
        """Read a compressed asset and decompress it."""
        extParams = {} # extra metadata present in the header
        if offset is not None: file.seek(offset)
        sig  = file.readStruct('4s')
        offs = file.tell()
        decLen:int  = None # decoded (raw) data length
        compLen:int = None # packed (compressed) data length
        data:bytes  = None # result
        compFmt     = None # compression format

        if sig == b"\xFA\xCE\xFE\xED": # wrapper used by game
            header = file.readStruct('3I')
            decLen, zlbDataOffs, compLen = header
            compLen += 0x10
            zlbDataOffs = (zlbDataOffs*4) + offs
            extParams['archiveFmt'] = 'FACEFEED'
            extParams['unknown'] = []
            while file.tell() < zlbDataOffs:
                extParams['unknown'].append(file.readu32())
            # following is ZLB data (no header)
            compFmt = 'zlb'

        elif sig == b"ZLB\0": # zlib compression
            version = file.readu32()
            decLen  = file.readu32()
            compLen = file.readu32()
            if version != 1:
                warnings.warn(f"ZLB version is {version}, expected 1")
            compFmt = 'zlb'
            extParams['archiveFmt'] = 'ZLB'

        # sig can be 'DIR\0' or 'DIRn', they mean the same
        elif sig[0:3] == b'DIR': # not compressed
            version  = file.readu32()
            decLen   = file.readu32()
            _compLen = file.readu32()
            extParams['unknown'] = []
            extParams['archiveFmt'] = 'DIR'
            for i in range(4):
                extParams['unknown'].append(file.readu32())
            if version not in (0, 1):
                warnings.warn(f"DIR version is {version}, expected 0 or 1")
            if _compLen != decLen:
                warnings.warn(f"DIR packed length ({_compLen}) doesn't match raw length ({decLen})")

        # other signatures that can appear in old versions of the game:
        # 'LZO'(?), 0xE0E0E0E0, 0xF0F0F0F0

        if compFmt is None: # not compressed
            data = file.read(decLen)
        elif compFmt == 'zlb': # zlib compression
            packed = file.read(compLen)
            data   = zlib.decompress(packed)
            if len(data) != decLen:
                warnings.warn(f"Unpacked data length is {len(data)}, expected {decLen}")
        else:
            raise ValueError("Unsupported compression format")

        return data, extParams

