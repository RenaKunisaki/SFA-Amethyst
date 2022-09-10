# this line allows methods in a class to be annotated with
# a return type of that class.
from __future__ import annotations
import numpy as np
import numpy.matlib
import bpy
import bmesh
from .BitStreamReader import BitStreamReader
from .RenderStreamParser import RenderStreamParser

class Parser:
    """Parses SFA models."""

    def __init__(self, gx) -> None:
        self.gx = gx

    def parse(self, model:dict) -> dict[str, bmesh]:
        """Parse the given model.

        :param model: Dict of model data/params.
        :returns: Parsed model data.
        """
        self.model  = model
        self.isMap  = model['isMap']
        self.file   = model['file']
        self.result = {}

        if self.isMap: streams = [
            'renderInstrsMain',
            'renderInstrsReflective',
            'renderInstrsWater',
        ]
        else: streams = ['renderInstrs']

        for sName in streams:
            mName = model['name']
            if sName == 'renderInstrsReflective':
                mName += '.reflective'
            elif sName == 'renderInstrsWater':
                mName += '.water'
            else: mName += '.main'
            self._resetMtxs()
            stream = model[sName]
            reader = BitStreamReader(stream)
            parser = RenderStreamParser(self.gx)
            ops = parser.execute(model, reader)
            mesh2 = self._doParsedOps(ops, mName)

            # Write the bmesh data back to a new mesh.
            if mesh2 is not None:
                mesh = bpy.data.meshes.new(mName+'.mesh')
                mesh2.to_mesh(mesh)
                mesh2.free()
                meshObj = bpy.data.objects.new(mName, mesh)
                mdata = meshObj.data
                bpy.context.collection.objects.link(meshObj)
                #self.parent._add_object_to_group(meshObj, mName)
                #mdata.materials.append(bpy.data.materials[mat.name])
                self.result[mName] = meshObj

        # model:
        #'isMap': True,
        #'header': header,
        #'file': file,
        #'path': path,
        #'name': name,
        #'object': bpy.data.objects.new(name, None),
        #'vertexPositions': file.reads32(header.nVtxs*6, header.vertexPositions),
        #'vertexColors': file.readu32(header.nColors*2, header.vertexColors),
        #'vertexTexCoords': file.reads32(header.nTexCoords*4, header.vertexTexCoords),
        #'renderInstrsMain': file.readu8(header.nRenderInstrsMain, header.renderInstrsMain),
        #'renderInstrsReflective': file.readu8(header.nRenderInstrsReflective, header.renderInstrsReflective),
        #'renderInstrsWater': file.readu8(header.nRenderInstrsWater, header.renderInstrsWater),
        #'textureIds': file.reads32(header.nTextures, header.textures),
        #'displayLists': [DisplayListPtr, header.displayLists, header.nDlists],
        #'GCpolygons': [GCPolygon, header.GCpolygons, header.nPolygons],
        #'polygonGroups': [PolygonGroup, header.polygonGroups, header.nPolyGroups],
        #'shaders': [Shader, header.shaders, header.nShaders],

        return self.result


    def _resetMtxs(self):
        self.mtxs = []
        for i in range(20):
            self.mtxs.append(np.matlib.identity(4))
            # XXX do something with these...

    def _doParsedOps(self, ops:list[list], streamName:str):
        mesh = self._createMesh(ops)
        for op in ops:
            opName = op[0]
            if opName == 'mtxs': self._doOpMatrix(op)
            elif opName == 'textures': self._doOpTextures(op)
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
        # 'textures'
        # 'mtxs'

    def _doOpMatrix(self, op):
        mtxs = op[0] # dict of id => mat4
        for idx, mtx in mtxs.items():
            # is there really no better way!?
            self.mtxs[idx] = np.array([
                [mtx[ 0], mtx[ 1], mtx[ 2], mtx[ 3]],
                [mtx[ 4], mtx[ 5], mtx[ 6], mtx[ 7]],
                [mtx[ 8], mtx[ 9], mtx[10], mtx[11]],
                [mtx[12], mtx[13], mtx[14], mtx[15]],
            ])

    def _doOpTextures(self, op):
        textures = op[0] # list of textures
        # or texture IDs (self.model.textures[n])
        # XXX do something

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
        for vtx in vtxs:
            pos = np.array([ # swap Y/Z and scale how the game does
                vtx['POS'][0] / 8,
                vtx['POS'][2] / 8,
                vtx['POS'][1] / 8,
            ])
            mesh.verts.new(pos)
        mesh.verts.ensure_lookup_table()
        mesh.verts.index_update()
        return mesh

    def _addFacesToMesh(self, mesh:bmesh, ops:list[list]):
        # iterate the draw ops to find which vertices are
        # part of which faces, and create those faces.
        def makeFace(vs):
            try:
                face = mesh.faces.new(list(
                    map(lambda v: mesh.verts[v['id']], vs)))
                # face.smooth = self.parent.operator.smooth_faces
            except ValueError: # face already exists
                pass
        for op in ops:
            if not op[0].startswith('draw'): continue
            opVtxs = op[2]
            if op[0] == 'drawQuads':
                for i in range(0, len(opVtxs), 4):
                    makeFace(opVtxs[i:i+4])

            elif op[0] == 'drawTris':
                for i in range(0, len(opVtxs), 3):
                    makeFace(opVtxs[i:i+3])

            elif op[0] == 'drawTriStrip':
                for i in range(2, len(opVtxs), 1):
                    makeFace(opVtxs[i-2:i+1])

            elif op[0] == 'drawTriFan':
                for i in range(2, len(opVtxs), 1):
                    makeFace([opVtxs[1], opVtxs[i-1], opVtxs[i]])

            elif op[0] == 'drawLines':
                for i in range(0, len(opVtxs), 2):
                    makeFace(opVtxs[i:i+2])

            elif op[0] == 'drawLineStrip':
                for i in range(1, len(opVtxs), 1):
                    makeFace(opVtxs[i-1:i])

            elif op[0] == 'drawPoints':
                for i in range(0, len(opVtxs), 1):
                    makeFace(opVtxs[i:i+1])



