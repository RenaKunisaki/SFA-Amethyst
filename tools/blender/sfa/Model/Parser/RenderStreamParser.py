# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from enum import IntEnum
from .BitStreamReader import BitStreamReader
from ...GX.GX import GX
from ...GX.CP import CP

DefaultCull = GX.CullMode.BACK
vatDefaults = [
    # these are set in videoInit() and almost never change
    { # VAT 0
        'POSCNT': 1, 'POSFMT': 3, 'POSSHFT':  0, # s16
        'COL0CNT':1, 'COL0FMT':5, 'COL0SHFT': 0, # rgba8888
        'TEX0CNT':1, 'TEX0FMT':3, 'TEX0SHFT': 7, # s16
    },
    { # VAT 1
        'POSCNT': 1, 'POSFMT': 3, 'POSSHFT':  2, # s16
        'COL0CNT':1, 'COL0FMT':5, 'COL0SHFT': 0, # rgba8888
        'TEX0CNT':1, 'TEX0FMT':4, 'TEX0SHFT': 0, # float
    },
    { # VAT 2
        'POSCNT': 1, 'POSFMT': 4, 'POSSHFT':  0, # float
        'NRMCNT': 0, 'NRMFMT': 4, 'NRMSHFT':  0, # float
        'COL0CNT':1, 'COL0FMT':5, 'COL0SHFT': 0, # rgba8888
        'TEX0CNT':1, 'TEX0FMT':4, 'TEX0SHFT': 0, # float
        'TEX1CNT':1, 'TEX1FMT':4, 'TEX1SHFT': 0, # float
    },
    { # VAT 3
        'POSCNT': 1, 'POSFMT': 3, 'POSSHFT':  8, #  s16
        'NRM3CNT':1, 'NRM3FMT':1, 'NRM3SHFT': 0, #  s8
        'COL0CNT':1, 'COL0FMT':3, 'COL0SHFT': 0, #  rgba4444
        'TEX0CNT':1, 'TEX0FMT':3, 'TEX0SHFT':10, #  s16
        'TEX1CNT':1, 'TEX1FMT':3, 'TEX1SHFT':10, #  s16
        'TEX2CNT':1, 'TEX2FMT':3, 'TEX2SHFT':10, #  s16
        'TEX3CNT':1, 'TEX3FMT':3, 'TEX3SHFT':10, #  s16
    },
    { # VAT 4
        'POSCNT': 1, 'POSFMT': 4, 'POSSHFT':  0, # float
        'COL0CNT':1, 'COL0FMT':5, 'COL0SHFT': 0, # rgba8888
        'TEX0CNT':1, 'TEX0FMT':3, 'TEX0SHFT': 7, # s16
        'NRMCNT': 0, 'NRMFMT': 4, 'NRMSHFT':  0, # float
    },
    { # VAT 5 (map blocks)
        'POSCNT': 1, 'POSFMT': 3, 'POSSHFT':  3, # s16
        'NRMCNT': 0, 'NRMFMT': 1, 'NRMSHFT':  0, # s8
        'COL0CNT':1, 'COL0FMT':3, 'COL0SHFT': 0, # rgba4444
        'TEX0CNT':1, 'TEX0FMT':3, 'TEX0SHFT': 8, # s16
        'TEX1CNT':1, 'TEX1FMT':3, 'TEX1SHFT': 8, # s16
        'TEX2CNT':1, 'TEX2FMT':3, 'TEX2SHFT': 8, # s16
        'TEX3CNT':1, 'TEX3FMT':3, 'TEX3SHFT': 8, # s16
    },
    { # VAT 6 (character models)
        'POSCNT': 1, 'POSFMT': 3, 'POSSHFT':  8, # s16
        'NRMCNT': 0, 'NRMFMT': 1, 'NRMSHFT':  0, # s8
        'COL0CNT':1, 'COL0FMT':3, 'COL0SHFT': 0, # rgba4444
        'TEX0CNT':1, 'TEX0FMT':3, 'TEX0SHFT':10, # s16
        'TEX1CNT':1, 'TEX1FMT':3, 'TEX1SHFT':10, # s16
        'TEX2CNT':1, 'TEX2FMT':3, 'TEX2SHFT':10, # s16
        'TEX3CNT':1, 'TEX3FMT':3, 'TEX3SHFT':10, # s16
    },
    { # VAT 7
        'POSCNT': 1, 'POSFMT': 3, 'POSSHFT':  0, # s16
        'NRMCNT': 0, 'NRMFMT': 1, 'NRMSHFT':  0, # s8
        'COL0CNT':1, 'COL0FMT':3, 'COL0SHFT': 0, # rgba4444
        'TEX0CNT':1, 'TEX0FMT':3, 'TEX0SHFT':10, # s16
        'TEX1CNT':1, 'TEX1FMT':3, 'TEX1SHFT':10, # s16
        'TEX2CNT':1, 'TEX2FMT':3, 'TEX2SHFT':10, # s16
        'TEX3CNT':1, 'TEX3FMT':3, 'TEX3SHFT':10, # s16
    },
]

class ShaderFlags(IntEnum):
    Hidden             = (1<< 1) # invisible, exploded walls, etc
    Fog                = (1<< 2) # enable fog
    CullBackface       = (1<< 3)
    ReflectSkyscape    = (1<< 5)
    Caustic            = (1<< 6)
    Lava               = (1<< 7)
    Reflective         = (1<< 8) # Occurs on Krazoa Palace reflective floors
    FuzzRelated        = (1<< 9)
    AlphaCompare       = (1<<10)
    TranspRelated2000  = (1<<13)
    ShortFur           = (1<<14) # 4 layers
    MediumFur          = (1<<15) # 8 layers
    LongFur            = (1<<16) # 16 layers
    StreamingVideo     = (1<<17) # Occurs on video panels in Great Fox. Used to display preview video.
    IndoorOutdoorBlend = (1<<18) # Occurs near cave entrances and windows. Requires special handling for lighting.
    BlendFlag29        = (1<<29)
    ForceBlend         = (1<<30)
    Water              = (1<<31)

class RenderStreamParser:
    """Parses and executes the bit-packed render
    opcode streams from map blocks and character
    models.
    """
    def __init__(self, gx) -> None:
        self.gx = gx

    def execute(self, model:dict, reader:BitStreamReader, params={}):
        """ Execute the instructions in the stream.
        :param model: The model to render.
        :param reader: Stream to read from.
        :param params: Additional render parameters.
        """
        self.model  = model
        self.reader = reader
        self.params = params
        self.isMap  = model['isMap'] # is map block or character model?
        self.VAT    = 5 if self.isMap else 6

        # current render state
        self.shader    = None
        self.shaderIdx = None
        self.result    = []
        self._setInitialGxParams()

        done = False
        while (not done) and (not self.reader.isEof()):
            op = self.reader.read(4)
            if   op == 1: self._renderOpTexture()
            elif op == 2: self._renderOpCallList()
            elif op == 3: self._renderOpSetVtxFmt()
            # 0 is unused, but does the same as 4
            elif op == 4 or op == 0: self._renderOpMatrix()
            elif op == 5: done = True
            else: raise ValueError("Unknown render op %d at bit 0x%X" % (
                op, self.reader.offset - 4))

        # do this or else everything breaks for some reason
        #self.batch.addFunction(() => {
        #    self.gx.setShaderParams(
        #        DefaultCull, # cull mode
        #        GX.BlendMode.NONE, # blend mode
        #        GX.BlendFactor.ONE, # sFactor
        #        GX.BlendFactor.ZERO, # dFactor
        #        GX.LogicOp.NOOP, # logicOp
        #        true, # compareEnable
        #        GX.Compare.LEQUAL, # compareFunc
        #        true, # updateEnable
        #        true, # alphaTest
        #    )
        #    self.gx.sync()
        #})

        return self.result

    def _setInitialGxParams(self):
        #self.gx.xf.reset()
        #self.gx.syncXF()

        # set default vtx formats for rendering model geometry
        self.gx.cp.setReg(CP.Reg.ARRAY_STRIDE_VTXS,   6) # sizeof(vec3s)
        self.gx.cp.setReg(CP.Reg.ARRAY_STRIDE_NORMALS,6) # sizeof(vec3s)
        self.gx.cp.setReg(CP.Reg.ARRAY_STRIDE_COLOR,  2) # sizeof(u16)
        for i in range(8):
            self.gx.cp.setReg(CP.Reg.ARRAY_STRIDE_TEXCOORD+i, 4) # sizeof(vec2s)
            self.gx.cp.setVatFormat(i, vatDefaults[i])

        # set initial render modes (XXX verify)
        self.gx.setShaderParams(
            DefaultCull, # cull backfaces
            GX.BlendMode.BLEND, GX.BlendFactor.SRCALPHA,
            GX.BlendFactor.INVSRCALPHA, GX.LogicOp.NOOP,
            True, GX.Compare.LEQUAL, True, # depth test+update enabled
            True) # alpha test enabled
        self.gx.setAlphaCompare(GX.Compare.GREATER, 0,
                GX.AlphaOp.AND, GX.Compare.GREATER, 0)


    def _handleShaderFlags(self):
        gx    = self.gx
        flags = self.shader.flags

        blendMode         = GX.BlendMode.NONE
        sFactor           = GX.BlendFactor.ONE
        dFactor           = GX.BlendFactor.ZERO
        logicOp           = GX.LogicOp.NOOP
        compareEnable     = True
        compareFunc       = GX.Compare.LEQUAL
        updateEnable      = True
        zCompLoc          = 1 # before tex
        alphaCompareA0    = 0
        alphaCompareA1    = 0
        alphaCompareOP0   = GX.Compare.GREATER
        alphaCompareOP1   = GX.Compare.GREATER
        alphaCompareLogic = GX.AlphaOp.AND

        chan0_enable     = True
        chan0_amb_src    = GX.ColorSrc.SRC_REG
        chan0_mat_src    = GX.ColorSrc.SRC_VTX
        chan0_light_mask = GX.LightID.LIGHT_NULL
        chan0_diff_fn    = GX.DiffuseFn.NONE
        chan0_attn_fn    = GX.AttnFn.NONE

        if flags & ShaderFlags.Fog == 0:
            pass # gx.setFog(0, 0, 0, 0, 0, fogColor2)
        else:
            pass # _gxSetDefaultFog
            # gx.setFog(fogStartZ,fogEndZ,fogNearZ,fogFarZ,4,fogColor)

        if (flags & ShaderFlags.Water | ShaderFlags.StreamingVideo) == 0:
            if flags & ShaderFlags.Lava == 0:
                pass # shaderFn_8005f1e0(shader, 0x80)
            # else shaderFn_8004da54(shader)

        if (flags & ShaderFlags.ReflectSkyscape) == 0: # or pSkyTexture == NULL
            if (flags & ShaderFlags.Caustic) == 0:
                pass # if(isHeavyFogEnabled()) {
                    # renderHeavyFog(getFogColor())
                # }
            else:
                pass # drawWaterSurface()
        else:
            pass # drawSkyReflection(pSkyTexture,skyMtx)


        if ((flags & ShaderFlags.ForceBlend) == 0
        and ((flags & 0x20000000) == 0)):
            if (((flags & ShaderFlags.AlphaCompare) == 0)
            or ((flags & ShaderFlags.Lava) != 0)):
                # GXSetAlphaCompare(7,0,0,7,0)
                alphaCompareOP0   = GX.Compare.ALWAYS
                alphaCompareA0    = 0
                alphaCompareLogic = GX.AlphaOp.AND
                alphaCompareOP1   = GX.Compare.ALWAYS
                alphaCompareA1    = 0
            else:
                zCompLoc        = 0 # after tex
                # GXSetAlphaCompare(4,0,0,4,0)
                alphaCompareOP0   = GX.Compare.GREATER
                alphaCompareA0    = 0
                alphaCompareLogic = GX.AlphaOp.AND
                alphaCompareOP1   = GX.Compare.GREATER
                alphaCompareA1    = 0
        else:
            # GXSetAlphaCompare(7,0,0,7,0)
            alphaCompareOP0   = GX.Compare.ALWAYS
            alphaCompareA0    = 0
            alphaCompareLogic = GX.AlphaOp.AND
            alphaCompareOP1   = GX.Compare.ALWAYS
            alphaCompareA1    = 0
            blendMode    = GX.BlendMode.BLEND
            sFactor      = GX.BlendFactor.SRCALPHA
            dFactor      = GX.BlendFactor.INVSRCALPHA
            updateEnable = False

        if (flags & (ShaderFlags.IndoorOutdoorBlend | 1 | 0x800 | 0x1000)) == 0:
            pass
            # objGetColor(0,&local_18.r,&local_18.g,&local_18.b)
            # GXSetChanCtrl(0,1,0,1,0,0,2)
            # gx.setChanCtrl... all default params
            # local_28 = local_18
            # gx.setChanAmbColor(Channel0_RGB,&local_28)
        else:
            # gx.setChanAmbColor(Channel0_RGB,color_803db63c)
            chan0_enable     = not (flags & ShaderFlags.IndoorOutdoorBlend)
            chan0_amb_src    = GX.ColorSrc.REG
            chan0_mat_src    = GX.ColorSrc.VTX
            chan0_light_mask = GX.LightID.NULL
            chan0_diff_fn    = GX.DiffuseFn.NONE
            chan0_attn_fn    = GX.AttnFn.NONE

        # chan0 stuff relates to lighting, not worried about it right now...

        cull = GX.CullMode.BACK if \
            flags & ShaderFlags.CullBackface else GX.CullMode.NONE

        self.gx.setShaderParams(cull, blendMode, sFactor, dFactor,
            logicOp, compareEnable, compareFunc, updateEnable,
            alphaCompareOP0 != GX.Compare.ALWAYS)
            # this seems unnecessary. we should be able to
            # just leave the alpha compare enabled.
        self.gx.setAlphaCompare(alphaCompareOP0, alphaCompareA0,
            alphaCompareLogic, alphaCompareOP1, alphaCompareA1)

    def _renderOpTexture(self):
        """Select a texture and shader.
        This can affect how later commands are interpreted.
        """
        gx  = self.gx
        ops = self.reader
        idx = ops.read(6)
        if self.params.get('isGrass', False): return
        if self.shaderIdx == idx: return

        self.shader = self.model['shaders'][idx]
        self.shaderIdx = idx
        if self.shader is not None: self._handleShaderFlags()
        else:
            self.gx.setShaderParams(
                DefaultCull, # cull backfaces
                GX.BlendMode.NONE, # blend mode
                GX.BlendFactor.ONE, # sFactor
                GX.BlendFactor.ZERO, # dFactor
                GX.LogicOp.NOOP, # logicOp
                True, # compareEnable
                GX.Compare.LEQUAL, # compareFunc
                True, # updateEnable
                True, # alphaTest
            )
            #XXX this must be a flag on the texture or something
            gx.setAlphaCompare(GX.Compare.GREATER, 0,
                GX.AlphaOp.AND, GX.Compare.GREATER, 0)

        nLayers = 0 if (self.shader is None) else self.shader.nLayers
        textures = []
        for i in range(GX.MAX_TEXTURES):
            tex = None
            if i < nLayers:
                idx = self.shader.layer[i].texture
                if idx >= 0 and idx in self.model['textureIds']:
                    tex = self.model['textureIds'][idx]
            textures.append((i, tex))

        self.result.append(['textures', textures])


    def _renderOpCallList(self):
        """Call one of the model's display lists."""
        ops = self.reader
        idx = ops.read(8)
        if idx >= len(self.model['displayLists']):
            raise ValueError("Calling list %d but max is %d" % (
                idx, len(self.model['displayLists'])))

        dlistData = {
            'POS':  self.model['vertexPositions'],
            'NRM':  None if self.isMap else self.model['vertexNormals'],
            'COL0': self.model['vertexColors'],
            'TEX0': self.model['vertexTexCoords'],
            'TEX1': self.model['vertexTexCoords'],
            'TEX2': self.model['vertexTexCoords'],
            'TEX3': self.model['vertexTexCoords'],
            'TEX4': self.model['vertexTexCoords'],
            'TEX5': self.model['vertexTexCoords'],
            'TEX6': self.model['vertexTexCoords'],
            'TEX7': self.model['vertexTexCoords'],
        }

        dlist = self.model['displayLists'][idx]
        self.model['file'].seek(dlist.list)
        instrs = self.model['file'].read(dlist.size)
        self.result += self.gx.dlistParser.parse(instrs, dlistData)


    def _renderOpSetVtxFmt(self):
        """Change the vertex data format."""
        ops = self.reader
        sizes = {
            'PMTX': 0,
            'TMTX': [0,0,0,0,0,0,0,0],
            'POS':  0,
            'NRM':  0,
            'COL':  [0,0],
            'TEX':  [0,0,0,0,0,0,0,0],
        }
        triNrm = False
        aFlags = 0 if self.shader is None else self.shader.attrFlags

        if self.isMap or self.model['header'].nBones < 2:
            pass # GXSetCurrentMtx(0);
        else:
            sizes['PMTX'] = GX.AttrType.DIRECT
            which = 0 # T0MIDX
            # texture, lighting => auxTex0, auxTex1
            # Shader vs ShaderDef, it's confusing...
            if self.shader and (
            self.shader.auxTex0 >= 0 or
            self.shader.auxTex1 >= 0):
                which_00 = which
                if self.shader.auxTex2 >= 0:
                    # If the material has textures, we have
                    # texcoord matrices 0,1
                    sizes['TMTX'][0] = GX.AttrType.DIRECT
                    which_00 = 2 # T2MIDX
                    sizes['TMTX'][1] = GX.AttrType.DIRECT
                which_00 += 1
                sizes['TMTX'][which_00] = GX.AttrType.DIRECT

            texN2 = 7 # T7MIDX
            flags = 0 # 1:NoFog, 2:EXTRA_FUZZY, 4:DrawFuzz, 8:ForceFuzz

            nTextureMtxs_803dcc5c = 0
            for idx in range(self.model['header'].nTexMtxs):
                if (((flags & 0xff) == 4) and (idx == 0)):
                    #if((nTextureMtxs_803dcc5c == 0) ||
                    #(FUN_8001d7f8(PTR_803dcc64,local_38,auStack52), local_38 != 0)) {
                    #    enable = false;
                    #}
                    #else {
                    #    enable = true;
                    #}
                    enable = False
                elif (idx < nTextureMtxs_803dcc5c) and ((flags & 0xff) == 0):
                    enable = True
                else: enable = False

                if enable:
                    sizes['TMTX'][which] = GX.AttrType.DIRECT
                    next = texN2
                    which = which + 1
                else:
                    next = texN2 - 1
                    sizes['TMTX'][texN2] = GX.AttrType.DIRECT
                texN2 = next
        sizes['POS'] = GX.AttrType.INDEX16 if ops.read(1) else \
            GX.AttrType.INDEX8

        if (aFlags & 1) and not self.isMap:
            sizes['NRM'] = GX.AttrType.INDEX16 if ops.read(1) \
                else GX.AttrType.INDEX8
        if aFlags & 2:
            sizes['COL'][0] = GX.AttrType.INDEX16 if ops.read(1) \
                else GX.AttrType.INDEX8
        else: sizes['COL'][0] = 0

        texSize = GX.AttrType.INDEX16 if ops.read(1) \
            else GX.AttrType.INDEX8
        if self.params.get('isGrass', False): return

        if self.shader:
            for i in range(self.shader.nLayers):
                sizes['TEX'][i] = texSize
        else: sizes['TEX'][0] = texSize

        vcdHi = 0
        vcdLo = ((sizes['POS'] << 9) | (sizes['NRM'] << 11) |
            (sizes['COL'][0] << 13) | (sizes['COL'][1] << 15))
        if sizes['PMTX']: vcdLo |= (1 << 0)
        for i in range(8):
            if sizes['TMTX'][i]: vcdLo |= (1 << (i+1))
            vcdHi |= sizes['TEX'][i] << (i*2)

        self.gx.cp.setReg(0x50 | self.VAT, vcdLo) # VCD FMT LO
        self.gx.cp.setReg(0x60 | self.VAT, vcdHi) # VCD FMT HI

        r70 = self.gx.cp.getReg(0x70 | self.VAT)
        if triNrm: r70 |= (1 << 31)
        else: r70 &= ~(1 << 31)
        self.gx.cp.setReg(0x70 | self.VAT, r70) # VCD FMT A


    def _renderOpMatrix(self):
        """Load one of the model's matrices into GX XF registers."""
        mtxs = {}
        idxs = []
        count = self.reader.read(4)

        # following data is indices into the model's matrix list.
        for i in range(count):
            idxs.append(self.reader.read(8))

        # for map blocks the game reads the indices but
        # doesn't do anything with them.
        if self.isMap: return

        tbl = ( #not sure why the game does this
             0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 0, 0,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 0)

        nMax = (self.model['header'].nVtxGroups +
            self.model['header'].nBones)

        for i in range(count):
            iMtx = idxs[i]
            assert iMtx < nMax

            # we only store the translation vector, not the
            # full transformation matrix.
            xl = self.model['xlates'][iMtx]
            mtxs[tbl[i]*3] = ( # mat4
                1, 0, 0, 0,  0, 1, 0, 0,  0, 0, 1, 0,
                xl[0], xl[1], xl[2], 1)

        self.result.append(['mtxs', mtxs])
