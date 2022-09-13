import logging; log = logging.getLogger(__name__)
import bmesh
import bpy
import bpy_extras
import os
import os.path
from .Exporter import Exporter


class ExportOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    """Export an SFA model file"""

    bl_idname    = "export_scene.sfadventures"
    bl_label     = "Export Star Fox Adventures model"
    bl_options   = {'UNDO'}
    filename_ext = ".bin" # XXX is this used?

    filter_glob  = bpy.props.StringProperty(
        default="*.sfamodel;*.bin",
        options={'HIDDEN'},
    )
    filepath = bpy.props.StringProperty(
        name="File Path",
        #maxlen=1024,
        description="Where to export the model file(s) to")

    exportWholeMap: bpy.props.BoolProperty(name="Export Entire Map",
        description="Export each block to its own modXX.bin file.",
        default=True)


    def draw(self, context):
        box = self.layout.box()
        box.label(text="Map Export:", icon='PREFERENCES')
        box.prop(self, 'exportWholeMap')


    def execute(self, context):
        #user_preferences = context.user_preferences
        #addon_prefs = user_preferences.addons[self.bl_idname].preferences
        #print("PREFS:", user_preferences, addon_prefs)

        # enter Object mode if not already
        try: bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError: pass

        nExport = 0
        if self.exportWholeMap:
            for name, col in bpy.data.collections.items():
                if not name.startswith('mod'): continue
                nExport += 1
                path, _ = os.path.split(self.properties.filepath)
                path = os.path.join(path, name + '.bin')
                exporter = Exporter(self, context)
                r = exporter.exportBlock(name, path)
                if r != {'FINISHED'}: return r

            if nExport == 0:
                print("No blocks found to export")
                # XXX better error message/display
            return {'FINISHED'}

        else: # only export the selected block
            raise NotImplementedError
            # TODO: get selected block and all that
            log.info("importing: %s", self.properties.filepath)
            importer = Importer(self, context)
            return importer.run(self.properties.filepath)


    @staticmethod
    def menu_func_export(self, context):
        """Handle the Export menu item."""
        self.layout.operator(
            ExportOperator.bl_idname,
            text="Star Fox Adventures")
