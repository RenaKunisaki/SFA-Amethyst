# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from collections import OrderedDict
from ctypes import (BigEndianStructure, sizeof,
    c_byte   as s8,
    c_ubyte  as u8,
    c_int16  as s16,
    c_uint16 as u16,
    c_int32  as s32,
    c_uint32 as u32,
    c_float  as f32, # name "float" is already used
    c_double as f64)
from ..Model.Common import DisplayListPtr, PolygonGroup, \
    GCPolygon, Shader
from ..GX.GX import GX
from .Model import Model

class MapBlockHeader(BigEndianStructure):
    """The header of a map block file on disc/in RAM."""
    _fields_ = [
        ('unused00',                u32), # set from 80060b90 - XXX confirm unused
        ('flags04',                 u16),
        ('unk06',                   u16),
        ('length',                  s32), # file size
        ('mtx',                     f32*12),
        ('unk3C',                   u32*4), # maybe mtx is 4x4? if it's even a matrix
        ('GCpolygons',              u32), # -> GCPolygon
        ('polygonGroups',           u32), # -> PolygonGroup
        ('textures',                u32), # -> s32[] texture IDs
        ('vertexPositions',         u32), # -> vec3s
        ('vertexColors',            u32), # -> u16 (RGBA4444)
        ('vertexTexCoords',         u32), # -> vec2s
        ('shaders',                 u32), # -> Shader
        ('displayLists',            u32), # -> DisplayListPtr
        ('linehits',                u32), # -> LineHit (XXX used?)
        ('hits',                    u32), # -> HitsBinEntry (0 in file)
        ('unkHits',                 u32), # set to 0 in initHits
        ('renderInstrsMain',        u32), # -> BitStream
        ('renderInstrsReflective',  u32), # -> BitStream
        ('renderInstrsWater',       u32), # -> BitStream
        ('nRenderInstrsMain',       u16), # length in bytes
        ('nRenderInstrsReflective', u16), # length in bytes
        ('nRenderInstrsWater',      u16), # length in bytes
        ('yMin',                    s16),
        ('yMax',                    s16),
        ('yOffset',                 s16),
        ('nVtxs',                   u16), # number of vec3s in vertexPositions
        ('nUnk',                    u16),
        ('nColors',                 u16),
        ('nTexCoords',              u16),
        ('nPolygons',               u16),
        ('nPolyGroups',             u16),
        ('nHits',                   u16),
        ('unk9E',                   u16), # set to 0 in initHits
        ('nTextures',               u8),
        ('nDlists',                 u8),
        ('nShaders',                u8),
        ('unkA3',                   u8), # padding?
        ('name',                    s8*20), # size guessed
    ]

class MapBlock(Model):
    """One block from a map."""

    RenderStreamOrder:OrderedDict[str,str] = OrderedDict([
        ('main',       '.main'),
        ('reflective', '.reflective'),
        ('water',      '.water'),
    ])
    """List of stream name => mesh name suffix, in the order they
    should be parsed.
    """

    def __init__(self, gx:GX) -> None:
        super().__init__(gx)


    def readFromFile(self, file, path:str) -> MapBlock:
        header = MapBlockHeader.from_buffer_copy(
            file.read(sizeof(MapBlockHeader)))
        self.name = bytes(header.name).replace(b'\0', b'') \
            .decode('utf-8')

        self.header = header
        self.file = file
        self.filePath = path
        # these need to be read from maps.xml
        self.xOffset  = 0
        self.zOffset  = 0
        self._readData()

        return self

    def _readData(self):
        file   = self.file
        header = self.header
        self.vertexPositions = file.read(header.nVtxs*6, header.vertexPositions)
        self.vertexColors = file.read(header.nColors*2, header.vertexColors)
        self.vertexTexCoords = file.read(header.nTexCoords*4, header.vertexTexCoords)
        self.textureIds = file.reads32(header.nTextures, header.textures)
        self.displayLists = self._readObjects(DisplayListPtr, file,
            header.displayLists, header.nDlists)
        self.GCpolygons = self._readObjects(GCPolygon, file,
            header.GCpolygons, header.nPolygons)
        self.polygonGroups = self._readObjects(PolygonGroup, file,
            header.polygonGroups, header.nPolyGroups)
        self.shaders = self._readObjects(Shader, file,
            header.shaders, header.nShaders)

        self.renderStreams = {
            'main': file.readu8(header.nRenderInstrsMain, header.renderInstrsMain),
            'reflective': file.readu8(header.nRenderInstrsReflective, header.renderInstrsReflective),
            'water': file.readu8(header.nRenderInstrsWater, header.renderInstrsWater),
        }

        # ensure a list even if only one item
        if type(self.textureIds) is not list:
            self.textureIds = [self.textureIds]
