from ctypes import (BigEndianStructure,
    c_byte   as s8,
    c_ubyte  as u8,
    c_int16  as s16,
    c_uint16 as u16,
    c_int32  as s32,
    c_uint32 as u32,
    c_float  as f32, # name "float" is already used
    c_double as f64)

class vec2s(BigEndianStructure):
    _fields_ = [('x',s16), ('y',s16)]
class vec3s(BigEndianStructure):
    _fields_ = [('x',s16), ('y',s16), ('z',s16)]
class vec3f(BigEndianStructure):
    _fields_ = [('x',f32), ('y',f32), ('z',f32)]
class Mtx43(BigEndianStructure):
    _fields_ = [('m',f32*12)]

class GCPolygon(BigEndianStructure):
    """Polygon used by collision detection."""
    _fields_ = [
        ('vtxs',      u16*3), # Indices into block.vtxPositions
        ('subBlocks', u16), # High byte is Z axis; low byte is X.
            # Split the block into 8 strips; each bit tells whether
            # the polygon overlaps that strip.
    ]

class PolygonGroup(BigEndianStructure):
    _fields_ = [
        ('firstPolygon', u16), # Ends at next group's first polygon
        ('x1', s16),
        ('x2', s16),
        ('y1', s16),
        ('y2', s16),
        ('z1', s16),
        ('z2', s16),
        ('unk0E', u8), # probably padding because the game reads
        ('unk0F', u8), # the following fields as u32
        ('unk10', u8),
        ('type',  u8), # surface type
        ('flags', u16),
    ]

class DisplayListPtr(BigEndianStructure):
    _fields_ = [
        ('list', u32), # points to GX display list commands
        ('size', u16),
        ('bbox', vec3s*2),
        ('unk1E', u8),
        ('shaderId', u8), # XXX where is this used?
        ('specialBitAddr', u16), # offset relating to shaders
        ('unk22', u16), # offset of some sort
        ('unk24', u32), # always 0x07000000 (N64 leftover?)
    ]

class ShaderLayer(BigEndianStructure):
    _fields_ = [
        # texture is s32 because the game converts it to a pointer on load
        ('texture', s32), # idx into model's texture list (-1=none)
        ('tevMode', u8),
        ('enableTexChainStuff', u8),
        ('scrollingTexMtx', u8),
        ('unk07', u8), # probably padding
    ]


class Shader(BigEndianStructure):
    _fields_ = [
        ('unk00', u32),
        ('r', u8), # likely wrong
        ('g', u8),
        ('b', u8),
        ('unk07', u8),
        ('auxTex0', s32),
        ('alpha', u8),
        ('unk0D', u8),
        ('unk0E', u8),
        ('unk0F', u8),
        ('unk10', u32),
        ('auxTex1', s32),
        ('texture18', s32),
        ('unk1C', s32), # -1 -> 0, -2 -> 0, else -> 1
        ('unk20', u32), # pointer
        ('layer', ShaderLayer*2),
        ('auxTex2', s32),
        ('furTexture', s32),
        ('flags', u32), # ShaderFlags
        ('attrFlags', u8), # ShaderAttrFlags
        ('nLayers', s8),
        ('_pad42', u16),
    ]
