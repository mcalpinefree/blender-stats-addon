
import pprint
import bpy
import json
import requests
from datetime import datetime
from ..core.auth import Authenticator
from ..core.stats import SnapshotStats
from ..core.stats_queue import StatsQueue
from ..core.user import User
from ..logger import Logger
from ..preferences import Preferences
from ..settings import Settings


class CollectStats(bpy.types.Operator):
    '''Send collections of stats to current project'''
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        stats = SnapshotStats()
        stats.collect()

        # push counts
        t = datetime.now()
        s = t.strftime('%Y-%m-%dT%H:%M:%S.%f')
        time = s[:-3] + "Z"
        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        cognito = json.loads(addon_prefs.user_token)
        r = requests.get("https://api.blender-stats.staging.mcalpinefree.io/user",
                         headers={"Authorization": "Bearer " + cognito['id_token']})
        response = json.loads(r.content)
        print(response)
        # this is a hack, we need to choose the project the stats are associated with
        project_id = response["project_ids"][0]
        for key, value in stats.stats.items():
            if key == "blender_version":
                continue
            print("project_id {}, time {}, count {}, count_item {}".format(
                project_id, time, value, key))
            r = requests.post("https://api.blender-stats.staging.mcalpinefree.io/stat/count",
                              headers={"Authorization": "Bearer " +
                                       cognito['id_token']},
                              json={"project_id": project_id,
                                    "time": time,
                                    "count": value,
                                    "count_item": key})

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
        if "tokens" in self.cognito:
            cognito = self.cognito['tokens']
            self.httpd.shutdown()

            preferences = context.preferences
            addon_prefs = preferences.addons[Preferences.bl_idname].preferences
            addon_prefs.loginstate = "in"
            addon_prefs.user_token = json.dumps(self.cognito['tokens'])

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


def items_cb(self, context):
    preferences = context.preferences
    addon_prefs = preferences.addons[Preferences.bl_idname].preferences
    user = User.get_local_user(addon_prefs)

    projects = []
    for project in user.projects:
        projects.append((project["id"], project["name"], project["name"]))

    return projects


def update_cb(self, context):
    print("Updated:", self.dyn_list)


class SelectProject(bpy.types.Operator):
    '''Select current project'''
    bl_idname = "file.selectproject"
    bl_label = "Select Project"

    project_enum = bpy.props.EnumProperty(
        name="Project",
        items=items_cb,
        update=update_cb
    )

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        logger = Logger()
        layout.prop(self, "project_enum")

    def execute(self, context):
        logger = Logger()
        settings = Settings()
        logger.debug("previously selected project: {}\n".format(
            settings.get_str("selected_project_id")))
        logger.debug("selected project: {}\n".format(self.project_enum))
        settings.set_str("selected_project_id", self.project_enum)
        return {'FINISHED'}
