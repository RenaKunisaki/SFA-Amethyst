import logging; log = logging.getLogger(__name__)
import bmesh
import bpy
import bpy_extras
import os
import os.path
from .Importer import Importer


class ImportOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Load an SFA model file"""

    bl_idname    = "import_scene.sfadventures"
    bl_label     = "Import Star Fox Adventures model"
    bl_options   = {'UNDO'}
    filename_ext = ".sfamodel"

    filter_glob  = bpy.props.StringProperty(
        default="*.sfamodel;*.bin",
        options={'HIDDEN'},
    )
    filepath = bpy.props.StringProperty(
        name="File Path",
        #maxlen=1024,
        description="Filepath used for importing the model file")

    importWholeMap: bpy.props.BoolProperty(name="Import Entire Map",
        description="Import all modXX.bin files in the directory.",
        default=True)


    def draw(self, context):
        box = self.layout.box()
        box.label(text="Map Import:", icon='PREFERENCES')
        box.prop(self, 'importWholeMap')


    def execute(self, context):
        #user_preferences = context.user_preferences
        #addon_prefs = user_preferences.addons[self.bl_idname].preferences
        #print("PREFS:", user_preferences, addon_prefs)

        # enter Object mode if not already
        try: bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError: pass

        if self.importWholeMap:
            path, _ = os.path.split(self.properties.filepath)
            for name in os.listdir(path):
                if not name.startswith('mod'): continue
                log.info("importing: %s", name)
                importer = Importer(self, context)
                r = importer.run(os.path.join(path, name))
                if r != {'FINISHED'}: return r
            return {'FINISHED'}
        else:
            log.info("importing: %s", self.properties.filepath)
            importer = Importer(self, context)
            return importer.run(self.properties.filepath)


    @staticmethod
    def menu_func_import(self, context):
        """Handle the Import menu item."""
        self.layout.operator(
            ImportOperator.bl_idname,
            text="Star Fox Adventures")
