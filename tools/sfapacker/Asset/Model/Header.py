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

class Header(MyStruct):
    """The header of a model file on disc/in RAM."""
    # ^ denotes fields that are always 0 in the files on disc
    _fields_ = [
        ('usage',                 u8),    # 00 ref count
        ('unk01',                 u8),    # 01
        ('flags',                 u16),   # 02 ModelDataFlags2
        ('id',                    u16),   # 04 internally "cacheModNo"
        ('unk06',                 u16),   # 06 padding?
        ('headerCksum',           u32),   # 08
        ('dataSize',              u32),   # 0C size of this file
        ('unk10',                 u32),   # 10
        ('unk14',                 u32),   # 14
        ('radi',                  f32),   # 18 or float* ? maybe a scale
        ('exT',                   f32),   # 1C extraAmapSize (dlInfoSize?)
        ('textures',              u32),   # 20 ptr to tex IDs (u32, changed to ptrs on load)
        ('flags24',               u8),    # 24 ModelDataFlags24
        ('unk25',                 u8),    # 25 relates to lighting
        ('unk26',                 u16),   # 26 padding?
        ('vertexPositions',       u32),   # 28 vec3s*
        ('vertexNormals',         u32),   # 2C vec3s*
        ('vertexColours',         u32),   # 30 u16* (probably RGBA4444 since maps use that)
        ('vertexTexCoords',       u32),   # 34 vec2s*
        ('shaders',               u32),   # 38 Shader*
        ('joints',                u32),   # 3C Bone*
        ('boneQuats',             u32),   # 40 Quaternion*
        ('unk44',                 u32*3), # 44
        ('unk50',                 u32),   # 50
        ('vtxGroups',             u32),   # 54 ModelVtxGroup* aka weights
        ('hitSpheres',            u32),   # 58 HitSphere*
        ('GCpolygons',            u32),   # 5C GCpolygon* (hit detection)
        ('polygonGroups',         u32),   # 60 PolygonGroup*
        ('pAltIndBuf',            u32),   # 64 ?*
        ('amapBin',               u32),   # 68 u16*? from AMAP.BIN
        ('animIds',               u32),   #^6C s16* (XXX is this zero in file or is the data it points to?)
        ('animIdxs',              u16*8), # 70
        ('amapTab',               u32),   # 80
        ('animCacheSize',         u16),   # 84
        ('unk86',                 u16),   # 86 padding?
        ('posFineSkinningConfig', u32),   # 88 FineSkinningConfig*
        ('unk8C',                 u32),   # 8C
        ('unk90',                 u32),   # 90
        ('unk94',                 u32),   # 94
        ('unk98',                 u32),   # 98
        ('unk9C',                 u32),   # 9C
        ('unkA0',                 u32),   # A0
        ('posFineSkinningPieces', u32),   # A4 FineSkinningPiece* related to animBuf/vtxs; field_88.nVtxs = how many
        ('posFineSkinningWeights',u32),   # A8 ?*
        ('nrmFineSkinningConfig', u32),   # AC FineSkinningConfig*
        ('unkB0',                 u32),   # B0
        ('unkB4',                 u32),   # B4
        ('unkB8',                 u32),   # B8
        ('unkBC',                 u32),   # BC
        ('unkC0',                 u32),   # C0
        ('unkC4',                 u32),   # C4
        ('unkC8',                 u32),   # C8 -> sth 0x4 bytes; related to normals/textures; field AE = how many
        ('unkCC',                 u32),   # CC ?*
        ('dlists',                u32),   # D0 DisplayListPtr*
        ('renderInstrs',          u32),   # D4 -> bit-packed render ops
        ('nRenderInstrs',         u16),   # D8 #bytes
        ('unkDA',                 u16),   # DA padding?
        ('animations',            u32),   # DC s16**
        ('cullDistance',          s16),   # E0
        ('flagsE2',               u16),   # E2 ModelHeaderFlagsE2
        ('nVtxs',                 u16),   # E4
        ('nNormals',              u16),   # E6
        ('nColors',               u16),   # E8
        ('nTexCoords',            u16),   # EA
        ('nAnimations',           u16),   # EC
        ('unkEE',                 u16),   # EE nSomething?
        ('nPolyGroups',           u16),   # F0
        ('nTextures',             u8),    # F2
        ('nBones',                u8),    # F3 #mtxs at Model->mtxs
        ('nVtxGroups',            u8),    # F4
        ('nDlists',               u8),    # F5
        ('unkF6',                 u8),    # F6 nSomething?
        ('nHitSpheres',           u8),    # F7
        ('nShaders',              u8),    # F8
        ('nPtrsDC',               u8),    # F9 nAnimations? (#ptrs at field 0xDC)
        ('nTexMtxs',              u8),    # FA
        ('unkFB',                 u8),    # FB padding?
    ]
