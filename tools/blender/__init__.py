#!/usr/bin/env python3
"""SFA model import/export plugin for Blender.

This exists because Blender can't import/export bugger all.
"""

bl_info = {
    "name": "Star Fox Adventures",
    "description": "Import-Export SFA models",
    "author": "RenaKunisaki",
    "version": (0, 0, 1),
    "blender": (3, 2, 0),
    "location": "File > Import-Export",
    "warning": "This add-on is under development.",
    "wiki_url": "https://github.com/RenaKunisaki/StarFoxAdventures/wiki/",
    "tracker_url": "https://github.com/RenaKunisaki/StarFoxAdventures",
    "support": 'COMMUNITY',
    "category": "Import-Export"
}

# Reload the package modules when reloading add-ons in Blender with F8.
print("SFA MAIN")
if "bpy" in locals():
    import importlib
    names = ('sfa',)
    for name in names:
        ls = locals()
        if name in ls:
            importlib.reload(ls[name])

# fix up import path (why is this necessary?)
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# set up debug log
from .sfa import logger
logger.setup('sfa')
log = logger.logging.getLogger()

# import our modules
import bpy
from .sfa.importer.ImportOperator import ImportOperator
from .sfa.exporter.ExportOperator import ExportOperator
#from .sfa.importer.Preferences import SfaPreferences


# define Blender functions
__classes__ = (
    ImportOperator,
    ExportOperator,
)

def register():
    log.debug("SFA REGISTER")
    for c in __classes__:
        bpy.utils.register_class(c)
    bpy.types.TOPBAR_MT_file_import.append(
        ImportOperator.menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(
        ExportOperator.menu_func_export)

def unregister():
    log.debug("SFA UNREGISTER")
    for c in reversed(__classes__):
        bpy.utils.unregister_class(c)
    bpy.types.TOPBAR_MT_file_import.remove(
        ImportOperator.menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(
        ExportOperator.menu_func_export)

if __name__ == "__main__":
    register()

