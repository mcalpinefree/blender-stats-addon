
import bpy
import json
import requests
from ..core.stats import SnapshotStats
from ..core.stats_queue import StatsQueue
from ..core.auth import Authenticator
from ..preferences import Preferences
from ..core.user import User


class CollectStats(bpy.types.Operator):
    '''Send collections of stats to current project'''
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        stats = SnapshotStats()
        stats.collect()
        StatsQueue.add(stats)
        return {'FINISHED'}


class StartLogin(bpy.types.Operator):
    '''Login to blenderstats.com'''
    bl_idname = "file.start_login"
    bl_label = "Login"

    def execute(self, context):
        bpy.ops.object.login_manager('INVOKE_DEFAULT')
        return {'FINISHED'}

class Logout(bpy.types.Operator):
    '''Logout'''
    bl_idname = "file.logout"
    bl_label = "Logout"

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        addon_prefs.loginstate = "out"
        return {'FINISHED'}


class LoginManager(bpy.types.Operator):
    '''Manage login process'''
    bl_idname = "object.login_manager"
    bl_label = "Manage Login"

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
            addon_prefs.user_token = self.cognito['token'].decode("utf-8")

            cognito = json.loads(addon_prefs.user_token)

            user = User.get_user_online(cognito['id_token'])
            user.save_as_current_user(addon_prefs)

            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.execute(context)
        context.window_manager.modal_handler_add(self)
        auth = Authenticator()
        self.httpd = auth.start_login_process(self.cognito)
        bpy.ops.wm.url_open(url=Authenticator.login_url)
        return {'RUNNING_MODAL'}
