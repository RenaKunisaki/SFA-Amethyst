# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
import logging; log = logging.getLogger(__name__)
import bmesh
import bpy
import bpy_extras
from ..Model import Model

from ctypes import (BigEndianStructure, sizeof,
    c_byte   as s8,
    c_ubyte  as u8,
    c_int16  as s16,
    c_uint16 as u16,
    c_int32  as s32,
    c_uint32 as u32,
    c_float  as f32, # name "float" is already used
    c_double as f64)


class ShaderLayer(BigEndianStructure):
    """One layer of a shader in the game file."""
    _fields_ = [
        # texture is s32 because the game converts it to a pointer on load
        ('texture',             s32), # idx into model's texture list (-1=none)
        ('tevMode',             u8),
        ('enableTexChainStuff', u8),
        ('scrollingTexMtx',     u8),
        ('unk07',               u8), # probably padding
    ]


class ShaderData(BigEndianStructure):
    """Shader data in the game file."""
    _fields_ = [
        ('unk00',      u8),
        ('unk01',      u8),
        ('unk02',      u8),
        ('unk03',      u8),
        ('r',          u8), # likely wrong
        ('g',          u8),
        ('b',          u8),
        ('unk07',      u8),
        ('auxTex0',    s32),
        ('alpha',      u8),
        ('unk0D',      u8),
        ('unk0E',      u8),
        ('unk0F',      u8),
        ('unk10',      u32),
        ('auxTex1',    s32),
        ('texture18',  s32),
        ('unk1C',      s32), # -1 -> 0, -2 -> 0, else -> 1
        ('unk20',      u32), # pointer
        ('layer',      ShaderLayer*2),
        ('auxTex2',    s32),
        ('furTexture', s32),
        ('flags',      u32), # ShaderFlags
        ('attrFlags',  u8), # ShaderAttrFlags
        ('nLayers',    s8),
        ('_pad42',     u8*2),
    ]


class Shader:
    """A shader from one of the game's models.

    Could also be called a material.
    """

    def __init__(self, model:Model):
        self.model = model
        self.gx    = model.gx

    def readFromFile(self, file) -> Shader:
        data = ShaderData.from_buffer_copy(
            file.read(sizeof(ShaderData)))
        self.data      = data
        self.file      = file
        self.flags     = data.flags
        self.attrFlags = data.attrFlags
        self.nLayers   = data.nLayers
        self.layer     = data.layer

        self.id   = self._makeId()
        self.mat  = self.gx.getMaterial(self.id)

        self._loadTexture(data.auxTex0)
        self._loadTexture(data.auxTex1)
        self._loadTexture(data.auxTex2)
        self._loadTexture(data.texture18)
        self._loadTexture(data.furTexture)
        for iLayer in range(self.nLayers):
            layer = self.layer[iLayer]
            texObj = self._loadTexture(layer.texture)
            if texObj is not None:
                self.mat.use_nodes = True
                #material_output = self.mat.node_tree.nodes.get('Material Output')
                principled_BSDF = self.mat.node_tree.nodes.get('Principled BSDF')

                tex_node = self.mat.node_tree.nodes.new('ShaderNodeTexImage')
                tex_node.image = texObj.image

                links = self.mat.node_tree.links
                links.new(
                    tex_node.outputs['Color'],
                    principled_BSDF.inputs['Base Color'])
                links.new(tex_node.outputs['Alpha'],
                    principled_BSDF.inputs['Alpha'])

        if self.data.flags & (0x40000000 | 0x80000000):
            self.mat.blend_method = 'BLEND'
        elif self.data.flags & 0x400:
            self.mat.blend_method = 'CLIP'
        self.mat.use_backface_culling = (self.data.flags & 0x8) != 0
        return self


    def _makeId(self):
        """Generate a unique ID to avoid creating a ton of duplicate
        shaders/materials when importing a map.
        """
        fields = []
        for field in self.data._fields_:
            name, tp = field
            if name  == 'layer':
                for layer in self.data.layer:
                    for f2 in layer._fields_:
                        n2, t2 = f2
                        v2 = getattr(layer, n2)
                        fields.append(str(v2))
            else:
                val = getattr(self.data, name)
                fields.append(str(val))
        return ' '.join(fields)


    def _loadTexture(self, texIdx:int):
        """Load a texture.

        :param texIdx: The index into the model's texture list.
        :returns: The Blender texture object.
        """
        if texIdx < 0: return # no texture
        try:
            texId = self.model.textureIds[texIdx]
        except IndexError:
            log.error("Texture index %r not found in model %r",
                texIdx, self.model)
            return None
        return self.gx.loadTexture(texId)

