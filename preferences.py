import bpy
from bpy.props import StringProperty, EnumProperty

class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path"
    )

    loginstate: EnumProperty(
        items = [
            ("out", "Logged out", "User is logged out"),
            ("in", "Logged in", "User is logged in"),
            ("processing", "Processing login", "User has requested login and awaiting user input")
        ],
        name="Login State",
        default = "out"
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Currently no preferences available...")