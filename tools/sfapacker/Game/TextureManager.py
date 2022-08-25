from distutils.log import warn
import enum
import hashlib
import os.path
import warnings
import struct
import xml.etree.ElementTree as ET
from PIL import Image
from ..Asset.Texture import Texture, Header, GX
from ..BinaryFile import BinaryFile

class TextureManager:
    """Manages packing/unpacking textures."""

    game = None
    """The Game instance."""

    texTable: list[int] = None
    """Texture ID => index lookup table from TEXTABLE.bin."""

    texTableInv: dict[int, int] = None
    """Texture index => ID lookup table."""


    def __init__(self, game):
        self.game = game


    # XXX maybe not useful
    def _readTexTable(self, force=False) -> None:
        """Read the index lookup table."""
        if (self.texTable is not None) and (not force): return
        self.texTable, self.texTableInv = [], {}
        path = os.path.join(self.game.rootDir, 'TEXTABLE.bin')
        with BinaryFile(path, 'rb') as file:
            while file.tell() + 2 <= file.size:
                entry = file.readu16() # texture index
                idx = entry
                #if idx < 3000 or len(self.texTable) == 0: idx += 1
                if idx != 0 and idx != 0xFFFF:
                    self.texTableInv[idx] = len(self.texTable)
                self.texTable.append(entry)
        #print("TEX TABLE", list(map(lambda it: '%04X=%04X'%it, enumerate(self.texTable))))
        #print("INV TABLE", list(map(lambda it: '%04X=%04X'%it, self.texTableInv.items())))


    def texIdToIndex(self, tId:int) -> int:
        """Convert a texture ID to a texture index."""
        if tId < 0: # the game uses negative IDs to bypass translation
            return -tId
        elif tId >= 0x8000:
            # negative 16-bit or 32-bit texture IDs that may get
            # incorrectly interpreted as large IDs
            return tId & 0x7FFF
        else:
            self._readTexTable()
            try:
                res = self.texTable[tId]
                if res == 0xFFFF: return None # deleted ID
                if tId < 3000 or res == 0: res += 1 # game does this
                return res
            except IndexError: # invalid ID
                return None


    def getTexturesInMap(self, mapDir:str) -> dict[int, bool]:
        """Build a map of which textures are present
        in the given map directory."""
        self._readTexTable()

        result = {}
        fTab0  = self.game.openMapFile(mapDir, 'TEX0.tab')
        fTab1  = self.game.openMapFile(mapDir, 'TEX1.tab')

        for tId, idx in enumerate(self.texTable):
            if tId < 3000 or idx == 0: idx += 1 # game does this
            # most deleted texture IDs refer to ID 0 (which becomes
            # 1 because of the check above) which is the placeholder
            # texture. Some refer to -1 which gives the same.
            if idx == 0xFFFF or idx == 1: continue

            fTab0.seek(idx*4)
            fTab1.seek(idx*4)
            try: t0 = fTab0.readu32()
            except struct.error: t0 = 0
            try: t1 = fTab1.readu32()
            except struct.error: t1 = 0
            if (t0 & 0xC0000000) != 0 or (t1 & 0xC0000000) != 0:
                result[tId] = True
            else: result[tId] = False
            print("tId %08X idx %08X T0 %08X T1 %08X" % (
                tId, idx, t0, t1))

        return result


    def unpackMapTextures(self, mapDir:str, which:int) \
    -> list[Texture]:
        """Unpack textures from specified map directory.

        :param mapDir: Directory within game filesystem, eg "animtest"
        :param which: Which texture file to unpack (0 or 1)
        :return: list of textures.
        """
        self._readTexTable()

        # open the files
        inPath = os.path.join(self.game.rootDir, mapDir,
            f'TEX{which}')
        try: binFile = BinaryFile(inPath+'.bin', 'rb')
        except FileNotFoundError:
            binFile = BinaryFile(inPath+'.BIN', 'rb')
        try: tabFile = BinaryFile(inPath+'.tab', 'rb')
        except FileNotFoundError:
            tabFile = BinaryFile(inPath+'.TAB', 'rb')

        result = self._unpackTextureFile(binFile, tabFile, which)
        binFile.close()
        tabFile.close()
        return result


    def unpackTexPre(self) -> list[Texture]:
        """Unpack textures from TEXPRE.bin.

        :return: a list of textures.
        """
        inPath = os.path.join(self.game.rootDir, 'TEXPRE')
        binFile = BinaryFile(inPath+'.bin', 'rb')
        tabFile = BinaryFile(inPath+'.tab', 'rb')

        result = self._unpackTextureFile(binFile, tabFile, 2)
        binFile.close()
        tabFile.close()
        return result


    def _unpackTextureFile(self, binFile:BinaryFile,
    tabFile:BinaryFile, which:int) -> list[Texture]:
        result: list[Texture] = [] # the textures
        idx = 0 # which entry index
        while True:
            tabEntry = tabFile.readu32()
            if tabEntry == 0xFFFFFFFF: break
            # skip the placeholder entry for missing textures
            if tabEntry == 0x01000000 and idx > 0:
                idx += 1
                continue

            offset  = tabEntry & 0x00FFFFFF
            nFrames = (tabEntry >> 24) & 0x3F
            flags   = tabEntry >> 30 # table override?
            if flags == 0: continue # texture not present

            tex = Texture(idx, nFrames, which)
            tex.unpackFromFile(binFile, offset * 2)
            result.append(tex)
            idx += 1
        return result


    def packFromDir(self, path:str, elem:ET.Element) -> \
    list[dict[int, Texture]]:
        """Read files from disk and pack to Texture.

        :param path: Path to the directory containing the image files.
        :param elem: XML Element containing Texture elements.
        :return: a list containing three dicts of idx => Texture;
            one for TEX0, TEX1, and TEXPRE.
        """
        result = [ {}, {}, {} ]
        for eTexture in elem.findall('Texture'):
            tex = Texture.fromImages(path, eTexture)
            result[tex.whichFile][tex.id] = tex
        return result


    def packToData(self, path:str, elem:ET.Element) \
    -> dict[str, bytes]:
        """Read files from disk and pack to game binary files.

        :param path: Path to the directory containing the image files.
        :param elem: XML Element containing Texture elements.
        :return: a dict of file name => data, containing the data
            for TEX0.bin, TEX0.tab, TEX1.bin, TEX1.tab,
            TEXPRE.bin, TEXPRE.tab. Each entry may be None if
            no textures were found for that file.
        """
        files  = self.packFromDir(path, elem)
        result = {
            'TEX0.bin':   None, 'TEX0.tab':   None,
            'TEX1.bin':   None, 'TEX1.tab':   None,
            'TEXPRE.bin': None, 'TEXPRE.tab': None,
        }
        maxId = max(
            # add a 0 entry in case keys() is empty
            max([0] + list(files[0].keys())),
            max([0] + list(files[1].keys())),
            max([0] + list(files[2].keys())),
        )
        print("max ID", hex(maxId))
        tabs    = [ [], [], [] ]
        bins    = [ [], [], [] ]
        offsets = [  0,  0,  0 ]
        for i in range(maxId+1):
            tabs[0].append(0x01000000)
            tabs[1].append(0x01000000)
            tabs[2].append(0x01000000)

        for eTexture in elem.findall('Texture'):
            fid, tid = eTexture.get('id').split(':')
            fid  = int(fid, 16)
            tid  = int(tid, 16)
            tex  = files[fid][tid]
            data = tex.toBinary()
            offs = offsets[fid]
            try: tabs[fid][tid] = (0x80000000 |
                (len(tex.frames) << 24) | (offs >> 1))
            except IndexError:
                print("ERROR %X:%04X" % (fid, tid))
                raise
            offsets[fid] += len(data)
            bins[fid].append(data)

        for i, name in enumerate(Texture.DIR_NAMES):
            if len(bins[i]) > 0:
                result[name+'.bin'] = b''.join(bins[i])
                result[name+'.tab'] = self.game._makeTableFile(tabs[i])
        return result


    def getTextureStats(self):
        """Analyze all texture headers and list all observed
        values for each field.
        """
        fields = {}
        hashes = set()
        for field in Header._fields_:
            name, typ = field
            if typ is GX.TexObj:
                for f2 in GX.TexObj._fields_:
                    n2, t2 = f2
                    fields['TexObj_'+n2] = {}
            else:
                fields[name] = {}
        for name in os.listdir(self.game.rootDir):
            path = os.path.join(self.game.rootDir, name)
            try:
                tex0 = self.game.texMgr.unpackMapTextures(path, 0)
                tex1 = self.game.texMgr.unpackMapTextures(path, 1)
                textures = list(tex0.values()) + list(tex1.values())
                for tex in textures:
                    for frame in tex.frames:
                        for name in fields.keys():
                            if name.startswith('TexObj_'):
                                val = getattr(frame.header.texObj,
                                    name[7:])
                            else:
                                val = getattr(frame.header, name)
                            if val not in fields[name]:
                                fields[name][val] = 0
                            fields[name][val] += 1
                        hash = hashlib.md5()
                        hash.update(frame.imageData)
                        hashes.add(hash.hexdigest())
            except (FileNotFoundError, NotADirectoryError):
                pass

        texPre = self.game.texMgr.unpackTexPre()
        for tex in texPre.values():
            for frame in tex.frames:
                for name in fields.keys():
                    if name.startswith('TexObj_'):
                        val = getattr(frame.header.texObj,
                            name[7:])
                    else:
                        val = getattr(frame.header, name)
                    if val not in fields[name]:
                        fields[name][val] = 0
                    fields[name][val] += 1
                hash = hashlib.md5()
                hash.update(frame.imageData)
                hashes.add(hash.hexdigest())

        for name, vals in fields.items():
            print(name)
            for val, count in vals.items():
                print('  %08X %9d' % (val, count))
        print("Unique hashes:", len(hashes))

