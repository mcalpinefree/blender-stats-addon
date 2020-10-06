# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Blender Stats",
    "author" : "McAlpine Free Ltd",
    "description" : "Addon to send stats to blenderstats.com",
    "blender" : (2, 80, 0),
    # version field will be overwritten by concourse ci when released
    "version" : (0, 0, 1),
    "location" : "View3D > Sidevar > Blender Stats",
    "warning" : "",
    "category" : "3D View"
}

import bpy
from . import panels
from . import operators
from .preferences import Preferences

def register():
    # forces the AddonPreferences to be autosaved: https://blender.stackexchange.com/questions/157677/add-on-preferences-auto-saving-bug
    # this may not be the best solution
    bpy.context.preferences.use_preferences_save = True
    bpy.utils.register_class(Preferences)
    panels.register()
    operators.register()


def unregister():
    bpy.utils.unregister_class(Preferences)
    panels.unregister()
    operators.unregister()
