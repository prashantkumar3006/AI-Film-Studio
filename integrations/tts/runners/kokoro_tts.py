#!/usr/bin/env python3
"""English TTS with Kokoro-82M (Apache-2.0 weights). Small enough for CPU.

Install where it runs:   pip install kokoro soundfile
(Kokoro also needs espeak-ng on the system for some voices.)

Usage:
    python integrations/tts/runners/kokoro_tts.py --text "Hello" --voice am_michael --out line.wav --speed 1.0

Check the voice list on huggingface.co/hexgrad/Kokoro-82M; voice IDs
starting with 'a' are American English, 'b' British English.
"""

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--voice", default="am_michael")
    parser.add_argument("--out", required=True)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--lang-code", default=None, help="Kokoro language code; default from voice prefix")
    args = parser.parse_args()

    try:
        import numpy as np
        import soundfile as sf
        from kokoro import KPipeline
    except ImportError as error:
        print(f"Missing dependency: {error}. Run: pip install kokoro soundfile", file=sys.stderr)
        return 2

    pipeline = KPipeline(lang_code=args.lang_code or args.voice[0])
    chunks = [audio for _, _, audio in pipeline(args.text, voice=args.voice, speed=args.speed)]
    if not chunks:
        print("Kokoro produced no audio", file=sys.stderr)
        return 1
    sf.write(args.out, np.concatenate(chunks), 24000)
    return 0


if __name__ == "__main__":
    sys.exit(main())
