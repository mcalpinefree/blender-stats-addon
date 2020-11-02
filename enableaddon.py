import shutil
import bpy
import pathlib
import os
from os import path

current_dir = pathlib.Path(__file__).parent.absolute()

user_path = bpy.utils.resource_path('USER')
addons_path = path.join(user_path, "scripts/addons")
blender_stats_installed_path = path.join(addons_path, "blender-stats-addon")

if path.exists(blender_stats_installed_path):
    if path.islink(blender_stats_installed_path):
        os.unlink(blender_stats_installed_path)
    else:
        shutil.rmtree(blender_stats_installed_path)

shutil.copytree(current_dir, blender_stats_installed_path)

bpy.ops.preferences.addon_install(
    filepath='{}/__init__.py'.format(current_dir))
bpy.ops.preferences.addon_enable(module='blender-stats-addon')
bpy.ops.wm.save_userpref()
