"""Blender-side script: render a layout frame (or range) with Workbench.

Runs inside Blender (``bpy``), not in the studio's Python. Kept to APIs
that have been stable since Blender 2.8. Prints STUDIO_RENDER_OK on
success so the adapter can verify.
"""

import argparse
import sys

import bpy  # type: ignore


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--camera")
    parser.add_argument("--frame", type=int, default=1)
    parser.add_argument("--end-frame", type=int)
    parser.add_argument("--resolution", default="1920x1080")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    scene = bpy.context.scene
    if args.camera:
        if args.camera not in bpy.data.objects:
            raise SystemExit(f"Camera '{args.camera}' not found in this .blend")
        scene.camera = bpy.data.objects[args.camera]
    width, height = (int(v) for v in args.resolution.lower().split("x"))
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.fps = 24
    scene.render.engine = "BLENDER_WORKBENCH"
    shading = scene.display.shading
    shading.light = "STUDIO"
    shading.color_type = "MATERIAL"
    shading.show_object_outline = True
    shading.show_cavity = True
    scene.render.image_settings.file_format = "PNG"

    if args.end_frame:
        scene.frame_start = args.frame
        scene.frame_end = args.end_frame
        scene.render.filepath = args.out.rstrip("/") + "/frame_"
        bpy.ops.render.render(animation=True)
    else:
        scene.frame_set(args.frame)
        scene.render.filepath = args.out
        bpy.ops.render.render(write_still=True)
    print("STUDIO_RENDER_OK")


main()
