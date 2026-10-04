# ComfyUI workflows

Each workflow is a pair:

- `<name>.api.json` — exported from ComfyUI with **Export (API)**
- `<name>.mapping.json` — which node inputs the studio fills, and which
  registry models/tools the workflow uses (checked by the license gate)

## Mapping format

```json
{
  "tools": ["comfyui"],
  "models": ["wan2_2_ti2v_5b"],
  "required": ["prompt", "seed", "image"],
  "optional_nodes": {"10": {"when_missing": "lora_file", "passthrough": {"0": ["4", 0], "1": ["4", 1]}}},
  "inputs": {
    "prompt": [{"node": "6", "input": "text"}],
    "seed":   [{"node": "3", "input": "seed", "transform": "int"}],
    "image":  [{"node": "52", "input": "image"}]
  }
}
```

- `transform`: `int`, `float` or `prefix` (prepends `text`).
- `optional_nodes`: nodes removed when a param is absent (a LoRA loader
  with no LoRA), with links rewired to the passthrough outputs.
- Uploaded images (keyframes for image-to-video, references) are passed
  with `upload={"image": path}` and land in the mapped input as the
  uploaded file name.
- The mapping is validated against the workflow on every load, so a
  re-export that renumbers nodes fails loudly instead of silently.

## Included

| Workflow | Purpose | Status |
|---|---|---|
| `keyframe_sdxl` | Text-to-image keyframe, one LoRA | starter: add ControlNet (Blender layout) and reference nodes, re-export, update the mapping |

## To add next (from ComfyUI's built-in templates)

| Name | Base template | Models (registry keys) |
|---|---|---|
| `keyframe_edit` | Qwen-Image-Edit multi-image | `qwen_image_edit_2509` |
| `video_i2v_5b` | Wan2.2 TI2V-5B image-to-video | `wan2_2_ti2v_5b` |
| `video_flf_14b` | Wan2.2 14B first/last frame | `wan2_2_i2v_a14b` |
| `mouth_shapes` | inpaint mouth region A-F, X from the approved keyframe | same checkpoint as keyframes |

Then set `comfyui.workflows.video` / `mouth_shapes` in `studio/config.yaml`.
