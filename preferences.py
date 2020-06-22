import bpy
from bpy.props import StringProperty

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Currently no preferences available...")