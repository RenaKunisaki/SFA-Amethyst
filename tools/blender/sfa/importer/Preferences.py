import logging; log = logging.getLogger(__name__)
import bpy


class SfaPreferences(bpy.types.AddonPreferences):
    bl_idname = "import_scene.sfadventures"

    def _onUpdate(self, context):
        log.debug("_onUpdate %r", context)

    importWholeMap = bpy.props.BoolProperty(
        name="Import Entire Map",
        description="Import all modXX.bin files in the directory.",
        default=True,
        options={'ANIMATABLE'},
        subtype='NONE',
        update=_onUpdate,
    )

    def draw(self, context):
        self.layout.prop(self, "importWholeMap")
