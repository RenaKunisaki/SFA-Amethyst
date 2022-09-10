from enum import IntEnum

_GX_TF_CTF = 0x20 # copy-texture-format only
_GX_TF_ZTF = 0x10 # Z-texture-format

class GXConstants:
    """Mixin class to define a bunch of constants from
    the GC SDK."""

    VAT_FIELD_ORDER = (
        'PNMTXIDX', 'T0MIDX', 'T1MIDX', 'T2MIDX', 'T3MIDX', 'T4MIDX',
        'T5MIDX', 'T6MIDX', 'T7MIDX', 'POS', 'NRM', 'COL0', 'COL1',
        'TEX0', 'TEX1', 'TEX2', 'TEX3', 'TEX4', 'TEX5', 'TEX6',
        'TEX7')

    class Attr(IntEnum):
        PNMTXIDX      = 0x00 # position/normal matrix index
        TEX0MTXIDX    = 0x01 # texture 0 matrix index
        TEX1MTXIDX    = 0x02 # texture 1 matrix index
        TEX2MTXIDX    = 0x03 # texture 2 matrix index
        TEX3MTXIDX    = 0x04 # texture 3 matrix index
        TEX4MTXIDX    = 0x05 # texture 4 matrix index
        TEX5MTXIDX    = 0x06 # texture 5 matrix index
        TEX6MTXIDX    = 0x07 # texture 6 matrix index
        TEX7MTXIDX    = 0x08 # texture 7 matrix index
        POS           = 0x09 # position
        NRM           = 0x0A # normal
        CLR0          = 0x0B # color 0
        CLR1          = 0x0C # color 1
        TEX0          = 0x0D # input texture coordinate 0
        TEX1          = 0x0E # input texture coordinate 1
        TEX2          = 0x0F # input texture coordinate 2
        TEX3          = 0x10 # input texture coordinate 3
        TEX4          = 0x11 # input texture coordinate 4
        TEX5          = 0x12 # input texture coordinate 5
        TEX6          = 0x13 # input texture coordinate 6
        TEX7          = 0x14 # input texture coordinate 7
        POS_MTX_ARRAY = 0x15 # position matrix array pointer
        NRM_MTX_ARRAY = 0x16 # normal matrix array pointer
        TEX_MTX_ARRAY = 0x17 # texture matrix array pointer
        LIGHT_ARRAY   = 0x18 # light parameter array pointer
        NBT           = 0x19 # normal, bi-normal, tangent
        MAX_ATTR      = 0x1A # maximum number of vertex attributes
        NULL          = 0xFF # NULL attribute (to mark end of lists)

    class AttrType(IntEnum):
        NONE    = 0
        DIRECT  = 1
        INDEX8  = 2
        INDEX16 = 3

    class TexGenType(IntEnum):
        TG_MTX3x4 = 0x00
        TG_MTX2x4 = 0x01
        TG_BUMP0  = 0x02
        TG_BUMP1  = 0x03
        TG_BUMP2  = 0x04
        TG_BUMP3  = 0x05
        TG_BUMP4  = 0x06
        TG_BUMP5  = 0x07
        TG_BUMP6  = 0x08
        TG_BUMP7  = 0x09
        TG_SRTG   = 0x0A

    class TexGenSrc(IntEnum):
        TG_POS       = 0x00
        TG_NRM       = 0x01
        TG_BINRM     = 0x02
        TG_TANGENT   = 0x03
        TG_TEX0      = 0x04
        TG_TEX1      = 0x05
        TG_TEX2      = 0x06
        TG_TEX3      = 0x07
        TG_TEX4      = 0x08
        TG_TEX5      = 0x09
        TG_TEX6      = 0x0A
        TG_TEX7      = 0x0B
        TG_TEXCOORD0 = 0x0C
        TG_TEXCOORD1 = 0x0D
        TG_TEXCOORD2 = 0x0E
        TG_TEXCOORD3 = 0x0F
        TG_TEXCOORD4 = 0x10
        TG_TEXCOORD5 = 0x11
        TG_TEXCOORD6 = 0x12
        TG_COLOR0    = 0x13
        TG_COLOR1    = 0x14

    class CompCnt(IntEnum):
        POS_XY   = 0
        POS_XYZ  = 1
        NRM_XYZ  = 0
        NRM_NBT  = 1 #  one index per NBT
        NRM_NBT3 = 2 #  one index per each of N/B/T
        CLR_RGB  = 0
        CLR_RGBA = 1
        TEX_S    = 0
        TEX_ST   = 1

    class CompType(IntEnum):
        U8     = 0
        S8     = 1
        U16    = 2
        S16    = 3
        F32    = 4
        RGB565 = 0
        RGB8   = 1
        RGBX8  = 2
        RGBA4  = 3
        RGBA6  = 4
        RGBA8  = 5

    class ChannelID(IntEnum):
        COLOR0      = 0x00
        COLOR1      = 0x01
        ALPHA0      = 0x02
        ALPHA1      = 0x03
        COLOR0A0    = 0x04 # Color 0 + Alpha 0
        COLOR1A1    = 0x05 # Color 1 + Alpha 1
        COLOR_ZERO  = 0x06 # RGBA = 0
        ALPHA_BUMP  = 0x07 # bump alpha 0-248, RGB=0
        ALPHA_BUMPN = 0x08 # normalized bump alpha, 0-255, RGB=0
        COLOR_NULL  = 0xFF

    class ColorSrc(IntEnum):
        SRC_REG = 0
        SRC_VTX = 1

    class LightID(IntEnum):
        LIGHT0     = 0x001
        LIGHT1     = 0x002
        LIGHT2     = 0x004
        LIGHT3     = 0x008
        LIGHT4     = 0x010
        LIGHT5     = 0x020
        LIGHT6     = 0x040
        LIGHT7     = 0x080
        MAX_LIGHT  = 0x100
        LIGHT_NULL = 0x000

    class DiffuseFn(IntEnum):
        NONE  = 0
        SIGN  = 1
        CLAMP = 2

    class AttnFn(IntEnum):
        SPEC = 0 # use specular attenuation
        SPOT = 1 # use distance/spotlight attenuation
        NONE = 2 # attenuation is off

    class SpotFn(IntEnum):
        OFF   = 0x00
        FLAT  = 0x01
        COS   = 0x02
        COS2  = 0x03
        SHARP = 0x04
        RING1 = 0x05
        RING2 = 0x06

    class DistAttnFn(IntEnum):
        OFF    = 0
        GENTLE = 1
        MEDIUM = 2
        STEEP  = 3

    class PosNrmMtx(IntEnum):
        PNMTX0  = 0
        PNMTX1  = 3
        PNMTX2  = 6
        PNMTX3  = 9
        PNMTX4 = 12
        PNMTX5 = 15
        PNMTX6 = 18
        PNMTX7 = 21
        PNMTX8 = 24
        PNMTX9 = 27

    class TexMtx(IntEnum):
        TEXMTX0  = 30
        TEXMTX1  = 33
        TEXMTX2  = 36
        TEXMTX3  = 39
        TEXMTX4  = 42
        TEXMTX5  = 45
        TEXMTX6  = 48
        TEXMTX7  = 51
        TEXMTX8  = 54
        TEXMTX9  = 57
        IDENTITY: 60

    class PTTexMtx(IntEnum):
        PTTEXMTX0   = 64
        PTTEXMTX1   = 67
        PTTEXMTX2   = 70
        PTTEXMTX3   = 73
        PTTEXMTX4   = 76
        PTTEXMTX5   = 79
        PTTEXMTX6   = 82
        PTTEXMTX7   = 85
        PTTEXMTX8   = 88
        PTTEXMTX9   = 91
        PTTEXMTX10  = 94
        PTTEXMTX11  = 97
        PTTEXMTX12 = 100
        PTTEXMTX13 = 103
        PTTEXMTX14 = 106
        PTTEXMTX15 = 109
        PTTEXMTX16 = 112
        PTTEXMTX17 = 115
        PTTEXMTX18 = 118
        PTTEXMTX19 = 121
        PTIDENTITY = 125

    class TexMtxType(IntEnum):
        MTX3x4 = 0
        MTX2x4 = 1

    class Primitive(IntEnum):
        POINTS        = 0xB8
        LINES         = 0xA8
        LINESTRIP     = 0xB0
        TRIANGLES     = 0x90
        TRIANGLESTRIP = 0x98
        TRIANGLEFAN   = 0xA0
        QUADS         = 0x80

    class TexOffset(IntEnum):
        ZERO          = 0
        SIXTEENTH     = 1
        EIGHTH        = 2
        FOURTH        = 3
        HALF          = 4
        ONE           = 5
        MAX_TEXOFFSET = 6

    class CullMode(IntEnum):
        NONE  = 0
        FRONT = 1
        BACK  = 2
        ALL   = 3

    class ClipMode(IntEnum):
        #  Note: these are (by design) backwards of typical enable/disables!
        ENABLE  = 0
        DISABLE = 1

    class TexWrapMode(IntEnum):
        CLAMP           = 0
        REPEAT          = 1
        MIRROR          = 2
        MAX_TEXWRAPMODE = 3

    class TexFilter(IntEnum):
        NEAR          = 0
        LINEAR        = 1
        NEAR_MIP_NEAR = 2
        LIN_MIP_NEAR  = 3
        NEAR_MIP_LIN  = 4
        LIN_MIP_LIN   = 5

    class CITexFmt(IntEnum):
        C4    = 0x8
        C8    = 0x9
        C14X2 = 0xA

    class TexFmt(IntEnum):
        TF_I4     = 0x0
        TF_I8     = 0x1
        TF_IA4    = 0x2
        TF_IA8    = 0x3
        TF_RGB565 = 0x4
        TF_RGB5A3 = 0x5
        TF_RGBA8  = 0x6
        TF_CMPR   = 0xE
        CTF_R4    = 0x0 | _GX_TF_CTF
        CTF_RA4   = 0x2 | _GX_TF_CTF
        CTF_RA8   = 0x3 | _GX_TF_CTF
        CTF_YUVA8 = 0x6 | _GX_TF_CTF
        CTF_A8    = 0x7 | _GX_TF_CTF
        CTF_R8    = 0x8 | _GX_TF_CTF
        CTF_G8    = 0x9 | _GX_TF_CTF
        CTF_B8    = 0xA | _GX_TF_CTF
        CTF_RG8   = 0xB | _GX_TF_CTF
        CTF_GB8   = 0xC | _GX_TF_CTF
        TF_Z8     = 0x1 | _GX_TF_ZTF
        TF_Z16    = 0x3 | _GX_TF_ZTF
        TF_Z24X8  = 0x6 | _GX_TF_ZTF
        CTF_Z4    = 0x0 | _GX_TF_ZTF | _GX_TF_CTF
        CTF_Z8M   = 0x9 | _GX_TF_ZTF | _GX_TF_CTF
        CTF_Z8L   = 0xA | _GX_TF_ZTF | _GX_TF_CTF
        CTF_Z16L  = 0xC | _GX_TF_ZTF | _GX_TF_CTF
        TF_A8     = 0x7 | _GX_TF_CTF #  to keep compatibility

    class TlutFmt(IntEnum):
        IA8         = 0x0
        RGB565      = 0x1
        RGB5A3      = 0x2
        MAX_TLUTFMT = 0x3

    class TlutSize(IntEnum):
        TLUT_16     = 1	#  number of 16 entry blocks.
        TLUT_32     = 2
        TLUT_64     = 4
        TLUT_128    = 8
        TLUT_256   = 16
        TLUT_512   = 32
        TLUT_1K    = 64
        TLUT_2K   = 128
        TLUT_4K   = 256
        TLUT_8K   = 512
        TLUT_16K = 1024

    class Tlut(IntEnum):
        #  default 256-entry TLUTs
        TLUT0    = 0x00
        TLUT1    = 0x01
        TLUT2    = 0x02
        TLUT3    = 0x03
        TLUT4    = 0x04
        TLUT5    = 0x05
        TLUT6    = 0x06
        TLUT7    = 0x07
        TLUT8    = 0x08
        TLUT9    = 0x09
        TLUT10   = 0x0A
        TLUT11   = 0x0B
        TLUT12   = 0x0C
        TLUT13   = 0x0D
        TLUT14   = 0x0E
        TLUT15   = 0x0F
        BIGTLUT0 = 0x10
        BIGTLUT1 = 0x11
        BIGTLUT2 = 0x12
        BIGTLUT3 = 0x13

    class TexMapID(IntEnum):
        TEXMAP0      = 0x00
        TEXMAP1      = 0x01
        TEXMAP2      = 0x02
        TEXMAP3      = 0x03
        TEXMAP4      = 0x04
        TEXMAP5      = 0x05
        TEXMAP6      = 0x06
        TEXMAP7      = 0x07
        MAX_TEXMAP   = 0x08
        TEXMAP_NULL  = 0xFF
        TEX_DISABLE  = 0x100 # mask: disables texture look up

    class TexCacheSize(IntEnum):
        TEXCACHE_32K  = 0
        TEXCACHE_128K = 1
        TEXCACHE_512K = 2
        TEXCACHE_NONE = 3

    class IndTexFormat(IntEnum):
        ITF_8 = 0 # 8 bit texture offsets.
        ITF_5 = 1 # 5 bit texture offsets.
        ITF_4 = 2 # 4 bit texture offsets.
        ITF_3 = 3 # 3 bit texture offsets.
        MAX_ITFORMAT = 4

    class IndTexBiasSel(IntEnum):
        NONE = 0
        S    = 1
        T    = 2
        ST   = 3
        U    = 4
        SU   = 5
        TU   = 6
        STU  = 7
        MAX_ITBIAS = 8

    class IndTexAlphaSel(IntEnum):
        OFF = 0
        S   = 1
        T   = 2
        U   = 3
        MAX_ITBALPHA = 4

    class IndTexMtxID(IntEnum):
        ITM_OFF = 0
        ITM_0   = 1
        ITM_1   = 2
        ITM_2   = 3 # skip 4
        ITM_S0  = 5
        ITM_S1  = 6
        ITM_S2  = 7 # skip 8
        ITM_T0  = 9
        ITM_T1 = 10
        ITM_T2 = 11

    class IndTexWrap(IntEnum):
        ITW_OFF = 0 # no wrapping
        ITW_256 = 1 # wrap 256
        ITW_128 = 2 # wrap 128
        ITW_64  = 3 # wrap 64
        ITW_32  = 4 # wrap 32
        ITW_16  = 5 # wrap 16
        ITW_0   = 6 # wrap 0
        MAX_ITWRAP = 7

    class IndTexScale(IntEnum):
        ITS_1   = 0 # Scale by 1.
        ITS_2   = 1 # Scale by 1/2.
        ITS_4   = 2 # Scale by 1/4.
        ITS_8   = 3 # Scale by 1/8.
        ITS_16  = 4 # Scale by 1/16.
        ITS_32  = 5 # Scale by 1/32.
        ITS_64  = 6 # Scale by 1/64.
        ITS_128 = 7 # Scale by 1/128.
        ITS_256 = 8 # Scale by 1/256.
        MAX_ITSCALE = 9

    # GXIndTexStageID just maps n to n
    # GXTevStageID just maps n to n
    class TevRegID(IntEnum):
        TEVPREV = 0
        TEVREG0 = 1
        TEVREG1 = 2
        TEVREG2 = 3
        MAX_TEVREG = 4

    class TevOp(IntEnum):
        ADD            = 0
        SUB            = 1
        COMP_R8_GT     = 8
        COMP_R8_EQ     = 9
        COMP_GR16_GT  = 10
        COMP_GR16_EQ  = 11
        COMP_BGR24_GT = 12
        COMP_BGR24_EQ = 13
        COMP_RGB8_GT  = 14
        COMP_RGB8_EQ  = 15
        COMP_A8_GT    = 14 #  for alpha channel
        COMP_A8_EQ:    15  #  for alpha channel

    class TevColorArg(IntEnum):
        CPREV   = 0x00
        APREV   = 0x01
        C0      = 0x02
        A0      = 0x03
        C1      = 0x04
        A1      = 0x05
        C2      = 0x06
        A2      = 0x07
        TEXC    = 0x08
        TEXA    = 0x09
        RASC    = 0x0A
        RASA    = 0x0B
        ONE     = 0x0C
        HALF    = 0x0D
        KONST   = 0x0E
        ZERO    = 0x0F
        TEXRRR  = 0x10 #  obsolete
        TEXGGG  = 0x11 #  obsolete
        TEXBBB  = 0x12 #  obsolete
        QUARTER = 0x0E #  obsolete, to keep compatibility

    class TevAlphaArg(IntEnum):
        APREV = 0
        A0    = 1
        A1    = 2
        A2    = 3
        TEXA  = 4
        RASA  = 5
        KONST = 6
        ZERO  = 7
        ONE   = 6 # obsolete, to keep compatibility

    class TevBias(IntEnum):
        ZERO        = 0
        ADDHALF     = 1
        SUBHALF     = 2
        MAX_TEVBIAS = 3

    class TevClampMode(IntEnum):
        LINEAR = 0
        GE     = 1
        EQ     = 2
        LE     = 3
        MAX_TEVCLAMPMODE = 4

    # TevKColorID just maps n to n
    class TevKColorSel(IntEnum):
        KCSEL_8_8  = 0x00
        KCSEL_7_8  = 0x01
        KCSEL_6_8  = 0x02
        KCSEL_5_8  = 0x03
        KCSEL_4_8  = 0x04
        KCSEL_3_8  = 0x05
        KCSEL_2_8  = 0x06
        KCSEL_1_8  = 0x07
        KCSEL_1    = 0x00
        KCSEL_3_4  = 0x02
        KCSEL_1_2  = 0x04
        KCSEL_1_4  = 0x06
        KCSEL_K0   = 0x0C
        KCSEL_K1   = 0x0D
        KCSEL_K2   = 0x0E
        KCSEL_K3   = 0x0F
        KCSEL_K0_R = 0x10
        KCSEL_K1_R = 0x11
        KCSEL_K2_R = 0x12
        KCSEL_K3_R = 0x13
        KCSEL_K0_G = 0x14
        KCSEL_K1_G = 0x15
        KCSEL_K2_G = 0x16
        KCSEL_K3_G = 0x17
        KCSEL_K0_B = 0x18
        KCSEL_K1_B = 0x19
        KCSEL_K2_B = 0x1A
        KCSEL_K3_B = 0x1B
        KCSEL_K0_A = 0x1C
        KCSEL_K1_A = 0x1D
        KCSEL_K2_A = 0x1E
        KCSEL_K3_A = 0x1F

    class TevKAlphaSel(IntEnum):
        KASEL_8_8  = 0x00
        KASEL_7_8  = 0x01
        KASEL_6_8  = 0x02
        KASEL_5_8  = 0x03
        KASEL_4_8  = 0x04
        KASEL_3_8  = 0x05
        KASEL_2_8  = 0x06
        KASEL_1_8  = 0x07
        KASEL_1    = 0x00
        KASEL_3_4  = 0x02
        KASEL_1_2  = 0x04
        KASEL_1_4  = 0x06
        KASEL_K0_R = 0x10
        KASEL_K1_R = 0x11
        KASEL_K2_R = 0x12
        KASEL_K3_R = 0x13
        KASEL_K0_G = 0x14
        KASEL_K1_G = 0x15
        KASEL_K2_G = 0x16
        KASEL_K3_G = 0x17
        KASEL_K0_B = 0x18
        KASEL_K1_B = 0x19
        KASEL_K2_B = 0x1A
        KASEL_K3_B = 0x1B
        KASEL_K0_A = 0x1C
        KASEL_K1_A = 0x1D
        KASEL_K2_A = 0x1E
        KASEL_K3_A = 0x1F

    class TevSwapSel(IntEnum):
        SWAP0 = 0
        SWAP1 = 1
        SWAP2 = 2
        SWAP3 = 3
        MAX_TEVSWAP = 4

    class TevColorChan(IntEnum):
        RED   = 0
        GREEN = 1
        BLUE  = 2
        ALPHA = 3

    class AlphaOp(IntEnum):
        AND  = 0
        OR   = 1
        XOR  = 2
        XNOR = 3
        MAX_ALPHAOP = 4

    class TevScale(IntEnum):
        SCALE_1  = 0
        SCALE_2  = 1
        SCALE_4  = 2
        DIVIDE_2 = 3
        MAX_TEVSCALE = 4

    class FogType(IntEnum):
        GX_FOG_NONE          = 0x00
        GX_FOG_PERSP_LIN     = 0x02
        GX_FOG_PERSP_EXP     = 0x04
        GX_FOG_PERSP_EXP2    = 0x05
        GX_FOG_PERSP_REVEXP  = 0x06
        GX_FOG_PERSP_REVEXP2 = 0x07
        GX_FOG_ORTHO_LIN     = 0x0A
        GX_FOG_ORTHO_EXP     = 0x0C
        GX_FOG_ORTHO_EXP2    = 0x0D
        GX_FOG_ORTHO_REVEXP  = 0x0E
        GX_FOG_ORTHO_REVEXP2 = 0x0F
        #  For compatibility with former versions
        GX_FOG_LIN           = 0x02 # GX_FOG_PERSP_LIN,
        GX_FOG_EXP           = 0x04 # GX_FOG_PERSP_EXP,
        GX_FOG_EXP2          = 0x05 # GX_FOG_PERSP_EXP2,
        GX_FOG_REVEXP        = 0x06 # GX_FOG_PERSP_REVEXP,
        GX_FOG_REVEXP2       = 0x07 # GX_FOG_PERSP_REVEXP2

    class BlendMode(IntEnum):
        NONE     = 0x0
        BLEND    = 0x1
        LOGIC    = 0x2
        SUBTRACT = 0x3

    class BlendFactor(IntEnum):
        ZERO        = 0x0
        ONE         = 0x1
        SRCCLR      = 0x2
        INVSRCCLR   = 0x3
        SRCALPHA    = 0x4
        INVSRCALPHA = 0x5
        DSTALPHA    = 0x6
        INVDSTALPHA = 0x7

    class Compare(IntEnum):
        NEVER   = 0x0
        LESS    = 0x1
        EQUAL   = 0x2
        LEQUAL  = 0x3
        GREATER = 0x4
        NEQUAL  = 0x5
        GEQUAL  = 0x6
        ALWAYS  = 0x7

    class LogicOp(IntEnum):
        CLEAR   = 0x0
        AND     = 0x1
        REVAND  = 0x2
        COPY    = 0x3
        INVAND  = 0x4
        NOOP    = 0x5
        XOR     = 0x6
        OR      = 0x7
        NOR     = 0x8
        EQUIV   = 0x9
        INV     = 0xa
        REVOR   = 0xb
        INVCOPY = 0xc
        INVOR   = 0xd
        NAND    = 0xe
        SET     = 0xf

    class PixelFmt(IntEnum):
        RGB8_Z24   = 0
        RGBA6_Z24  = 1
        RGB565_Z16 = 2
        Z24        = 3
        Y8         = 4
        U8         = 5
        V8         = 6
        YUV420     = 7

    class ZFmt16(IntEnum):
        LINEAR = 0
        NEAR   = 1
        MID    = 2
        FAR    = 3

    class TevMode(IntEnum):
        MODULATE = 0
        DECAL    = 1
        BLEND    = 2
        REPLACE  = 3
        PASSCLR  = 4

    class Gamma(IntEnum):
        GM_1_0 = 0
        GM_1_7 = 1
        GM_2_2 = 2

    class ProjectionType(IntEnum):
        PERSPECTIVE  = 0
        ORTHOGRAPHIC = 1

    class Event(IntEnum):
        VCACHE_MISS_ALL = 0
        VCACHE_MISS_POS = 1
        VCACHE_MISS_NRM = 2

    class FBClamp(IntEnum):
        CLAMP_NONE   = 0
        CLAMP_TOP    = 1
        CLAMP_BOTTOM = 2

    class Anisotropy(IntEnum):
        ANISO_1 = 0
        ANISO_2 = 1
        ANISO_4 = 2
        MAX_ANISOTROPY = 3

    class ZTexOp(IntEnum):
        DISABLE    = 0
        ADD        = 1
        REPLACE    = 2
        MAX_ZTEXOP = 3

    class AlphaReadMode(IntEnum):
        READ_00   = 0
        READ_FF   = 1
        READ_NONE = 2

    class Perf0(IntEnum):
        VERTICES            = 0x00
        CLIP_VTX            = 0x01
        CLIP_CLKS           = 0x02
        XF_WAIT_IN          = 0x03
        XF_WAIT_OUT         = 0x04
        XF_XFRM_CLKS        = 0x05
        XF_LIT_CLKS         = 0x06
        XF_BOT_CLKS         = 0x07
        XF_REGLD_CLKS       = 0x08
        XF_REGRD_CLKS       = 0x09
        CLIP_RATIO          = 0x0A
        TRIANGLES           = 0x0B
        TRIANGLES_CULLED    = 0x0C
        TRIANGLES_PASSED    = 0x0D
        TRIANGLES_SCISSORED = 0x0E
        TRIANGLES_0TEX      = 0x0F
        TRIANGLES_1TEX      = 0x10
        TRIANGLES_2TEX      = 0x11
        TRIANGLES_3TEX      = 0x12
        TRIANGLES_4TEX      = 0x13
        TRIANGLES_5TEX      = 0x14
        TRIANGLES_6TEX      = 0x15
        TRIANGLES_7TEX      = 0x16
        TRIANGLES_8TEX      = 0x17
        TRIANGLES_0CLR      = 0x18
        TRIANGLES_1CLR      = 0x19
        TRIANGLES_2CLR      = 0x1A
        QUAD_0CVG           = 0x1B
        QUAD_NON0CVG        = 0x1C
        QUAD_1CVG           = 0x1D
        QUAD_2CVG           = 0x1E
        QUAD_3CVG           = 0x1F
        QUAD_4CVG           = 0x20
        AVG_QUAD_CNT        = 0x21
        CLOCKS              = 0x22
        NONE                = 0x23

    class Perf1(IntEnum):
        TEXELS           = 0x00
        TX_IDLE          = 0x01
        TX_REGS          = 0x02
        TX_MEMSTALL      = 0x03
        TC_CHECK1_2      = 0x04
        TC_CHECK3_4      = 0x05
        TC_CHECK5_6      = 0x06
        TC_CHECK7_8      = 0x07
        TC_MISS          = 0x08
        VC_ELEMQ_FULL    = 0x09
        VC_MISSQ_FULL    = 0x0A
        VC_MEMREQ_FULL   = 0x0B
        VC_STATUS7       = 0x0C
        VC_MISSREP_FULL  = 0x0D
        VC_STREAMBUF_LOW = 0x0E
        VC_ALL_STALLS    = 0x0F
        VERTICES         = 0x10
        FIFO_REQ         = 0x11
        CALL_REQ         = 0x12
        VC_MISS_REQ      = 0x13
        CP_ALL_REQ       = 0x14
        CLOCKS           = 0x15
        NONE             = 0x16

    class VCachePerf(IntEnum):
        POS  = 0x0
        NRM  = 0x1
        CLR0 = 0x2
        CLR1 = 0x3
        TEX0 = 0x4
        TEX1 = 0x5
        TEX2 = 0x6
        TEX3 = 0x7
        TEX4 = 0x8
        TEX5 = 0x9
        TEX6 = 0xA
        TEX7 = 0xB
        ALL  = 0xF

    class CopyMode(IntEnum):
        PROGRESSIVE = 0
        INTLC_EVEN  = 2
        INTLC_ODD   = 3

    class MiscToken(IntEnum):
        XF_FLUSH           = 1
        DL_SAVE_CONTEXT    = 2
        ABORT_WAIT_COPYOUT = 3
        NULL               = 0

    class XFFlushVal(IntEnum):
        NONE = 0
        SAFE = 8
