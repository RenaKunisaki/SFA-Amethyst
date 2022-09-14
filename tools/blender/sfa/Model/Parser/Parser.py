# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
from ctypes import Union
import logging; log = logging.getLogger(__name__)
import numpy as np
import numpy.matlib
import bpy
import bmesh
from .BitStreamReader import BitStreamReader
from .RenderStreamParser import RenderStreamParser
from ..Model import Model
from ..MapBlock import MapBlock

MAP_CELL_SIZE = 640

class Parser:
    """Parses SFA models and creates meshes for them."""

    SCALE = 1/1
    """Amount to scale models by."""

    def __init__(self, gx) -> None:
        self.gx = gx

    def parse(self, model:Model) -> dict[str, bmesh]:
        """Parse the given model.

        :param model: Model to parse.
        :returns: Parsed model data.
        """
        self.model  = model
        self.isMap  = isinstance(model, MapBlock)
        self.file   = model.file
        self.result = {}

        #col = bpy.data.collections.get(model.name, None)
        #if col is None:
        #    col = bpy.data.collections.new(model.name)
        #    bpy.context.scene.collection.children.link(col)

        # create an Empty as the parent
        if self.isMap: empty = self._createEmptyForMapBlock()
        # XXX else
        bpy.context.scene.collection.objects.link(empty)

        for sName, sDisp in model.RenderStreamOrder.items():
            mName = model.name + sDisp
            self._resetMtxs()
            self.uvMaps = {}
            stream = model.renderStreams[sName]
            reader = BitStreamReader(stream)
            parser = RenderStreamParser(self.gx)
            ops    = parser.execute(model, reader)
            mesh2  = self._doParsedOps(ops, mName)

            # Write the bmesh data back to a new mesh.
            if mesh2 is not None:
                log.debug("Creating mesh %r", mName)
                mesh = bpy.data.meshes.new(mName+'.mesh')
                mesh2.to_mesh(mesh)
                mesh2.free()
                meshObj = bpy.data.objects.new(mName, mesh)
                mdata = meshObj.data
                bpy.context.scene.collection.objects.link(meshObj)

                # add the new object to a collection.
                #if meshObj.name not in col.objects:
                #    col.objects.link(meshObj)
                # rather, set it as child of the empty
                meshObj.parent = empty

                self._setUvMaps(mdata)

                for shader in model.shaders:
                    mdata.materials.append(shader.mat)
                self.result[mName] = meshObj

        return self.result


    def _createEmptyForMapBlock(self):
        x = (self.model.xOffset-0.5) * MAP_CELL_SIZE / 8
        y = (self.model.zOffset-0.5) * MAP_CELL_SIZE / 8
        z = self.model.header.yOffset / 8 # swap Y/Z
        #x += (MAP_CELL_SIZE / 2) / 8
        #y += (MAP_CELL_SIZE / 2) / 8
        #z += ((self.model.header.yMax - self.model.header.yMin) / 2) / 8
        empty = bpy.data.objects.new(self.model.name, None)
        empty.location=(x*self.SCALE, -y*self.SCALE, z*self.SCALE)
        empty.empty_display_type = 'CUBE'
        empty.empty_display_size = (MAP_CELL_SIZE/2) / 8 * self.SCALE
        return empty


    def _resetMtxs(self):
        self.mtxs = []
        for i in range(20):
            self.mtxs.append(np.matlib.identity(4))
            # XXX do something with these...

    def _doParsedOps(self, ops:list[list], streamName:str):
        mesh = self._createMesh(ops)
        for op in ops:
            opName = op[0]
            if   opName == 'mtxs':   self._doOpMatrix(op, mesh)
            elif opName == 'shader': self._doOpShader(op, mesh)
            else: # draw
                pass
        self._addFacesToMesh(mesh, ops)
        return mesh
        # ops are:
        # 'drawQuads'
        # 'drawTris'
        # 'drawTriStrip'
        # 'drawTriFan'
        # 'drawLines'
        # 'drawLineStrip'
        # 'drawPoints'
        # 'shader'
        # 'mtxs'

    def _doOpMatrix(self, op, mesh):
        mtxs = op[0] # dict of id => mat4
        for idx, mtx in mtxs.items():
            # is there really no better way!?
            self.mtxs[idx] = np.array([
                [mtx[ 0], mtx[ 1], mtx[ 2], mtx[ 3]],
                [mtx[ 4], mtx[ 5], mtx[ 6], mtx[ 7]],
                [mtx[ 8], mtx[ 9], mtx[10], mtx[11]],
                [mtx[12], mtx[13], mtx[14], mtx[15]],
            ])

    def _doOpShader(self, op, mesh):
        shader, shaderIdx = op[0], op[1]
        #mesh.materials.append(shader.mat)
        # nothing to do here. this is handled by
        # _addFacesToMesh.

    def _createMesh(self, ops:list[list]) -> bmesh:
        mesh = bmesh.new()

        # iterate the draw ops and extract all vertices.
        # keep them in order but avoid duplicating them.
        # add them to the mesh.
        vtxs = []
        vIds = {}
        fields = ('POS', 'COL0', 'TEX0', 'TEX1', 'TEX2',
            'TEX3', 'TEX4', 'TEX5', 'TEX6', 'TEX7')
        for op in ops:
            if not op[0].startswith('draw'): continue
            opVtxs = op[2] # [op, vat, vtxs]
            for i, vtx in enumerate(opVtxs):
                # make unique ID to avoid duplicates
                # but keep them in order
                vId = []
                for field in fields:
                    val = vtx.get(field, None)
                    if type(val) is list:
                        val = ','.join(map(str, val))
                    vId.append(str(val))
                vId = ' '.join(vId)
                if vId not in vIds:
                    vIds[vId] = len(vtxs)
                    vtxs.append(vtx)
                # save the vtx IDs; we need them later to create
                # faces between them.
                opVtxs[i]['id'] = vIds[vId]
        if len(vtxs) == 0:
            mesh.free()
            return None

        offs = [0,0,0]
        if self.isMap:
            # the game scales vtxs by 1/8; this is independent
            # of the global scaling factor we set above
            offs = [
                (-MAP_CELL_SIZE/2) / 8,
                0,
                (-MAP_CELL_SIZE/2) / 8,
            ]

        #self.vtxsByIdx = vtxs
        for vtx in vtxs:
            pos = np.array([
                vtx['POS'][0]/8, vtx['POS'][1]/8,
                vtx['POS'][2]/8, 1 ])
            mtx = self.mtxs[vtx['PNMTXIDX']]
            pos = pos @ mtx
            # Blender has Y/Z swapped compared to game
            # and uses CCW winding order while game uses
            # CW. Correct this by swapping, inverting Y,
            # and reversing the order of vertices in each
            # face (in _addFacesToMesh).
            mesh.verts.new([ # swap Y/Z for Blender
                (pos.item(0) + offs[0]) *  self.SCALE,
                (pos.item(2) + offs[2]) * -self.SCALE,
                (pos.item(1) + offs[1]) *  self.SCALE,
            ])
            #log.debug("V %r", vtx)
        mesh.verts.ensure_lookup_table()
        mesh.verts.index_update()
        return mesh

    def _addFacesToMesh(self, mesh:bmesh, ops:list[list]):
        # iterate the draw ops to find which vertices are
        # part of which faces, and create those faces.
        shaderIdx = None
        for i in range(self.gx.MAX_TEXTURES):
            self.uvMaps['TEX'+str(i)] = {}

        def makeFace(vs):
            try:
                # reverse because of opposite winding order
                face = mesh.faces.new(reversed(list(
                    map(lambda v: mesh.verts[v['id']], vs))))
                #face.normal_flip()
                #face.normal_update()
            except ValueError: # face already exists
                return
            if shaderIdx is not None:
                face.material_index = shaderIdx
            # face.smooth = self.parent.operator.smooth_faces
            for vtx in vs:
                for i in range(self.gx.MAX_TEXTURES):
                    tex = vtx.get('TEX'+str(i), None)
                    if tex is not None:
                        self.uvMaps['TEX'+str(i)][vtx['id']] = tex

        for op in ops:
            if op[0] == 'shader':
                shaderIdx = op[2]
            if not op[0].startswith('draw'): continue
            opVtxs = op[2]
            if op[0] == 'drawQuads':
                for i in range(0, len(opVtxs), 4):
                    makeFace(opVtxs[i:i+4])

            elif op[0] == 'drawTris':
                for i in range(0, len(opVtxs), 3):
                    makeFace(opVtxs[i:i+3])

            elif op[0] == 'drawTriStrip':
                a, b = opVtxs[0], opVtxs[1]
                which = False
                for i in range(2, len(opVtxs), 1):
                    c = opVtxs[i]
                    #makeFace(opVtxs[i-2:i+1])
                    makeFace([a, b, c])
                    if which: b = c
                    else: a = c
                    which = not which

            elif op[0] == 'drawTriFan':
                a, b = opVtxs[0], opVtxs[1]
                for i in range(2, len(opVtxs), 1):
                    c = opVtxs[i]
                    makeFace([a, b, c])
                    b = c

            elif op[0] == 'drawLines':
                for i in range(0, len(opVtxs), 2):
                    makeFace(opVtxs[i:i+2])

            elif op[0] == 'drawLineStrip':
                for i in range(1, len(opVtxs), 1):
                    makeFace(opVtxs[i-1:i])

            elif op[0] == 'drawPoints':
                for i in range(0, len(opVtxs), 1):
                    makeFace(opVtxs[i:i+1])

    def _setUvMaps(self, mdata):
        # assign UV maps
        for i in range(self.gx.MAX_TEXTURES):
            uv = self.uvMaps['TEX'+str(i)]
            if len(uv) > 0:
                mdata.uv_layers.new(name='TEX'+str(i))
                for _, poly in enumerate(mdata.polygons):
                    for loopIdx in poly.loop_indices:
                        loop = mdata.loops[loopIdx]
                        uvloop = mdata.uv_layers.active.data[loopIdx]
                        # since we inverted the Y axis for geometry
                        # we need to also invert it for texcoord.
                        #vtx = self.vtxsByIdx[loop.vertex_index]
                        #x, y = uv[vtx['id']]
                        try:
                            x, y = uv[loop.vertex_index]
                            uvloop.uv.x, uvloop.uv.y = x, 1-y
                        except KeyError: pass
