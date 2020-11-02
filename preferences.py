import bpy
from bpy.props import StringProperty, EnumProperty, CollectionProperty


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    filepath: StringProperty(
        name="Example File Path"
    )

    loginstate: EnumProperty(
        items=[
            ("out", "Logged out", "User is logged out"),
            ("in", "Logged in", "User is logged in"),
            ("processing", "Processing login",
             "User has requested login and awaiting user input")
        ],
        name="Login State",
        default="out"
    )

    user_token: StringProperty(
        name="Cognito Token",
        default="",
        maxlen=5000,
    )

    user_id: StringProperty(
        name="User Id",
        default="",
        maxlen=300,
    )

    user_name: StringProperty(
        name="User name",
        default="",
        maxlen=300,
    )

    projects: StringProperty(
        name="Project IDs",
        default="[]",
        maxlen=5000,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Currently no preferences available...")
