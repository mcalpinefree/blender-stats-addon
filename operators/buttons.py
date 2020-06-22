
import bpy
from ..core.stats import SnapshotStats
from ..core.stats_queue import StatsQueue
from ..core.auth import Authenticator


class CollectStats(bpy.types.Operator):
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        stats = SnapshotStats()
        stats.collect()
        StatsQueue.add(stats)
        return {'FINISHED'}


class Login(bpy.types.Operator):
    bl_idname="file.login"
    bl_label = "Login"

    def execute(self, context):
        Authenticator.start_login_process()
        bpy.ops.wm.url_open(url=Authenticator.login_url)

        return {'FINISHED'}
        
            
