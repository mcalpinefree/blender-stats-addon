
import pprint
import bpy
import json
import requests
from ..core.user import User
from ..preferences import Preferences
from ..settings import Settings


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
        user_token = addon_prefs.user_token

        if (login_state == "out"):
            self.layout.label(text="Please log in:")
            self.layout.operator('file.start_login')
        elif (login_state == "processing"):
            self.layout.label(text="Please log in in the browser...")
        elif (login_state == "in"):
            user = User.get_local_user(addon_prefs)
            self.layout.label(text="Logged in: {}".format(user.name))
            self.layout.operator('file.logout')
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
        settings = Settings()

        row = self.layout.row()
        selected_project_id = settings.get_str("selected_project_id")
        if selected_project_id != "":
            row.label(text="Current project:")
            for project in user.projects:
                if selected_project_id == project["id"]:
                    row.label(text=project["name"])
        else:
            row.label(text="Please select a project")

        self.layout.operator('file.selectproject')
