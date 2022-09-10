import logging; log = logging.getLogger(__name__)
import bmesh
import bpy
import bpy_extras
import os
import os.path
import tempfile
import shutil
import struct
import math
from ctypes import sizeof
from ..BinaryFile import BinaryFile
from ..Model.MapBlock import MapBlock
from ..Model.Common import DisplayListPtr, PolygonGroup, \
    GCPolygon, Shader
from ..GX.GX import GX
from ..Model.Parser.Parser import Parser


class Importer:
    def __init__(self, operator, context):
        self.operator = operator
        self.context  = context
        self.gx       = GX()


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
        header = MapBlock.from_buffer_copy(file.read(sizeof(MapBlock)))
        name = bytes(header.name).decode('utf-8')

        data = {
            'isMap': True,
            'header': header,
            'file': file,
            'path': path,
            'name': name,
            #'object': bpy.data.objects.new(name, None),
            'vertexPositions': file.read(header.nVtxs*6, header.vertexPositions),
            'vertexColors': file.read(header.nColors*2, header.vertexColors),
            'vertexTexCoords': file.read(header.nTexCoords*4, header.vertexTexCoords),
            'renderInstrsMain': file.readu8(header.nRenderInstrsMain, header.renderInstrsMain),
            'renderInstrsReflective': file.readu8(header.nRenderInstrsReflective, header.renderInstrsReflective),
            'renderInstrsWater': file.readu8(header.nRenderInstrsWater, header.renderInstrsWater),
            'textureIds': file.reads32(header.nTextures, header.textures),
            'displayLists': [DisplayListPtr, header.displayLists, header.nDlists],
            'GCpolygons': [GCPolygon, header.GCpolygons, header.nPolygons],
            'polygonGroups': [PolygonGroup, header.polygonGroups, header.nPolyGroups],
            'shaders': [Shader, header.shaders, header.nShaders],
        }
        self._readObjs(data, file)
        self._readModel(data, file)
        return {'FINISHED'}


    def importCharModel(self, path:str, file:BinaryFile):
        """Import a character model from a file.

        :param path: The path of the file we're reading.
        :param file: The file to read from.
        """
        raise NotImplementedError
        return {'FINISHED'}


    def _readObjs(self, data, file):
        # convert [type, offset, count] to list of objects.
        # type must inheret ctypes.Structure.
        for name, val in data.items():
            if type(val) is not list: continue
            oType, offset, count = val
            items = []
            file.seek(offset)
            for _ in range(count):
                items.append(oType.from_buffer_copy(
                    file.read(sizeof(oType))))
            data[name] = items

    def _readModel(self, data, file):
        parser = Parser(self.gx)
        result = parser.parse(data)
