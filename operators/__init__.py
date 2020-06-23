import bpy

from .buttons import CollectStats, Login, LoginTest
from .timers import process_stats_queue, count_time

def register():
    bpy.utils.register_class(CollectStats)
    bpy.utils.register_class(Login)
    bpy.utils.register_class(LoginTest)
    bpy.app.timers.register(process_stats_queue)
    bpy.app.timers.register(count_time)

def unregister():
    bpy.utils.unregister_class(CollectStats)
    bpy.utils.unregister_class(Login)
    bpy.utils.unregister_class(LoginTest)
    bpy.app.timers.unregister(process_stats_queue)
    bpy.app.timers.register(count_time)