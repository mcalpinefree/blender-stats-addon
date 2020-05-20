
import bpy
from .panel import BlenderStatsMainPanel, BlenderStatsProjectPanel

def register():
    bpy.utils.register_class(BlenderStatsMainPanel)
    bpy.utils.register_class(BlenderStatsProjectPanel)

def unregister():
    bpy.utils.unregister_class(BlenderStatsMainPanel)
    bpy.utils.unregister_class(BlenderStatsProjectPanel)