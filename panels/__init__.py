
import bpy
from .panel import BlenderStatsMainPanel, BlenderStatsProjectPanel, MyShortAddonProperties

def register():
    bpy.utils.register_class(BlenderStatsMainPanel)
    bpy.utils.register_class(BlenderStatsProjectPanel)
    bpy.utils.register_class(MyShortAddonProperties)
    bpy.types.Scene.custom_settings = bpy.props.PointerProperty(type=MyShortAddonProperties)

def unregister():
    del bpy.types.Scene.custom_settings
    bpy.utils.unregister_class(BlenderStatsMainPanel)
    bpy.utils.unregister_class(BlenderStatsProjectPanel)
    bpy.utils.unregister_class(MyShortAddonProperties)