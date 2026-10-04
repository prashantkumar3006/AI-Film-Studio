#!/usr/bin/env python3
"""Hindi (and 20 other Indian languages) TTS with AI4Bharat Indic Parler-TTS
(Apache-2.0). Use a GPU for episode volumes; CPU works but is slow.

Install where it runs:
    pip install git+https://github.com/huggingface/parler-tts.git soundfile

Named Hindi speakers on the model card: Rohit, Divya (recommended),
Aman, Rani. Keep each character on one speaker plus a fixed description
so the voice stays consistent across episodes.

Usage:
    python integrations/tts/runners/indic_parler_tts.py \
        --text "नमस्ते" --speaker Rohit \
        --description "Rohit speaks in a calm, low voice, very clear audio." \
        --out line.wav
"""

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    parser.add_argument("--speaker", default="Rohit")
    parser.add_argument("--description", default="")
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--model", default="ai4bharat/indic-parler-tts")
    args = parser.parse_args()

    try:
        import soundfile as sf
        import torch
        from parler_tts import ParlerTTSForConditionalGeneration
        from transformers import AutoTokenizer
    except ImportError as error:
        print(f"Missing dependency: {error}. See the install line in this file.", file=sys.stderr)
        return 2

    torch.manual_seed(args.seed)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = ParlerTTSForConditionalGeneration.from_pretrained(args.model).to(device)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    description_tokenizer = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)

    description = args.description or f"{args.speaker} speaks with a clear, expressive voice. The recording is very high quality with no background noise."
    if args.speaker not in description:
        description = f"{args.speaker}: {description}"
    desc = description_tokenizer(description, return_tensors="pt").to(device)
    prompt = tokenizer(args.text, return_tensors="pt").to(device)
    generation = model.generate(
        input_ids=desc.input_ids,
        attention_mask=desc.attention_mask,
        prompt_input_ids=prompt.input_ids,
        prompt_attention_mask=prompt.attention_mask,
    )
    sf.write(args.out, generation.cpu().numpy().squeeze(), model.config.sampling_rate)
    return 0


if __name__ == "__main__":
    sys.exit(main())
