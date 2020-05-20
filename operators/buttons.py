
import bpy
from ..core.stats import SnapshotStats


class CollectStats(bpy.types.Operator):
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        stats = SnapshotStats()
        stats.collect()
        return {'FINISHED'}
