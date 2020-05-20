import bpy

from .buttons import CollectStats

def register():
    bpy.utils.register_class(CollectStats)

def unregister():
    bpy.utils.unregister_class(CollectStats)