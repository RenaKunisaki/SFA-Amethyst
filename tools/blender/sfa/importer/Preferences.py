import logging; log = logging.getLogger(__name__)
import bpy


class SfaPreferences(bpy.types.AddonPreferences):
    bl_idname = "import_scene.sfadventures"

    def _onUpdate(self, context):
        print("SFA _onUpdate", context)

    debugDumpFiles = bpy.props.BoolProperty(
        name="Dump debug info to files",
        description="Create `sfa-SomeFile-dump.txt` files for debugging.",
        default=False,
        options={'ANIMATABLE'},
        subtype='NONE',
        update=_onUpdate,
    )

    def draw(self, context):
        print("SfaPreferences draw")
        self.layout.prop(self, "debugDumpFiles")
