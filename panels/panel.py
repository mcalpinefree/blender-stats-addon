
import bpy

class BlenderStatsBasePanel:
    bl_category = "Blender Stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

class BlenderStatsMainPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstats"
    bl_label = "Blender Stats"

    def draw(self, context):
        self.layout.label(text="Logged in")
        row = self.layout.row()
        row.label(text="Current project:")
        row.label(text="Test Project")
        self.layout.operator('file.collectstats')

class BlenderStatsProjectPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstatsprojects"
    bl_label = "Projects"

    def draw(self, context):
        self.layout.label(text="This will be a list of projects")

