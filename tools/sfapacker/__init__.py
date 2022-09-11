#!/usr/bin/env python3
"""Pack and unpack assets from SFA."""
import os
import os.path
import sys
import xml.etree.ElementTree as ET

# what the fuck
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sfapacker.Asset import Asset
from sfapacker.Asset.Texture import Texture, TextureFrame, Header
from sfapacker.Game import Game
from sfapacker.BinaryFile import BinaryFile
from sfapacker.Asset.Texture.GX import GX

class App:
    def __init__(self, rootDir:str) -> None:
        self.game = Game(rootDir)


    def unpack(self, inPath:str, outPath:str) -> None:
        """Unpack assets from specified file to specified directory."""

        # get the file's name without extension
        path, name = os.path.split(inPath)
        name, ext  = name.split('.', maxsplit=1)

        # which type of file is this?
        nameFuncs = {
            #'AMAP':         self._unpackAnimMap,
            #'ANIM':         self._unpackAnimations,
            #'ANIMCURV':     self._unpackAnimCurves,
            # no need to modify BITTABLE
            #'CAMACTIO':     self._unpackCamActions,
            #'ENVFXACT':     self._unpackEnvFx,
            #'ENVFXACTIONS': self._unpackEnvFx,
            #'HITS':         self._unpackHits,
            #'MAPINFO':      self._unpackMapInfo,
            #'MAPS':         self._unpackMapsBin,
            #'MODANIM':      self._unpackModAnim,
            'MODELS':       self._unpackModels,
            #'globalma':     self._unpackGlobalMap,
            #'globalmap':    self._unpackGlobalMap,
            #'OBJECTS':      self._unpackObjects,
            #'OBJSEQ':       self._unpackObjSeq,
            #'PREANIM':      self._unpackPreAnim,
            #'TABLES':       self._unpackTexTables,
            'TEX0':         self._unpackTextures,
            'TEX1':         self._unpackTextures,
            'TEXPRE':       self._unpackTextures,
            #'VOXMAP':       self._unpackVoxMap,
            #'WARPTAB':      self._unpackWarpTab,
            #'WEAPONDA':     self._unpackWeaponData,
        }

        if ext.startswith('romlist'):
            return self._unpackRomlist(inPath, outPath)
        elif name in nameFuncs:
            return nameFuncs[name](inPath, outPath)
        else:
            raise RuntimeError("Don't know how to unpack this file")


    def _unpackTextures(self, inPath:str, outPath:str) -> list[Asset]:
        """Unpack textures to specified directory.

        :param inPath: Path to file to unpack.
        :param outPath: Path to directory to write to.
        :returns: Assets that were extracted.

        Writes texture images to specified directory.
        """
        path, name = os.path.split(inPath)
        if name == 'TEXPRE':
            textures = self.game.texMgr.unpackTexPre()
        else:
            if name.startswith('TEX0'): which = 0
            else: which = 1
            textures = self.game.texMgr.unpackMapTextures(path, which)
        for tex in textures:
            tex.unpackToDir(outPath)
        return textures


    def _unpackModels(self, inPath:str, outPath:str) -> list[Asset]:
        """Unpack models to specified directory.

        :param inPath: Path to file to unpack.
        :param outPath: Path to directory to write to.
        :returns: Assets that were extracted.

        Writes model files to specified directory.
        """
        path, name = os.path.split(inPath)
        models = self.game.modelMgr.unpackMapModels(path)
        for model in models:
            model.unpackToDir(outPath)
        return models


    def unpackMapTable(self, outPath:str) -> None:
        """Unpack global map info.

        :param outPath: Path to file to write to.
        """
        maps  = self.game.mapMgr.readAllMapInfo()
        eRoot = ET.Element('maps')
        for mp in maps:
            eRoot.append(self.game.mapMgr.mapInfoToXml(mp))
        tree = ET.ElementTree(eRoot)
        ET.indent(tree, space='\t', level=0)
        tree.write(outPath)


# XXX proper arg parsing
if __name__ == '__main__':
    args = sys.argv[1:]
    action = args.pop(0)
    app = App(args.pop(0))

    if action == 'getTextureStats':
        app.game.texMgr.getTextureStats()

    elif action == 'unpack':
        inPath  = args.pop(0)
        outPath = args.pop(0)
        app.unpack(inPath, outPath)

    elif action == 'unpackMapTable':
        outPath = args.pop(0)
        app.unpackMapTable(outPath)

    elif action in ('unpackTex', 'unpackTexPre'):
        outPath = args.pop(0)
        if action == 'unpackTexPre':
            assets = app.unpack('TEXPRE.bin', outPath)
        else:
            mapName = args.pop(0)
            assets  = app.unpack(mapName + '/TEX0.bin', outPath)
            assets += app.unpack(mapName + '/TEX1.bin', outPath)
        eRoot = ET.Element('assets')
        for asset in assets:
            eRoot.append(asset.toXml())
        tree = ET.ElementTree(eRoot)
        ET.indent(tree, space='\t', level=0)
        tree.write(os.path.join(outPath, 'assets.xml'))

    elif action == 'listTex':
        textures = app.game.texMgr.getTexturesInMap(args.pop(0))
        res = []
        for tId, present in textures.items():
            if present: res.append('%04X' % tId)
        print(res)

    elif action == 'packTex':
        path = args.pop(0)
        tree = ET.parse(os.path.join(path, 'assets.xml'))
        files = app.game.texMgr.packToData(path, tree.getroot())
        for name, data in files.items():
            if data is not None:
                print("Writing", name)
                with open(os.path.join(path, name), 'wb') as file:
                    file.write(data)

    else:
        raise RuntimeError("Unknown action: "+str(action))
