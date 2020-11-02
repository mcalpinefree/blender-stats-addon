import bpy


# suggested way of keeping settings per file:
# https://www.blender.org/forum/viewtopic.php?t=27291

# This class encapsulates settings per blend file
class Settings():
    def register():
        bpy.types.Scene.selected_project_id = bpy.props.StringProperty()

    def unregister():
        pass

    settings = None

    def __init__(self):
        self.settings = bpy.data.scenes.get("Settings")
        if self.settings is None:
            self.settings = bpy.data.scenes.new("Settings")

    def get_str(self, key):
        return getattr(self.settings, key)

    def set_str(self, key, value):
        return setattr(self.settings, key, value)
