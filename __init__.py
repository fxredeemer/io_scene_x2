# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import sys, os, bpy
sys.path.append(os.path.dirname(__file__)) 
from bpy.props import StringProperty, BoolProperty, EnumProperty
from . import export_x

bl_info = {
    "name": "DirectX X Format",
    "author": "fx137, Bibindon",
    "version": (0, 0, 3),
    "blender": (2, 80, 0),
    "location": "File > Export > DirectX (.x)",
    "description": "Migrated to 2.8 from (https://github.com/bibindon/io_scene_x2)",
    "support": "TESTING",
    "category": "Import-Export"}

if "bpy" in locals():
    import imp
    imp.reload(export_x)

class ExportDirectX(bpy.types.Operator):
    """Export selection to DirectX"""

    bl_idname = "export_scene.x"
    bl_label = "Export DirectX"

    filepath = StringProperty(
        subtype='FILE_PATH')

    SelectedOnly = BoolProperty(
        name="Export Selected Objects Only",
        description="Export only selected objects",
        default=True)

    CoordinateSystem = EnumProperty(
        name="Coordinate System",
        description="Use the selected coordinate system for export",
        items=(('LEFT_HANDED', "Left-Handed", "Use a Y up, Z forward system or a Z up, -Y forward system"),
               ('RIGHT_HANDED', "Right-Handed", "Use a Y up, -Z forward system or a Z up, Y forward system")),
        default='RIGHT_HANDED')

    UpAxis = EnumProperty(
        name="Up Axis",
        description="The selected axis points upward",
        items=(('Y', "Y", "The Y axis points up"),
               ('Z', "Z", "The Z axis points up")),
        default='Z')

    ExportMeshes = BoolProperty(
        name="Export Meshes",
        description="Export mesh objects",
        default=True)

    ExportNormals = BoolProperty(
        name="Export Normals",
        description="Export mesh normals",
        default=True)

    FlipNormals = BoolProperty(
        name="Flip Normals",
        description="Flip mesh normals before export",
        default=False)

    ExportUVCoordinates = BoolProperty(
        name="Export UV Coordinates",
        description="Export mesh UV coordinates, if any",
        default=True)

    ExportMaterials = BoolProperty(
        name="Export Materials",
        description="Export material properties and reference image textures",
        default=True)

    ExportVertexColors = BoolProperty(
        name="Export Vertex Colors",
        description="Export mesh vertex colors, if any",
        default=False)

    ExportSkinWeights = BoolProperty(
        name="Export Skin Weights",
        description="Bind mesh vertices to armature bones",
        default=False)

    ApplyModifiers = BoolProperty(
        name="Apply Modifiers",
        description="Apply the effects of object modifiers before export",
        default=False)

    ExportArmatureBones = BoolProperty(
        name="Export Armature Bones",
        description="Export armatures bones",
        default=False)

    ExportRestBone = BoolProperty(
        name="Export Rest Position",
        description="Export bones in their rest position (recommended for "
            "animation)",
        default=False)

    ExportAnimation = BoolProperty(
        name="Export Animations",
        description="Export object and bone animations.  Data is exported for "
            "every frame",
        default=False)

    IncludeFrameRate = BoolProperty(
        name="Include Frame Rate",
        description="Include the AnimTicksPerSecond template which is "
            "used by some engines to control animation speed",
        default=False)

    ExportActionsAsSets = BoolProperty(
        name="Export Actions as AnimationSets",
        description="Export each action of each object as a separate "
            "AnimationSet. Otherwise all current actions are lumped "
            "together into a single set",
        default=False)

    ExportNLATrackAction = BoolProperty(
        name="Export NLA track Actions",
        description="Export NLA track actions",
        default=False)

    Verbose = BoolProperty(
        name="Verbose",
        description="Run the exporter in debug mode. Check the console for output",
        default=False)

    def execute(self, context):
        self.filepath = bpy.path.ensure_ext(self.filepath, ".x")

        Exporter = export_x.DirectXExporter(self, context)
        Exporter.Export()
        return {'FINISHED'}

    def invoke(self, context, event):
        if not self.filepath:
            self.filepath = bpy.path.ensure_ext(bpy.data.filepath, ".x")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator(ExportDirectX.bl_idname,
                         text="DirectX (.x)").filepath = "*.x"

def register():
    bpy.utils.register_class(ExportDirectX)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ExportDirectX)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)


if __name__ == "__main__":
    register()
