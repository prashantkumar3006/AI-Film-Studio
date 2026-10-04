"""Legal guard rails: license clearance, asset provenance and content scans.

None of this is legal advice. It enforces the studio's own rule: nothing
reaches a monetised release unless every tool, model, LoRA and asset in
it has a recorded, verified commercial-use clearance.
"""

from studio.legal.licenses import Clearance, check_entry, load_catalogue  # noqa: F401
