# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from enum import IntEnum

NUM_VATS = 8

VAT_MASK = { #[mask, shift]
    #VAT A
    'POSCNT':        [0x01,  0],
    'POSFMT':        [0x07,  1],
    'POSSHFT':       [0x1F,  4],
    'NRMCNT':        [0x01,  9],
    'NRMFMT':        [0x07, 10],
    'COL0CNT':       [0x01, 13],
    'COL0FMT':       [0x07, 14],
    'COL1CNT':       [0x01, 17],
    'COL1FMT':       [0x07, 18],
    'TEX0CNT':       [0x01, 21],
    'TEX0FMT':       [0x07, 22],
    'TEX0SHFT':      [0x1F, 25],
    'BYTEDEQUANT':   [0x01, 30],
    'NORMALINDEX3':  [0x01, 31],

    #VAT B
    'TEX1CNT':       [0x01,  0],
    'TEX1FMT':       [0x07,  1],
    'TEX1SHFT':      [0x1F,  4],
    'TEX2CNT':       [0x01,  9],
    'TEX2FMT':       [0x07, 10],
    'TEX2SHFT':      [0x1F, 13],
    'TEX3CNT':       [0x01, 18],
    'TEX3FMT':       [0x07, 19],
    'TEX3SHFT':      [0x1F, 22],
    'TEX4CNT':       [0x01, 27],
    'TEX4FMT':       [0x07, 28],
    'VCACHE_ENHANCE':[0x01, 31], #"must always be 1"

    #VAT C
    'TEX4SHFT':      [0x1F,  0],
    'TEX5CNT':       [0x01,  5],
    'TEX5FMT':       [0x07,  6],
    'TEX5SHFT':      [0x1F,  9],
    'TEX6CNT':       [0x01, 14],
    'TEX6FMT':       [0x07, 15],
    'TEX6SHFT':      [0x1F, 18],
    'TEX7CNT':       [0x01, 23],
    'TEX7FMT':       [0x07, 24],
    'TEX7SHFT':      [0x1F, 27],
}

class CP:
    class Reg(IntEnum):
        MATINDEX_A            = 0x30
        MATINDEX_B            = 0x40
        VCD_LO                = 0x50 # 0-7
        VCD_HI                = 0x60 # 0-7
        VAT_A                 = 0x70 # 0-7
        VAT_B                 = 0x80 # 0-7
        VAT_C                 = 0x90 # 0-7
        ARRAY_BASE_VTXS       = 0xA0
        ARRAY_BASE_NORMALS    = 0xA1
        ARRAY_BASE_COLOR      = 0xA2 # 0-1
        ARRAY_BASE_TEXCOORD   = 0xA4 # 0-7
        ARRAY_BASE_INDEX      = 0xAC # 0-3, general purpose array
        ARRAY_STRIDE_VTXS     = 0xB0
        ARRAY_STRIDE_NORMALS  = 0xB1
        ARRAY_STRIDE_COLOR    = 0xB2
        ARRAY_STRIDE_TEXCOORD = 0xB4
        ARRAY_STRIDE_INDEX    = 0xBC

    def __init__(self, gx) -> None:
        self.gx = gx
        self.reset()

    def reset(self):
        """Reset all state back to default."""
        self._rawVals = {}
        self.vcd = []
        self.arrayBase = {
            'POS': 0, 'NRM': 0, 'COL0':0, 'COL1':0,
            'TEX0':0, 'TEX1':0, 'TEX2':0, 'TEX3':0,
            'TEX4':0, 'TEX5':0, 'TEX6':0, 'TEX7':0,
            'IDXA':0, 'IDXB':0, 'IDXC':0, 'IDXD':0,
        }
        self.arrayStride = {
            'POS': 0, 'NRM': 0, 'COL0':0, 'COL1':0,
            'TEX0':0, 'TEX1':0, 'TEX2':0, 'TEX3':0,
            'TEX4':0, 'TEX5':0, 'TEX6':0, 'TEX7':0,
            'IDXA':0, 'IDXB':0, 'IDXC':0, 'IDXD':0,
        }
        for i in range(NUM_VATS):
            self.vcd.append({})
            self.setReg(i+CP.Reg.VCD_LO, 0x200)
            self.setReg(i+CP.Reg.VCD_HI, 0)
            self.setReg(i+CP.Reg.VAT_A,  0x40000000)
            self.setReg(i+CP.Reg.VAT_B,  0x80000000)
            self.setReg(i+CP.Reg.VAT_C,  0)

    def getReg(self, reg:int) -> int:
        return self._rawVals[reg]

    def setReg(self, reg:int, val:int):
        """Set CP register.

        :param reg: Register ID.
        :param val: Value, which should be a 32-bit integer.
        """
        self._rawVals[reg] = val
        if   reg in range(0x50,0x58): self._setVcdLo(reg&7, val)
        elif reg in range(0x60,0x68): self._setVcdHi(reg&7, val)
        elif reg in range(0x70,0x78): self._setVcdFmtA(reg&7, val)
        elif reg in range(0x80,0x88): self._setVcdFmtB(reg&7, val)
        elif reg in range(0x90,0x98): self._setVcdFmtC(reg&7, val)
        elif reg == 0xA0: self._setArrayBase('POS',  val)
        elif reg == 0xA1: self._setArrayBase('NRM',  val)
        elif reg == 0xA2: self._setArrayBase('COL0', val)
        elif reg == 0xA3: self._setArrayBase('COL1', val)
        elif reg == 0xA4: self._setArrayBase('TEX0', val)
        elif reg == 0xA5: self._setArrayBase('TEX1', val)
        elif reg == 0xA6: self._setArrayBase('TEX2', val)
        elif reg == 0xA7: self._setArrayBase('TEX3', val)
        elif reg == 0xA8: self._setArrayBase('TEX4', val)
        elif reg == 0xA9: self._setArrayBase('TEX5', val)
        elif reg == 0xAA: self._setArrayBase('TEX6', val)
        elif reg == 0xAB: self._setArrayBase('TEX7', val)
        elif reg == 0xAC: self._setArrayBase('IDXA', val)
        elif reg == 0xAD: self._setArrayBase('IDXB', val)
        elif reg == 0xAE: self._setArrayBase('IDXC', val)
        elif reg == 0xAF: self._setArrayBase('IDXD', val)
        elif reg == 0xB0: self._setArrayStride('POS',  val)
        elif reg == 0xB1: self._setArrayStride('NRM',  val)
        elif reg == 0xB2: self._setArrayStride('COL0', val)
        elif reg == 0xB3: self._setArrayStride('COL1', val)
        elif reg == 0xB4: self._setArrayStride('TEX0', val)
        elif reg == 0xB5: self._setArrayStride('TEX1', val)
        elif reg == 0xB6: self._setArrayStride('TEX2', val)
        elif reg == 0xB7: self._setArrayStride('TEX3', val)
        elif reg == 0xB8: self._setArrayStride('TEX4', val)
        elif reg == 0xB9: self._setArrayStride('TEX5', val)
        elif reg == 0xBA: self._setArrayStride('TEX6', val)
        elif reg == 0xBB: self._setArrayStride('TEX7', val)
        elif reg == 0xBC: self._setArrayStride('IDXA', val)
        elif reg == 0xBD: self._setArrayStride('IDXB', val)
        elif reg == 0xBE: self._setArrayStride('IDXC', val)
        elif reg == 0xBF: self._setArrayStride('IDXD', val)
        else:
            raise ValueError(
                "Don't know what to do with CP reg 0x%X (val 0x%X" % (
                reg, val))

    def _setVcdLo(self, vcd, val): # CP registers 0x50 - 0x57
        # these describe the params of draw commands; whether each
        # field has nothing, the direct value, or an index.
        self.vcd[vcd]['PNMTXIDX'] =  val        & 1 # Position/Normal Matrix Index (*1)
        self.vcd[vcd]['T0MIDX']   = (val >>  1) & 1 # Texture Coordinate 0 Matrix Index
        self.vcd[vcd]['T1MIDX']   = (val >>  2) & 1
        self.vcd[vcd]['T2MIDX']   = (val >>  3) & 1
        self.vcd[vcd]['T3MIDX']   = (val >>  4) & 1
        self.vcd[vcd]['T4MIDX']   = (val >>  5) & 1
        self.vcd[vcd]['T5MIDX']   = (val >>  6) & 1
        self.vcd[vcd]['T6MIDX']   = (val >>  7) & 1
        self.vcd[vcd]['T7MIDX']   = (val >>  8) & 1
        self.vcd[vcd]['POS']      = (val >>  9) & 3 # Position
        self.vcd[vcd]['NRM']      = (val >> 11) & 3 # Normal or Normal/Binormal/Tangent
        self.vcd[vcd]['COL0']     = (val >> 13) & 3 # Color0 (Diffused)
        self.vcd[vcd]['COL1']     = (val >> 15) & 3 # Color1 (Specular)
        # (*1) position and normal matrices are stored in 2 seperate areas of
        # internal XF memory, but there is a one to one correspondence between
        # normal and position index. If index 'A' is used for the position,
        # then index 'A' needs to be used for the normal as well.

    def _setVcdHi(self, vcd, val): # CP registers 0x60 - 0x67
        self.vcd[vcd]['TEX0'] =  val        & 3 # texture coordinate 0
        self.vcd[vcd]['TEX1'] = (val >>  2) & 3
        self.vcd[vcd]['TEX2'] = (val >>  4) & 3
        self.vcd[vcd]['TEX3'] = (val >>  6) & 3
        self.vcd[vcd]['TEX4'] = (val >>  8) & 3
        self.vcd[vcd]['TEX5'] = (val >> 10) & 3
        self.vcd[vcd]['TEX6'] = (val >> 12) & 3
        self.vcd[vcd]['TEX7'] = (val >> 14) & 3

    def _setVcdFmtA(self, vcd, val): #  CP registers 0x70 - 0x77
        # these define the format of the attribute data itself.
        # I think this applies to both direct values and arrays.
        self.vcd[vcd]['NORMALINDEX3'] = (val >> 31) & 1 # 1 or 3 idxs per normal
        self.vcd[vcd]['BYTEDEQUANT']  = (val >> 30) & 1 # shift applies to u8/s8 (should always be 1)
        self.vcd[vcd]['TEX0SHFT']     = (val >> 25) & 0x1F
        self.vcd[vcd]['TEX0FMT']      = (val >> 22) & 7
        self.vcd[vcd]['TEX0CNT']      = (val >> 21) & 1
        self.vcd[vcd]['COL1FMT']      = (val >> 18) & 7
        self.vcd[vcd]['COL1CNT']      = (val >> 17) & 1
        self.vcd[vcd]['COL0FMT']      = (val >> 14) & 7
        self.vcd[vcd]['COL0CNT']      = (val >> 13) & 1
        self.vcd[vcd]['NRMFMT']       = (val >> 10) & 7
        self.vcd[vcd]['NRMCNT']       = (val >>  9) & 1
        self.vcd[vcd]['POSSHFT']      = (val >>  4) & 0x1F
        self.vcd[vcd]['POSFMT']       = (val >>  1) & 7
        self.vcd[vcd]['POSCNT']       =  val        & 1
        # (*1) when nine-normals are selected in indirect mode, input will be
        # treated as three staggered indices (one per triple biased by
        # components size), into normal table (note: first index internally
        # biased by 0, second by 1, third by 2)

    def _setVcdFmtB(self, vcd, val): #  CP registers 0x80 - 0x87
        self.vcd[vcd]['VCACHE_ENHANCE'] = (val >> 31) & 1 # must be 1
        self.vcd[vcd]['TEX4FMT']        = (val >> 28) & 7
        self.vcd[vcd]['TEX4CNT']        = (val >> 27) & 1
        self.vcd[vcd]['TEX3SHFT']       = (val >> 22) & 0x1F
        self.vcd[vcd]['TEX3FMT']        = (val >> 19) & 7
        self.vcd[vcd]['TEX3CNT']        = (val >> 18) & 1
        self.vcd[vcd]['TEX2SHFT']       = (val >> 13) & 0x1F
        self.vcd[vcd]['TEX2FMT']        = (val >> 10) & 7
        self.vcd[vcd]['TEX2CNT']        = (val >>  9) & 1
        self.vcd[vcd]['TEX1SHFT']       = (val >>  4) & 0x1F
        self.vcd[vcd]['TEX1FMT']        = (val >>  1) & 7
        self.vcd[vcd]['TEX1CNT']        =  val        & 1

    def _setVcdFmtC(self, vcd, val): # CP registers 0x90 - 0x97
        self.vcd[vcd]['TEX7SHFT'] = (val >> 27) & 0x1F
        self.vcd[vcd]['TEX7FMT']  = (val >> 24) & 7
        self.vcd[vcd]['TEX7CNT']  = (val >> 23) & 1
        self.vcd[vcd]['TEX6SHFT'] = (val >> 18) & 0x1F
        self.vcd[vcd]['TEX6FMT']  = (val >> 15) & 7
        self.vcd[vcd]['TEX6CNT']  = (val >> 14) & 1
        self.vcd[vcd]['TEX5SHFT'] = (val >>  9) & 0x1F
        self.vcd[vcd]['TEX5FMT']  = (val >>  6) & 7
        self.vcd[vcd]['TEX5CNT']  = (val >>  5) & 1
        self.vcd[vcd]['TEX4SHFT'] =  val        & 0x1F

    def _setArrayBase(self, field, val): # CP registers 0xA0 - 0xAF
        # not really used, but included for completeness' sake.
        self.arrayBase[field] = val

    def _setArrayStride(self, field, val): # CP registers 0xB0 - 0xBF
        self.arrayStride[field] = val

    def setVatFormat(self, vat, params):
        # Convenience wrapper for setting up VAT
        fields = {
            'A': ['POSCNT','POSFMT','POSSHFT','NRMCNT','NRMFMT','COL0CNT',
                'COL0FMT','COL1CNT','COL1FMT','TEX0CNT','TEX0FMT','TEX0SHFT',
                'BYTEDEQUANT','NORMALINDEX3'],
            'B': ['TEX1CNT','TEX1FMT','TEX1SHFT','TEX2CNT','TEX2FMT','TEX2SHFT',
                'TEX3CNT','TEX3FMT','TEX3SHFT','TEX4CNT','TEX4FMT',
                'VCACHE_ENHANCE'],
            'C': ['TEX4SHFT','TEX5CNT','TEX5FMT','TEX5SHFT','TEX6CNT','TEX6FMT',
                'TEX6SHFT','TEX7CNT','TEX7FMT','TEX7SHFT'],
        }
        regs = {
            'A': self.getReg(vat+0x70),
            'B': self.getReg(vat+0x80),
            'C': self.getReg(vat+0x90),
        }
        for r in ['A', 'B', 'C']:
            for name in fields[r]:
                v = regs[r]
                p = params.get(name, None)
                if p is not None:
                    mask, shift = VAT_MASK[name]
                    v = (v & ~(mask << shift)) | (p << shift)
                regs[r] = v
        self.setReg(vat+0x70, regs['A'])
        self.setReg(vat+0x80, regs['B'])
        self.setReg(vat+0x90, regs['C'])
