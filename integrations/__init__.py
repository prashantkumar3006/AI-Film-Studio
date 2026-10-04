"""Adapters between the studio and external tools.

The studio never imports an external project directly. Each adapter
translates the studio's contract (shot lists, bible, provenance) into
the tool's own interface: an HTTP API (ComfyUI), a CLI (Blender,
Rhubarb, Remotion, ffmpeg) or a runner script executed locally or on a
GridShare GPU over SSH.
"""
