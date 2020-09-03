
import bpy
import json
import requests
from ..preferences import Preferences
from ..core.user import User


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
            self.layout.operator('file.start_login')
        elif (login_state == "processing"):
            self.layout.label(text="Please log in in the browser...")
        elif (login_state == "in"):
            user = User.get_local_user(addon_prefs)
            self.layout.label(text="Logged in: {}".format(user.name))
            self.layout.operator('file.logout')
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
        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        user = User.get_local_user(addon_prefs)

        for project in user.projects:
            self.layout.label(text=project["name"])

