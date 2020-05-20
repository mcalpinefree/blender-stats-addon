import bpy

class SnapshotStats:
    stats = {}
    def collect(self):

        #count things
        self.stats['object_count'] = len(bpy.data.objects.values())
        self.stats['scenes_count'] = len(bpy.data.scenes.values())
        self.stats['cameras_count'] = len(bpy.data.cameras.values())
        self.stats['lights_count'] = len(bpy.data.lights.values())
        self.stats['materials_count'] = len(bpy.data.materials.values())
        self.stats['meshes_count'] = len(bpy.data.meshes.values())
        self.stats['textures_count'] = len(bpy.data.textures.values())

        #version things
        self.stats['blender_version'] = bpy.data.version
        print(self.stats)
