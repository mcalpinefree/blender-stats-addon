
import bpy
import json
import requests
from ..core.stats import SnapshotStats
from ..core.stats_queue import StatsQueue
from ..core.auth import Authenticator
from ..preferences import Preferences


class CollectStats(bpy.types.Operator):
    '''Send collections of stats to current project'''
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        stats = SnapshotStats()
        stats.collect()
        StatsQueue.add(stats)
        return {'FINISHED'}


class LoginTest(bpy.types.Operator):
    '''Login'''
    bl_idname = "file.logintest"
    bl_label = "Login Stats"

    def execute(self, context):
        bpy.ops.object.login('INVOKE_DEFAULT')
        return {'FINISHED'}


class Login(bpy.types.Operator):
    '''Login to blenderstats.com'''
    bl_idname = "object.login"
    bl_label = "Login"

    def __init__(self):
        self.httpd = None
        self.cognito = {}

    def execute(self, context):
        return {'FINISHED'}

    def modal(self, context, event):
        if "token" in self.cognito:
            cognito = json.loads(self.cognito['token'])
            self.httpd.shutdown()

            preferences = context.preferences
            addon_prefs = preferences.addons[Preferences.bl_idname].preferences
            addon_prefs.loginstate = "in"
            addon_prefs.token = self.cognito['token'].decode("utf-8")

            cognito = json.loads(addon_prefs.token)
            r = requests.get("https://api.blender-stats.staging.mcalpinefree.io/user",
                             headers={"Authorization": "Bearer " + cognito['id_token']})
            user = json.loads(r.content)
            print("Hello {}!".format(user["name"]))
            addon_prefs.name = user["name"]

            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        auth = Authenticator()
        self.httpd = auth.start_login_process(self.cognito)
        bpy.ops.wm.url_open(url=Authenticator.login_url)
        return {'RUNNING_MODAL'}
