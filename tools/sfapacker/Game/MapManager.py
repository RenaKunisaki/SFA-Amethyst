import os.path
import struct
import xml.etree.ElementTree as ET

class MapManager:
    """Manages packing/unpacking maps."""

    game = None
    """The Game instance."""

    trkblk:list[int] = []
    """Array of map dir ID => offset. This offset is added to
    a block's `sub` value to get its index into the `modXX.tab`
    file.
    """

    dirIds:list[int] = []
    """List of map ID => dir ID read from the game executable."""

    mapDirs:list[str] = []
    """List of map dir ID => dir name."""


    def __init__(self, game):
        self.game = game


    def readAllMapInfo(self) -> list[dict]:
        """Read info for all maps.

        :returns: List of map ID => map info.
        """
        self._readTables()
        globalMap = self._readGlobalMap() # dict
        mapsBin   = self._readMapsBin()   # list
        mapInfo   = self._readMapInfo()   # list
        maps      = []
        for i, info in enumerate(mapInfo):
            mp = {'id': i}
            if i < len(self.dirIds):
                dirId = self.dirIds[i]
                dirName = self.mapDirs[dirId]
                mp['dir'] = dirName

            for k, v in info.items(): mp[k] = v
            if i in globalMap:
                for k, v in globalMap[i].items(): mp[k] = v
            if i < len(mapsBin):
                for k, v in mapsBin[i].items(): mp[k] = v

            maps.append(mp)
        return maps


    def mapInfoToXml(self, map) -> ET.Element:
        """Build XML element for given map."""
        fields = {
            'dir':           '%s',
            'name':          '%s',
            'type':          '%d',
            'playerObj':     '0x%04X',
            'x':             '%d',
            'z':             '%d',
            'layer':         '%d',
            'sizeX':         '%d',
            'sizeZ':         '%d',
            'originX':       '%d',
            'originZ':       '%d',
            'nBlocks':       '%d',
            'mapinfo_unk1D': '%d',
            'unk1E':         '%d',
            'unk08':         '0x%08X',
            'unk0C_0':       '0x%08X',
            'unk0C_1':       '0x%08X',
            'unk0C_2':       '0x%08X',
            'unk0C_3':       '0x%08X',
        }
        attrs = {'id':'0x%02X' % map['id']}
        for name, fmt in fields.items():
            v = map.get(name, None)
            if v is not None: attrs[name] = fmt % v
        link = map.get('link', None)
        if link is not None:
            attrs['link0'] = str(link[0])
            attrs['link1'] = str(link[1])

        eMap = ET.Element('map', attrs)
        for i, block in enumerate(map.get('blocks', [])):
            if block is None: continue
            eMap.append(ET.Element('block', {
                'n': str(i),
                'mod': str(block['mod']),
                'sub': str(block['sub']),
                'unk1': '%d' % block['unk1'],
                'unk2': '%d' % block['unk2'],
            }))
        return eMap


    def _readTables(self, force=False):
        self._readTrkBlk(force)
        self._readDirIds(force)
        self._readDirNames(force)


    def _readTrkBlk(self, force=False):
        """Read TRKBLK.tab."""
        if len(self.trkblk) > 0 and not force: return
        self.trkblk = []
        path = os.path.join(self.game.rootDir, 'TRKBLK.tab')
        with open(path, 'rb') as file:
            while True:
                data = file.read(2)
                if len(data) < 2: break
                self.trkblk.append(struct.unpack('>h', data)[0]) # grumble


    def _readDirIds(self, force=False):
        """Read map directory ID table from game executable."""
        if len(self.dirIds) > 0 and not force: return
        self.dirIds = []
        dol = self.game.dol
        tbl = self.game.addrs['mapIdXltnTbl']
        self.dirIds = []
        dol.file.seek(dol.addrToOffset(tbl['addr']))
        for _ in range(tbl['count']):
            idx = struct.unpack('>i', dol.file.read(4))[0] # grumble
            if idx < 0: break
            self.dirIds.append(idx)


    def _readDirNames(self, force=False):
        """Read map directory names from game executable."""
        if len(self.mapDirs) > 0 and not force: return
        self.mapDirs = []
        dol = self.game.dol

        # asset dir names
        # this table contains several duplicate entries, which is why we need
        # to track both the dir name and the dir ID (which is just the index
        # into this table).
        aNames = self.game.addrs['mapDirNames']
        base   = aNames['addr']
        self.mapDirs = []
        for i in range(aNames['count']):
            dol.file.seek(dol.addrToOffset(base+(i*4)))
            ptr = struct.unpack('>I', dol.file.read(4))[0] # grumble

            dol.file.seek(dol.addrToOffset(ptr))
            data = dol.file.read(256)
            end  = data.find(b'\0')
            data = data[0:end]
            self.mapDirs.append(data.decode('UTF-8'))


    def _readGlobalMap(self, name:str="globalma.bin") \
    -> dict[int,dict]:
        """Read all entries from globalmap file.

        :param name: File name (in game's root dir) to read.
        :returns: Dict of map ID => map info.
        """
        maps = {}
        path = os.path.join(self.game.rootDir, name)
        with open(path, 'rb') as file:
            while True:
                x, z, layer, mapId, link1, link2 = struct.unpack(
                    '>hhhhhh', file.read(12))
                if mapId < 0: break
                maps[mapId] = {
                    'id': mapId,
                    'x': x,
                    'z': z,
                    'layer': layer,
                    'link': [link1, link2]
                }
        return maps


    def _readMapsBin(self) -> list[dict]:
        """Read all info from MAPS.bin and MAPS.tab in the game's
        root directory.

        :returns: list of map ID => info.
        """
        maps = []
        pTab = os.path.join(self.game.rootDir, 'MAPS.tab')
        pBin = os.path.join(self.game.rootDir, 'MAPS.bin')
        fTab = open(pTab, 'rb')
        fBin = open(pBin, 'rb')

        while True:
            data = fTab.read(7*4)
            if len(data) < 7*4: break
            offsets = struct.unpack('>7I', data)
            info = self._readMapsBinInfo(fBin, offsets[0])
            blocks = self._readMapsBinBlockList(fBin, offsets[1],
                info['sizeX'] * info['sizeZ'])
            info['blocks'] = blocks
            maps.append(info)

        fBin.close()
        fTab.close()
        return maps


    def _readMapsBinInfo(self, file, offset:int) -> dict[str,int]:
        """Read a MapInfo entry from MAPS.bin.

        :param file: File to read from.
        :param offset: File offset to read from.
        :returns: Dict of map info.

        This reads the structure referenced by the first of the
        seven offsets in a MAPS.tab entry. Not to be confused
        with MAPINFO.bin.
        """
        file.seek(offset)
        data = struct.unpack('>hhhhIIIIIhH', file.read(0x20))
        return {
            'sizeX':   data[ 0],
            'sizeZ':   data[ 1],
            'originX': data[ 2],
            'originZ': data[ 3],
            'unk08':   data[ 4],
            'unk0C_0': data[ 5],
            'unk0C_1': data[ 6],
            'unk0C_2': data[ 7],
            'unk0C_3': data[ 8],
            'nBlocks': data[ 9],
            'unk1E':   data[10],
        }


    def _readMapsBinBlockList(self, file, offset:int, count:int) \
    -> list[dict]:
        """Read block list from MAPS.bin.

        :param file: File to read from.
        :param offset: File offset to read from.
        :param count: Number of blocks to read.
        :returns: List of block info.
        """
        file.seek(offset)
        blocks = []
        for i in range(count):
            data = file.read(4)
            if len(data) < 4: break
            val = struct.unpack('>I', data)[0] # grumble
            unk1 =  val >> 31
            mod  = (val >> 23) & 0x00FF
            sub  = (val >> 17) & 0x003F
            unk2 =  val        & 0x01FF
            if mod == 0xFF: blocks.append(None)
            else:
                # game does this for some reason
                if mod >= 5: mod += 1
                blocks.append({'idx': i,
                    'mod':  mod,  'sub':  sub,
                    'unk1': unk1, 'unk2': unk2,
                })
        return blocks


    def _readMapInfo(self) -> list[dict]:
        """Read info from MAPINFO.bin.

        :returns: List of map info.
        """
        path = os.path.join(self.game.rootDir, 'MAPINFO.bin')
        maps = []
        with open(path, 'rb') as file:
            while True:
                data = file.read(0x20)
                if len(data) < 0x20: break
                name, mType, unk, obj = struct.unpack('>28sBBH', data)
                maps.append({
                    'name': name.replace(b'\0', b'').decode('UTF-8'),
                    'type': mType,
                    'mapinfo_unk1D': unk, # always 6
                    'playerObj': obj,
                })
        return maps

