
import bpy
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


class Login(bpy.types.Operator):
    '''Login to blenderstats.com'''
    bl_idname="file.login"
    bl_label = "Login"

    def execute(self, context):
        Authenticator.start_login_process()
        bpy.ops.wm.url_open(url=Authenticator.login_url)

        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        
        #TODO: Login before setting this
        addon_prefs.loginstate = "in"

        return {'FINISHED'}
        
            
