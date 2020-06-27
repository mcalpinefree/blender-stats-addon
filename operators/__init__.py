import bpy

from .buttons import CollectStats, StartLogin, LoginManager, Logout
from .timers import process_stats_queue, count_time

def register():
    bpy.utils.register_class(CollectStats)
    bpy.utils.register_class(LoginManager)
    bpy.utils.register_class(StartLogin)
    bpy.utils.register_class(Logout)
    bpy.app.timers.register(process_stats_queue)
    bpy.app.timers.register(count_time)

def unregister():
    bpy.utils.unregister_class(CollectStats)
    bpy.utils.unregister_class(LoginManager)
    bpy.utils.unregister_class(StartLogin)
    bpy.utils.unregister_class(Logout)
    bpy.app.timers.unregister(process_stats_queue)
    bpy.app.timers.register(count_time)