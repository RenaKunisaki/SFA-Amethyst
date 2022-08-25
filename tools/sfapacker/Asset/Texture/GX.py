from enum import Enum, IntEnum
from sfapacker.MyStruct import MyStruct
from ctypes import (
    c_byte   as s8,
    c_ubyte  as u8,
    c_int16  as s16,
    c_uint16 as u16,
    c_int32  as s32,
    c_uint32 as u32,
    c_float  as f32, # name "float" is already used
    c_double as f64)

# has to be defined outside of GX class because other
# GX struct classes refer to it
class ImageFormat(IntEnum): # aka GXTexFmt
    """GX image formats."""
    I4     = 0x00
    I8     = 0x01
    IA4    = 0x02
    IA8    = 0x03
    RGB565 = 0x04
    RGB5A3 = 0x05
    RGBA8  = 0x06 # aka RGBA32
    C4     = 0x08
    C8     = 0x09
    C14X2  = 0x0A
    CMPR   = 0x0E # aka BC1

    # following are defined by GX but not used for image files
    ZTF    = 0x10 # Z-texture-format
    CTF    = 0x20 # copy-texture-format only

    R4     = 0x00 | CTF # For copying 4 bits from red.
    RA4    = 0x02 | CTF # For copying 4 bits from red, 4 bits from alpha.
    RA8    = 0x03 | CTF # For copying 8 bits from red, 8 bits from alpha.
    YUVA8  = 0x06 | CTF
    A8     = 0x07 | CTF # For copying 8 bits from alpha.
    R8     = 0x08 | CTF # For copying 8 bits from red.
    G8     = 0x09 | CTF # For copying 8 bits from green.
    B8     = 0x0A | CTF # For copying 8 bits from blue.
    RG8    = 0x0B | CTF # For copying 8 bits from red, 8 bits from green.
    GB8    = 0x0C | CTF # For copying 8 bits from green, 8 bits from blue.

    Z8     = 0x01 | ZTF # For texture copy, specifies upper 8 bits of Z.
    Z16    = 0x03 | ZTF # For texture copy, specifies upper 16 bits of Z.
    Z24X8  = 0x06 | ZTF # For texture copy, copies 24 Z bits and 0xff.

    Z4     = 0x00 | ZTF | CTF # For copying 4 upper bits from Z.
    Z8M    = 0x09 | ZTF | CTF # For copying the middle 8 bits of Z.
    Z8L    = 0x0A | ZTF | CTF # For copying the lower 8 bits of Z.
    Z16L   = 0x0C | ZTF | CTF # For copying the lower 16 bits of Z.

class GX:
    """Utility class for some GX things."""

    ImageFormat = ImageFormat

    class FilterMode(IntEnum):
        """Texture filter modes."""
        NEAR          = 0x00
        LINEAR        = 0x01
        NEAR_MIP_NEAR = 0x02
        LIN_MIP_NEAR  = 0x03
        NEAR_MIP_LIN  = 0x04
        LIN_MIP_LIN   = 0x05
        # XXX where are these ones used?
        #NEAR              = 0x00
        #NEAR_MIP_NEAR     = 0x01
        #NEAR_MIP_LINEAR   = 0x02
        ## 0x03 is unused/invalid
        #LINEAR            = 0x04
        #LINEAR_MIP_NEAR   = 0x05
        #LINEAR_MIP_LINEAR = 0x06
        ## 0x07 is unused/invalid

    class OldFilterMode(IntEnum):
        """Only used by some prototype hardware.
        Probably not used by any game except posibly
        some very old prototypes?"""
        NEAR              = 0x00
        LINEAR            = 0x01
        NEAR_MIP_NEAR     = 0x02
        LINEAR_MIP_NEAR   = 0x03
        NEAR_MIP_LINEAR   = 0x04
        LINEAR_MIP_LINEAR = 0x05

    class WrapMode(IntEnum):
        """Texture wrap modes."""
        CLAMP  = 0x00
        REPEAT = 0x01
        MIRROR = 0x02

    class PaletteFormat(Enum):
        IA8    = 0
        RGB565 = 1
        RGB5A3 = 2

    class TexObj(MyStruct):
        _fields_ = [
            ('mode0',    u32), # 00
            ('mode1',    u32), # 04
            ('image0',   u32), # 08
            ('image3',   u32), # 0C
            ('userData', u32), # 10 void*
            ('format',   u32), # 14 GXTexFmt
            ('tlutName', u32), # 18
            ('loadCnt',  u16), # 1C
            ('loadFmt',  u8),  # 1E (0=CMPR 1=4bpp 2=8bpp 3=32bpp)
            ('flags',    u8),  # 1F (1:mipmap; 2:isRGB)
        ]
        _enums_ = {
            'format': ImageFormat,
        }

    @staticmethod
    def GXGetTexBufferSize(width:int, height:int, format:int,
    useMipMaps:bool, maxLod:int) -> int:
        """Implement GXGetTexBufferSize()."""
        bitsW, bitsH = 0, 0

        F = GX.ImageFormat
        if format in (F.I4, F.C4, F.CMPR, F.R4, F.Z4):
            bitsW = 3
            bitsH = 3
        elif format in (F.I8, F.IA4, F.C8, F.Z8, F.RA4,
        F.A8, F.R8, F.G8, F.B8, F.Z8M, F.Z8L):
            bitsW = 3
            bitsH = 2
        elif format in (F.IA8, F.RGB565, F.RGB5A3, F.RGBA8,
        F.C14X2, F.Z16, F.Z24X8, F.RA8, F.RG8, F.GB8, F.Z16L):
            bitsW = 2
            bitsH = 2

        if format in (F.RGBA8, F.Z24X8): iVar2 = 0x40
        else: iVar2 = 0x20

        if (useMipMaps):
            result = 0
            uVar1 = maxLod & 0xff
            while uVar1 != 0:
                w = width & 0xffff
                h = height & 0xffff
                result += iVar2 * (w + (1 << bitsW) + -1 >> bitsW) * (h + (1 << bitsH) + -1 >> bitsH)
                if w == 1 and h == 1: return result
                if (width & 0xffff) < 2: width = 1
                else: width = w >> 1
                if (height & 0xffff) < 2: height = 1
                else: height = h >> 1
                uVar1 -= 1
        else:
            result = (iVar2 * ((width & 0xffff) + (1 << bitsW) + -1 >> bitsW) *
                ((height & 0xffff) + (1 << bitsH) + -1 >> bitsH))
        return result
