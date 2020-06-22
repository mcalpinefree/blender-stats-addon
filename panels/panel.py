
import bpy
from ..preferences import Preferences

class BlenderStatsBasePanel:
    bl_category = "Blender Stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

class BlenderStatsMainPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstats"
    bl_label = "Blender Stats"

    def draw(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        login_state = addon_prefs.loginstate
        
        if (login_state == "out"): 
            self.layout.label(text="Please log in:")
            self.layout.operator('file.login')
        elif (login_state == "processing"):
            self.layout.label(text="Please log in in the browser...")
        elif (login_state == "in"):
            self.layout.label(text="Logged in")
            row = self.layout.row()
            row.label(text="Current project:")
            row.label(text="Test Project")
            self.layout.operator('file.collectstats')
        else:
            self.layout.label(text="Something went wrong, unknown login state")

class BlenderStatsProjectPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstatsprojects"
    bl_label = "Projects"

    def draw(self, context):
        self.layout.label(text="This will be a list of projects")

