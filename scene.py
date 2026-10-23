"""Generate a reproducible Blender scene and render it on the CPU."""

from pathlib import Path

import bpy


def main():
    output = Path(__file__).resolve().parent / "output"
    output.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=False)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 32
    # Debian's Blender build does not include OpenImageDenoise.
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(output / "preview.png")

    material = bpy.data.materials.new("Blue ceramic")
    material.diffuse_color = (0.03, 0.25, 0.65, 1.0)
    material.use_nodes = True
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = material.diffuse_color
    shader.inputs["Roughness"].default_value = 0.3
    cube = bpy.data.objects["Cube"]
    cube.data.materials.clear()
    cube.data.materials.append(material)
    bevel = cube.modifiers.new("Soft edges", "BEVEL")
    bevel.width = 0.12
    bevel.segments = 4

    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -1))
    bpy.ops.wm.save_as_mainfile(filepath=str(output / "scene.blend"))
    bpy.ops.render.render(write_still=True)
    for name in ("scene.blend", "preview.png"):
        path = output / name
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing or empty output: {path}")
    print(f"Render complete: {output}")


if __name__ == "__main__":
    main()
