# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from io import BytesIO
from .GX import GX
from ..BinaryFile import BinaryFile

class DlistParser:
    def __init__(self, gx) -> None:
        self.gx = gx

    def parse(self, dList:bytes, buffers:dict[str,bytes]) -> list:
        """Parse a display list.
        :param dList: Display list to parse.
        :param buffers: Dict of vertex attribute buffers.
        :returns: List of operations.
        """
        self.list    = BinaryFile(BytesIO(dList))
        self.result  = []
        self.buffers = {}
        for name, buf in buffers.items():
            if buf is None: continue
            self.buffers[name] = BinaryFile(BytesIO(buf))

        while not self.list.isEof():
            op = self.list.readu8()
            if op >= 0x80 and op <= 0xC0:
                self._parseDrawOp(op)

            elif op == 0x00: pass # NOP

            elif op == 0x08: # LOAD_CP_REG
                self.gx.cp.setReg(
                    self.list.readu8(), self.list.readu32())

            elif op == 0x10: # LOAD_XF_REG
                nVals = (self.list.readu16() & 0xF) + 1
                reg   = self.list.readu16()
                for i in range(nVals):
                    self.gx.xf.setReg(reg+i, self.list.readu32())

            elif op in (0x20, 0x28, 0x30, 0x38): # LOAD_INDX_A, B, C, D
                idx  = self.list.readu16()
                offs = self.list.readu16()
                size = (offs >> 12) + 1
                offs = offs & 0xFFF
                # XXX do something with these

            elif op == 0x40: # CALL_DL
                # we're already parsing a dlist so this is invalid
                raise ValueError("Recursive display list call at offset 0x%X" %
                    self.list.tell())

            elif op == 0x48: pass # INVAL_CACHE (nothing to do here)

            elif op == 0x61: # LOAD_BP_REG
                val = self.list.readu32()
                reg = val >> 24
                val = val & 0xFFFFFF
                # XXX do something with these

            else:
                raise ValueError(
                    "Unknown display list opcode 0x%02X" % op)

        return self.result


    def _parseDrawOp(self, op):
        vat = op & 7
        nVtxs = self.list.readu16()
        op &= ~7
        if   op <  0x90: cmd = 'drawQuads'
        elif op == 0x90: cmd = 'drawTris'
        elif op == 0x98: cmd = 'drawTriStrip'
        elif op == 0xA0: cmd = 'drawTriFan'
        elif op == 0xA8: cmd = 'drawLines'
        elif op == 0xB0: cmd = 'drawLineStrip'
        elif op == 0xB8: cmd = 'drawPoints'
        vtxs = []
        for _ in range(nVtxs):
            vtxs.append(self._readVertex(vat))
        self.result.append([cmd, vat, vtxs])


    def _readVertex(self, vat):
        vtx = {
            # used for debug and to uniquely identify each
            # vertex to avoid making duplicates.
            'offset': self.list.tell(),
            'vat':    vat,
            'dlist':  self.list,
        }
        vcd = self.gx.cp.vcd[vat]
        for field in GX.VAT_FIELD_ORDER:
            fmt = vcd[field]
            val = None
            idx = None

            if fmt == 0: pass # no value
            elif fmt == 1: # direct
                val = self._readAttrDirect(field, self.list, vcd)
            else: # 2:8-bit index; 3:16-bit index
                val, idx = self._readAttrIndexed(field, vcd, fmt)

            if val is None:
                # fall back to a reasonable default
                if field == 'PNMTXIDX': val = 0
                elif field.startswith('COL'):
                    val = (0xFF, 0xFF, 0xFF, 0xFF)
            vtx[field] = val
            vtx[field+'_idx'] = idx
        return vtx


    def _readAttrIndexed(self, field, vcd, fmt):
        if fmt == 2: idx = self.list.readu8()
        else: idx = self.list.readu16()
        src = self.buffers[field]
        val = None
        if src is None: return val, idx

        # validate array stride for this attribute
        stride = self.gx.cp.arrayStride[field]
        if stride is None or stride <= 0:
            raise ValueError("Invalid array stride %s for field %s" % (
                stride, field))

        # compute byte offset
        offs = idx * stride
        if offs >= src.size:
            raise IndexError("Out of bounds index 0x%X for field %s (max is 0x%X)" % (
                idx, field, src.size / stride))

        # read the value from the attribute buffer
        src.seek(offs)
        val = self._readAttrDirect(field, src, vcd)
        return val, idx

    def _readAttrDirect(self, field, src, vcd):
        if field.endswith('IDX'):   return self._readIndexAttr(field, src, vcd)
        if field.startswith('COL'): return self._readColor(field, src, vcd)
        if field.startswith('NRM'): return self._readNormal(field, src, vcd)
        return self._readCoord(field, src, vcd)

    def _readIndexAttr(self, field, src, vcd):
        # XXX verify the SHFT/FMT/CNT don't apply here
        return src.readu8()

    def _readCoord(self, field, src, vcd):
        shift  = vcd.get(field+'SHFT', 0)
        fmt    = vcd.get(field+'FMT',  0)
        count  = vcd.get(field+'CNT',  0)
        vals   = []
        cntMin = 1 if field.startswith('TEX') else 2
        for i in range(count+cntMin):
            val = None
            if   fmt == 0: val = src.readu8()
            elif fmt == 1: val = src.reads8()
            elif fmt == 2: val = src.readu16()
            elif fmt == 3: val = src.reads16()
            elif fmt == 4: val = src.readFloat()
            else: raise ValueError(
                "Invalid format %s for attribute %s" % (
                    field, fmt))
            if (fmt == 0 or fmt == 1) and vcd.get('BYTEDEQUANT', False):
                val /= (1 << shift)
            elif(fmt == 2 or fmt == 3): val /= (1 << shift)
            vals.append(val)
        return vals

    def _readNormal(self, field, src, vcd):
        #shift  = vcd.get(field+'SHFT', 0) # not used for normals
        fmt    = vcd.get(field+'FMT',  0)
        count  = vcd.get(field+'CNT',  0)
        vals   = []
        if count == 0: count = 3
        else: count = 9
        for i in range(count):
            val = None
            # u8, u16 are not valid for normals
            if   fmt == 1: val = src.reads8()  / (1 <<  6)
            elif fmt == 3: val = src.reads16() / (1 << 14)
            elif fmt == 4: val = src.readFloat()
            else: raise ValueError(
                "Invalid format %s for attribute %s" % (
                    field, fmt))
            vals.append(val)
        return vals

    def _readColor(self, field, src, vcd):
        #shift  = vcd.get(field+'SHFT', 0) # not used for colors
        fmt    = vcd.get(field+'FMT',  0)
        count  = vcd.get(field+'CNT',  0) # XXX how does this work for color?
        r, g, b, a = 0xFF, 0xFF, 0xFF, 0xFF
        if   fmt == 0: # RGB565
            v = src.readu16()
            b = ( v        & 0x1F) * (255/31)
            g = ((v >>  5) & 0x3F) * (255/63)
            r = ((v >> 11) & 0x1F) * (255/31)
        elif fmt == 1: # RGB888
            r = src.readu8()
            g = src.readu8()
            b = src.readu8()
        elif fmt == 2: # RGBX8888
            r = src.readu8()
            g = src.readu8()
            b = src.readu8()
            src.readu8() # discard
        elif fmt == 3: # RGBA4444
            v = src.readu16()
            a = ( v        & 0xF) * (255/15)
            b = ((v >>  4) & 0xF) * (255/15)
            g = ((v >>  8) & 0xF) * (255/15)
            r = ((v >> 12) & 0xF) * (255/15)
        elif fmt == 4: # RGBA6666
            v = (src.readu8() << 16) | src.readu16()
            a = ( v        & 0x3F) * (255/63)
            b = ((v >>  6) & 0x3F) * (255/63)
            g = ((v >> 12) & 0x3F) * (255/63)
            r = ((v >> 18) & 0x3F) * (255/63)
        elif fmt == 5: # RGBA8888
            r = src.readu8()
            g = src.readu8()
            b = src.readu8()
            a = src.readu8()
        else: raise ValueError(
            "Invalid format %s for attribute %s" % (
                field, fmt))
        return (r, g, b, a)
