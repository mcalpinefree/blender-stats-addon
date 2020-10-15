
import bpy
import json
import requests
from ..preferences import Preferences
from ..core.user import User


class BlenderStatsBasePanel:
    bl_category = "Blender Stats"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


class BlenderStatsMainPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstats"
    bl_label = "Blender Stats"

    def draw(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        login_state = addon_prefs.loginstate

        if (login_state == "out"):
            self.layout.label(text="Please log in:")
            self.layout.operator('file.start_login')
        elif (login_state == "processing"):
            self.layout.label(text="Please log in in the browser...")
        elif (login_state == "in"):
            user = User.get_local_user(addon_prefs)
            self.layout.label(text="Logged in: {}".format(user.name))
            self.layout.operator('file.logout')
            row = self.layout.row()
            row.label(text="Current project:")
            row.label(text="Test Project")
            self.layout.operator('file.collectstats')
        else:
            self.layout.label(text="Something went wrong, unknown login state")


def execute_operator(self, context):
    eval('bpy.ops.' + self.primitive + '()')

class MyShortAddonProperties(bpy.types.PropertyGroup):
    mode_options = [
        ("mesh.primitive_plane_add", "Plane", '', 'MESH_PLANE', 0),
        ("mesh.primitive_cube_add", "Cube", '', 'MESH_CUBE', 1),
        ("mesh.primitive_circle_add", "Circle", '', 'MESH_CIRCLE', 2),
        ("mesh.primitive_uv_sphere_add", "UV Sphere", '', 'MESH_UVSPHERE', 3),
        ("mesh.primitive_ico_sphere_add", "Ico Sphere", '', 'MESH_ICOSPHERE', 4),
        ("mesh.primitive_cylinder_add", "Cylinder", '', 'MESH_CYLINDER', 5),
        ("mesh.primitive_cone_add", "Cone", '', 'MESH_CONE', 6),
        ("mesh.primitive_torus_add", "Torus", '', 'MESH_TORUS', 7)
    ]

    # primitive: bpy.props.EnumProperty(
    #     items=mode_options,
    #     description="offers....",
    #     default="mesh.primitive_plane_add",
    #     update=execute_operator
    # )

    

class BlenderStatsProjectPanel(BlenderStatsBasePanel, bpy.types.Panel):
    bl_idname = "OBJECT_PT_blenderstatsprojects"
    bl_label = "Projects"

    primitive:  bpy.props.EnumProperty(
        name="My Settings",
        description="Custom Settings",
        items=[
            ('S1', "Setting One", "", 0),
            ('S2', "Setting Two", "", 1),
            ('S3', "Setting Three", "", 2),
        ],
        default='S1'
    )

    # my_short_addon = bpy.props.PointerProperty(type=MyShortAddonProperties)

    # fixed_items = bpy.props.EnumProperty(items= [('0', 'A', 'The zeroth item'),    
    #                                             ('1', 'B', 'The first item'),    
    #                                             ('2', 'C', 'The second item'),    
    #                                             ('3', 'D', 'The third item')],
    #                                             name = "fixed list")

    def draw(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[Preferences.bl_idname].preferences
        user = User.get_local_user(addon_prefs)

        # self.layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        # self.layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        # self.layout.operator("object.select_random", text="Random")
        settings = context.scene.custom_settings
        print(settings)
        print(self.my_short_addon)
        self.layout.prop(self, "primitive")

        # self.layout.menu("INFO_MT_add", text="Add")

        for project in user.projects:
            self.layout.label(text=project["name"])

