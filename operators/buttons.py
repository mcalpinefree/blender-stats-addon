
import bpy
from ..core.stats import SnapshotStats
from ..core.stats_queue import StatsQueue


class CollectStats(bpy.types.Operator):
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        stats = SnapshotStats()
        stats.collect()
        StatsQueue.add(stats)
        return {'FINISHED'}
