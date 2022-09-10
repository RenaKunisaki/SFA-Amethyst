# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from .Constants import GXConstants

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

