from ctypes import (BigEndianStructure,
    c_byte   as s8,
    c_ubyte  as u8,
    c_int16  as s16,
    c_uint16 as u16,
    c_int32  as s32,
    c_uint32 as u32,
    c_float  as f32, # name "float" is already used
    c_double as f64)

class MapBlock(BigEndianStructure):
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
