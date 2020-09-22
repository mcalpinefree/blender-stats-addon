import bpy
import pathlib

current_dir = pathlib.Path(__file__).parent.absolute()

bpy.ops.preferences.addon_install(
    filepath='{}/__init__.py'.format(current_dir))
bpy.ops.preferences.addon_enable(module='blender-stats-addon')
bpy.ops.wm.save_userpref()
