
import bpy

class BlenderStatsBasePanel:
    bl_category = "Blender Stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

class BlenderStatsMainPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstats"
    bl_label = "Blender Stats"

    def draw(self, context):
        self.layout.label(text="Hello World")

class BlenderStatsSubPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_parent_id = "OBJECT_PT_blenderstats"
    bl_label = "SubPanel"

    def draw(self, context):
        self.layout.label(text="SubPanel Content")

