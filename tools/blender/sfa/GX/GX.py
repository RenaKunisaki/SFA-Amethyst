# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
import logging; log = logging.getLogger(__name__)
from .Constants import GXConstants
import bmesh
import bpy
import bpy_extras
import os
import os.path

class GX(GXConstants):
    """GameCube GPU simulator.

    While nowhere near precise enough to be considered an
    emulator, this class functions roughly the same as the
    real GX chip - give it arrays containing display list
    and vertex attribute data, set up the registers telling
    how the data is formatted, and it renders an image.
    """

    MAX_TEXTURES = 8

    def __init__(self) -> None:
        super().__init__()
        self._materials = {} # ID => material
        self._textures  = {} # ID => texture

        # import here to avoid dependency loop
        from .CP import CP
        from .DlistParser import DlistParser

        self.cp = CP(self)
        self.dlistParser = DlistParser(self)
        self.reset()

    def reset(self):
        self.alphaComp0 = GX.Compare.GREATER
        self.alphaRef0  = 0
        self.alphaOp    = GX.AlphaOp.AND
        self.alphaComp1 = GX.Compare.GREATER
        self.alphaRef1  = 0
        # XXX verify these, most are guessed
        self.cullMode   = GX.CullMode.BACK
        self.blendMode  = GX.BlendMode.NONE
        self.srcFactor  = 0
        self.destFactor = 0
        self.logicOp    = GX.LogicOp.CLEAR
        self.compareEnable = True
        self.compareFunc   = GX.Compare.LESS
        self.updateEnable  = True
        self.useAlphaTest  = True

    def setShaderParams(self, cullMode, blendMode, sFactor, dFactor,
    logicOp, compareEnable, compareFunc, updateEnable, alphaTest):
        self.cullMode = cullMode
        self.setBlendMode(blendMode, sFactor, dFactor, logicOp)
        self.setZMode(compareEnable, compareFunc, updateEnable)
        self.setUseAlphaTest(alphaTest)

    def setBlendMode(self,
    blendMode:GX.BlendMode,
    srcFactor:GX.BlendFactor,
    destFactor:GX.BlendFactor,
    logicOp:GX.LogicOp):
        """Implement GC SDK's gxSetBlendMode().
        :param blendMode: blend mode.
        :param srcFactor: source blend factor.
        :param destFactor: destination blend factor.
        :param logicOp: how to blend.
        """
        self.blendMode  = blendMode
        self.srcFactor  = srcFactor
        self.destFactor = destFactor
        self.logicOp    = logicOp

    def setZMode(self,
    compareEnable:bool,
    compareFunc:GX.Compare,
    updateEnable:bool):
        """Implement GC SDK's gxSetZMode().
        :param compareEnable: Whether to use depth compare.
        :param compareFunc: Compare function to use.
        :param updateEnable: Whether to update Z buffer.
        """
        self.compareEnable = compareEnable
        self.compareFunc   = compareFunc
        self.updateEnable  = updateEnable

    def setAlphaCompare(self,
    comp0:GX.Compare, ref0:float, op:GX.AlphaOp,
    comp1:GX.Compare, ref1:float):
        self.alphaComp0 = comp0
        self.alphaRef0  = ref0 / 255.0
        self.alphaOp    = op
        self.alphaComp1 = comp1
        self.alphaRef1  = ref1 / 255.0

    def setCullMode(self, mode:GX.CullMode):
        self.cullMode = mode

    def setUseAlphaTest(self, enable:bool):
        self.useAlphaTest = enable


    def setTexturePath(self, path:str):
        """Set the path to load textures from."""
        self._texturePath = path
        log.debug("texture path = %r", path)


    def loadTexture(self, tId:int):
        """Load a game texture."""
        if tId not in self._textures:
            name = 'tex%04X' % tId
            texture = bpy.data.textures.new(name, 'IMAGE')
            texture.image = self._loadTextureImage(tId)
            self._textures[tId] = texture
        return self._textures[tId]


    def _loadTextureImage(self, tId:int):
        #if(id & 0x8000) then id & 0x7FFF is an index into TEX1.tab
        #else, if(id >= 3000) then id (not id - 3000) is an index into TEXPRE.tab
        #else, id is an index into TEX0.tab
        path = self._texturePath
        if tId & 0x8000:
            path = os.path.join(path, 'TEX1',
                '%04X.00.png' % (tId & 0x7FFF))
        elif tId >= 3000:
            path = os.path.join(path, '..', 'TEXPRE',
                '%04X.00.png' % tId)
        else:
            path = os.path.join(path, 'TEX0',
                '%04X.00.png' % tId)
        image = bpy.data.images.load(path, check_existing=True)
        image['id'] = tId
        return image


    def getMaterial(self, mId:str):
        """Get or create a material with the given ID."""
        if mId not in self._materials:
            mat = bpy.data.materials.new(
                "mat%d" % len(self._materials))
            self._materials[mId] = mat

        return self._materials[mId]
