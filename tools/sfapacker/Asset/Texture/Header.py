from ctypes import (
    c_byte   as s8,
    c_ubyte  as u8,
    c_int16  as s16,
    c_uint16 as u16,
    c_int32  as s32,
    c_uint32 as u32,
    c_float  as f32, # name "float" is already used
    c_double as f64)
from sfapacker.MyStruct import MyStruct
import xml.etree.ElementTree as ET
from .GX import GX

class Header(MyStruct):
    # ^ denotes fields that are always 0 in the files on disc
    _fields_ = [
        ('next',                 u32), # ^00 Texture*
        ('flags',                u32), # ^04
        ('xOffset',              s16), # ^08
        ('width',                u16), #  0A
        ('height',               u16), #  0C
        ('usage',                s16), #  0E ref count
        ('frameVal10',           s16), #  10 related to anim frame count
        ('unk12',                s16), # ^12 always 0, never accessed?
        ('framesPerTick',        u16), #  14 how many frames to advance each tick
        ('format',               u8),  #  16 GXTexFmt
        ('wrapS',                u8),  #  17 GXTexWrapMode
        ('wrapT',                u8),  #  18 GXTexWrapMode
        ('minFilter',            u8),  #  19 FilterMode
        ('magFilter',            u8),  #  1A FilterMode
        ('_padding1B',           u8),  # ^1B always 0, never accessed (odd place for padding; maybe unused field)
        ('minLod',               u8),  #  1C (bias hardcoded to -2)
        ('maxLod',               u8),  #  1D
        ('unk1E',                u8),  #  1E padding? never accessed, but some files have 0xFF
        ('_padding1F',           u8),  # ^1F padding
        ('texObj',               GX.TexObj), # ^20 all zero in file
        ('texRegion',            u32), # ^40 GXTexRegion*
        ('bufSize',              s32), # ^44 raw image data size
        ('bNoTexRegionCallback', s8),  # ^48 bool use gxSetTexImage0 instead of gxCallTexRegionCallback
        ('bDoNotFree',           s8),  # ^49 bool (maybe memory region?)
        ('unk4A',                s8),  # ^4A never accessed
        ('unk4B',                s8),  # ^4B set to 10 on free, otherwise never acccessed (memory region?)
        ('bufSize2',             u32), # ^4C same as bufSize (allocated size?)
        ('tevVal50',             u32), #  50 0:use 1 TEV stage, not 2 (maybe bHasTwoTevStages?)
        ('_padding54',           u32), # ^54 XXX proper padding fields
        ('_padding58',           u32), # ^58
        ('_padding5C',           u32), # ^5C
    ]
    _enums_ = {
        'format':    GX.ImageFormat,
        'wrapS':     GX.WrapMode,
        'wrapT':     GX.WrapMode,
        'minFilter': GX.FilterMode,
        'magFilter': GX.FilterMode,
    }
