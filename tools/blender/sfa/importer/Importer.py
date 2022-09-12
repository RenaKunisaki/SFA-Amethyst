import logging; log = logging.getLogger(__name__)
import bmesh
import bpy
import bpy_extras
import os
import os.path
from pathlib import Path
import xml.etree.ElementTree as ET
from ..BinaryFile import BinaryFile
from ..Model.MapBlock import MapBlock
from ..GX.GX import GX
from ..Model.Parser.Parser import Parser

class Importer:
    """Imports models from SFA."""

    maps:dict[str,dict] = {}
    """Info from maps.xml, indexed by map dir name."""


    def __init__(self, operator, context):
        self.operator = operator
        self.context  = context
        self.gx       = GX()
        self.maps     = {}


    @staticmethod
    def _add_object_to_group(ob, group_name):
        # Get or create the required group.
        group = bpy.data.groups.get(group_name,
            bpy.data.groups.new(group_name))

        # Link the provided object to it.
        if ob.name not in group.objects:
            group.objects.link(ob)
        return group


    def run(self, path:str):
        """Perform the import."""
        self.wm   = bpy.context.window_manager
        self.path = path
        return self.importFile(path)

    def _readMapsXml(self, path:str, force=False):
        if len(self.maps) > 0 and not force: return
        xmlDir = os.path.join(path, '..', '..', 'maps.xml')
        try: file = open(xmlDir, 'rt')
        except FileNotFoundError: return
        xml = ET.parse(file)
        file.close()

        for eMap in xml.getroot().findall('map'):
            mp = {'blocks':{}}
            for k, v in eMap.attrib.items():
                if k not in ('dir', 'name'):
                    try: v = int(v, 0)
                    except ValueError: pass
                mp[k] = v
            # many unsued maps point to animtest dir. don't
            # reference them when trying to load the
            # actual animtest map.
            if 'dir' in mp and (
            mp['dir'] != 'animtest' or mp.get('id',0) == 0x1A):
                self.maps[mp['dir']] = mp
            for eBlock in eMap.findall('block'):
                mod = int(eBlock.get('mod'), 0)
                sub = int(eBlock.get('sub'), 0)
                mp['blocks']['%d:%d' % (mod,sub)] = {
                    'mod':  mod,
                    'sub':  sub,
                    'idx':  int(eBlock.get('n'   ), 0),
                    'unk1': int(eBlock.get('unk1'), 0),
                    'unk2': int(eBlock.get('unk2'), 0),
                }


    def importFile(self, path:str):
        """Try to import the given file.

        :param path: Path to the file to import.
        """
        file = BinaryFile(path)
        self.file = file

        # which type of file is this?
        dirName, fileName = os.path.split(path)
        if fileName.startswith('mod'):
            return self.importMapBlock(path, file)
        else:
            return self.importCharModel(path, file)


    def importMapBlock(self, path:str, file:BinaryFile):
        """Import a map block from a file.

        :param path: The path of the file we're reading.
        :param file: The file to read from.
        """
        dirs, name = os.path.split(path)
        self._readMapsXml(dirs)

        # back up to see which directory this is in.
        # should be "root/someMap/mod/modXX.XX.bin"
        dirs = Path(dirs).parts
        mapName = dirs[-2]

        self.gx.setTexturePath(os.path.join(*dirs[0:-1]))
        block = MapBlock(self.gx).readFromFile(file, path)

        if mapName in self.maps:
            mp   = self.maps[mapName]
            name = name.split('.') # ['modXX', 'XX', 'bin']
            mod  = int(name[0][3:])
            sub  = int(name[1])
            sx   = mp['sizeX']
            bk   = mp['blocks'].get('%d:%d' % (mod,sub), None)
            if bk is None:
                log.warn("Block %d.%d not found on map grid for %s",
                    mod, sub, mapName)
                idx = 0
            else:
                idx = bk['idx']
                block.xOffset = int(idx % sx)
                block.zOffset = int(idx / sx)
        else:
            log.warn("Unrecognized map dir %r; can't determine block offsets",
                mapName)

        parser = Parser(self.gx)
        parser.parse(block)
        return {'FINISHED'}


    def importCharModel(self, path:str, file:BinaryFile):
        """Import a character model from a file.

        :param path: The path of the file we're reading.
        :param file: The file to read from.
        """
        raise NotImplementedError
        return {'FINISHED'}
