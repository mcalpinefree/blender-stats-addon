
import bpy


class CollectStats(bpy.types.Operator):
    bl_idname = "file.collectstats"
    bl_label = "Collect Stats"

    def execute(self, context):
        objecctCount = bpy.data.objects.values().count
        return {'FINISHED'}
