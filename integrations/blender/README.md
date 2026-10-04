# Blender

## Interactive: Blender MCP with Claude (laptop)

[Blender MCP](https://github.com/ahujasid/blender-mcp) (MIT) lets Claude
create and edit objects, materials and cameras in your running Blender
through the Claude desktop app.

1. Install Blender 3.0+ and [uv](https://docs.astral.sh/uv/) (official
   installer, not pip).
2. `uvx blender-mcp install-addon` copies the add-on into Blender; enable it
   in Blender preferences and click "Connect" in the add-on panel.
3. Add the MCP server to the Claude desktop app config:
   `{"mcpServers": {"blender": {"command": "uvx", "args": ["blender-mcp"]}}}`
4. Ask Claude (with the `storyboard-previs` and `production-design`
   skills) to block out a set: simple shapes, correct scale, named cameras
   `CAM_SC01_SH001`, … Save as `series/<slug>/bible/layouts/<location>.blend`
   is fine for small files; large files belong outside git.

Assets Blender MCP can fetch (Poly Haven, Sketchfab, Poly Pizza, Hyper3D,
Hunyuan3D) each have their own license or service terms. Record the source
and license of anything you keep, or the release gate will block it.

## Headless: layout renders (`adapter.py`)

```bash
blender -b layout.blend --python integrations/blender/scripts/render_layout.py -- \
    --camera CAM_SC01_SH001 --frame 1 --out projects/.../07_storyboard-previs/layout/SC01_SH001.png
```

Workbench engine, so it runs on a CPU. The frame is a composition guide:
ComfyUI extracts depth or lineart from it to control the keyframe. The
script is kept to long-stable Blender APIs, but it is not run in CI (no
Blender there): test it once on your Blender version.
