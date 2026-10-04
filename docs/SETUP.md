# Setup

## 1. Laptop (CPU only is fine)

```bash
git clone <this private repo> && cd ai-film-studio
python -m pip install -r requirements.txt          # PyYAML
python -m pip install -r requirements-qc.txt       # optional QC extras (CPU)
# FFmpeg: https://ffmpeg.org/download.html  (required)
# Blender: https://www.blender.org/download/  (for layout)
# Rhubarb Lip Sync: release zip from github.com/DanielSWolf/rhubarb-lip-sync, put on PATH
# Node.js 18+ for Remotion: cd integrations/motion_graphics/remotion && npm install
cp .env.example .env                               # fill in later
python -m studio doctor
```

`python -m unittest discover -s tests` must pass before you start.

## 2. Claude

- Open the repo in **Claude Code**. `CLAUDE.md` and the skills in
  `.claude/skills/` load automatically.
- For Blender: install **Blender MCP** (see `integrations/blender/README.md`)
  and connect it to the **Claude desktop app**.
- Start every session with: "studio status for <series> <episode>". The
  `studio-manager` skill takes it from there.

## 3. GridShare GPU (only when there is a batch to run)

1. On gridshare.in, rent an RTX 4090 with the ComfyUI one-click image.
2. Put the SSH host, port and user into `.env`.
3. On the instance, once: clone this repo into `GRIDSHARE_REMOTE_DIR`,
   install Indic Parler-TTS (see the runner file header), and download the
   cleared models into ComfyUI's model folders:
   - `animagine-xl-4.0.safetensors` → `models/checkpoints/`
   - Wan2.2 and Qwen-Image-Edit files → use ComfyUI's built-in templates,
     which list the exact files and folders.
4. From the laptop:
   ```bash
   python -m studio compute start <series> <n> --gpu rtx_4090
   python -m studio compute tunnel        # ComfyUI at http://127.0.0.1:8188
   ```
5. When the batch is done: `python -m studio compute stop <series> <n>` and
   **stop the instance on gridshare.in**.

If GridShare offers a persistent volume, keep models on it: re-downloading
20+ GB every session wastes paid time.

## 4. ComfyUI workflows

`integrations/comfyui/workflows/` holds `<name>.api.json` + `<name>.mapping.json`
pairs. A starter keyframe workflow is included. To add one (e.g. Wan2.2
image-to-video): build or open it in ComfyUI, "Export (API)", save it here,
write the mapping (see `integrations/comfyui/workflows/README.md`), list
its models in the mapping, and make sure each is cleared in the registry.

## 5. First series

```bash
python -m studio series new my-show --title "My Show" --languages en,hi
# fill series/my-show/bible/ with Claude (series-bible skill)
python -m studio series check my-show
python -m studio episode new my-show 1 --title "Pilot"
python -m studio pipeline status my-show 1
```
