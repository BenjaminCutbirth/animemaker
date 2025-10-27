"""Colab-friendly entry point for experimenting with the animemaker pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from animemaker.pipeline import AnimationPipeline, AnimationRequest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--duration",
        type=int,
        required=True,
        help="Target duration of the planned episode in seconds.",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Textual concept or storyline for the episode.",
    )
    parser.add_argument(
        "--reference-images",
        nargs="*",
        default=(),
        metavar="IMAGE",
        help="Optional list of reference image file paths accessible in the Colab runtime.",
    )
    parser.add_argument(
        "--manga-pages",
        nargs="*",
        default=(),
        metavar="PAGE",
        help="Optional list of manga or manhwa page image paths to animate.",
    )
    parser.add_argument(
        "--frame-rate",
        type=int,
        default=24,
        help="Desired animation frame rate (frames per second).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="Output frame width in pixels.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Output frame height in pixels.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to store the generated plan JSON.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    request = AnimationRequest(
        duration_seconds=args.duration,
        prompt=args.prompt,
        reference_images=args.reference_images,
        manga_pages=args.manga_pages,
        frame_rate=args.frame_rate,
        resolution=(args.width, args.height),
    )
    pipeline = AnimationPipeline()
    project = pipeline.plan(request)
    summary = project.summary()
    output_json = json.dumps(summary, indent=2)

    if args.output:
        args.output.write_text(output_json, encoding="utf-8")
        print(f"Saved plan to {args.output.resolve()}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
