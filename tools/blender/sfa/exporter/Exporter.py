import logging; log = logging.getLogger(__name__)
import bmesh
import bpy
import bpy_extras
import os
import os.path
import struct
from ctypes import c_byte
from pathlib import Path
import xml.etree.ElementTree as ET
from ..BinaryFile import BinaryFile
from ..Model.MapBlock import MapBlock, MapBlockHeader
from ..GX.GX import GX
from ..Model.Parser.Parser import Parser
from .BitStreamWriter import BitStreamWriter

class Exporter:
    """Exports models to SFA formats."""

    # XXX needs to be same as importer
    SCALE = 1/10

    def __init__(self, operator, context):
        self.operator = operator
        self.context  = context
        self.gx       = GX()


    def exportBlock(self, name:str, path:str):
        """Export one map block.

        :param name: The block's name.
        :param path: The path to write to.
        """
        self.isMap = True
        self.wm = bpy.context.window_manager
        self.buffers = {
            'POS': [],
            'COL': [],
            'TEX': [],
        }
        self.yMin =  999999999
        self.yMax = -999999999
        self.dlists = []
        self.streams = {}
        col = bpy.data.collections[name]
        for stream in ('main', 'reflective', 'water'):
            try:
                obj = col.objects[name+'.'+stream]
            except KeyError:
                self.streams[stream] = b''
                continue
            self.streams[stream] = self._buildStream(obj)

        self._writeBlock(name, path)
        return {'FINISHED'}


    def _writeBlock(self, name:str, path:str):
        """Write block to file.

        :param name: Block name.
        :param path: Path to write to.
        """
        nameBytes = name.encode('utf-8')
        nameBytes += b'\0' * (20 - len(nameBytes))
        nameBytes = (c_byte * 20).from_buffer_copy(nameBytes)
        header = MapBlockHeader(
            nRenderInstrsMain = len(self.streams['main']),
            nRenderInstrsReflective = len(self.streams['reflective']),
            nRenderInstrsWater = len(self.streams['water']),
            nVtxs = len(self.buffers['POS']) // 3,
            nColors = len(self.buffers['COL']),
            nTexCoords = len(self.buffers['TEX']) // 2,
            nDlists = len(self.dlists),
            name = nameBytes,
            yMin = int(self.yMin), yMax = int(self.yMax),
            yOffset = 0, # XXX
        )
        with open(path, 'wb') as file:
            file.write(bytes(header))

            header.renderInstrsMain = file.tell()
            file.write(self.streams['main'])
            header.renderInstrsReflectve = file.tell()
            file.write(self.streams['reflective'])
            header.renderInstrsWater = file.tell()
            file.write(self.streams['water'])

            header.displayLists = file.tell()
            for dlist in self.dlists:
                file.write(dlist)

            # XXX texture ID list, shaders...

            header.vertexPositions = file.tell()
            for v in self.buffers['POS']:
                file.write(struct.pack('>h', int(v)))

            header.vertexColors = file.tell()
            for v in self.buffers['COL']: # XXX encode
                file.write(struct.pack('>H', int(v)))

            header.vertexTexCoords = file.tell()
            for v in self.buffers['TEX']:
                file.write(struct.pack('>h', int(v)))

            # go back and overwrite header with updated info
            file.seek(0)
            file.write(bytes(header))


    def _buildStream(self, obj) -> bytes:
        """Build the data for one render stream.

        :param obj: The Blender object for this stream.
        :returns: The render stream data.
        """
        mesh     = obj.data
        scale    = self.SCALE * 8 # game scales by 8
        iPos     = len(self.buffers['POS'])
        iCol     = len(self.buffers['COL'])
        iTex     = len(self.buffers['TEX'])
        curMat   = None
        curBatch = []
        self.curStream = BitStreamWriter()

        # XXX this depends on params of current shader
        self.curStream.addBits(4, 3) # SetVtxFmt cmd
        self.curStream.addBits(3, 7) # POS:I16, COL0:I16, TEX0:I16

        # of course the API for reading these is totally
        # different from the API for writing them because lol
        for vtx in mesh.vertices:
            x = vtx.co[0] * scale
            y = vtx.co[2] * scale # swap Y/Z
            z = vtx.co[1] * scale
            self.buffers['POS'].append(x)
            self.buffers['POS'].append(y)
            self.buffers['POS'].append(z)
            self.yMin = min(self.yMin, y)
            self.yMax = max(self.yMax, y)
        for face in mesh.polygons:
            if len(face.vertices) > 4:
                raise RuntimeError(
                    "Face with more than 4 vertices in "+
                    obj.name)
            poly = []

            if face.material_index != curMat:
                if curMat is not None:
                    if len(curBatch) > 0:
                        self._encodeBatch(curBatch)
                        curBatch = []
                    curMat = face.material_index
                    curBatch.append(('shader', curMat))

            curBatch.append(poly)
            # reverse for game's CW winding order
            for vIdx in reversed(face.vertices):
                vtx = mesh.vertices[vIdx]
                poly.append({
                    'POS':iPos+vIdx,
                    'COL':iCol+vIdx,
                    'TEX':iTex+vIdx})

        if len(curBatch) > 0:
            self._encodeBatch(curBatch)
        self.curStream.addBits(4, 5) # End command
        data = self.curStream.finish()
        pad  = len(data) % 4
        if pad: data += b'\0' * pad
        return data


    def _encodeBatch(self, batch:list):
        """Encode a polygon batch to display list/render stream.

        :param batch: The batch to encode.
        """
        for op in batch:
            if op[0] == 'shader':
                self._makeShaderCmd(op[1])
            else:
                self.curStream.addBits(4, 2) # CallDlist cmd
                self.curStream.addBits(8, len(self.dlists))
                self._makeDisplayList(op)


    def _makeShaderCmd(self, shaderIdx:int):
        """Make stream commands to change shader.

        :param shaderIdx: Shader index.
        """
        self.curStream.addBits(4, 1) # SetShader cmd
        self.curStream.addBits(6, shaderIdx)
        # XXX this depends on params of current shader
        self.curStream.addBits(4, 3) # SetVtxFmt cmd
        self.curStream.addBits(3, 7) # POS:I16, COL0:I16, TEX0:I16


    def _makeDisplayList(self, op:list[dict]):
        """Make display list for given polygon batch.

        :param op: Polygon batch, which is a list of dicts of
            the polygon's attribute indices.

        Adds the display list data to self.dlists.
        """
        # 0x80=QUADS, 0x90=TRIS
        drawOp  = 0x80 if len(op) > 3 else 0x90
        drawOp |= (5 if self.isMap else 6) # set VAT
        dlist   = struct.pack('>BH', drawOp, len(op))
        for poly in op:
            dlist += struct.pack('>BHHH',
                0, # PNMTXIDX
                poly['POS'],
                poly['COL'],
                poly['TEX'],
            )
        pad = len(dlist) % 16 # XXX verify padding
        if pad > 0: dlist += b'\0' * (16-pad)
        self.dlists.append(dlist)


