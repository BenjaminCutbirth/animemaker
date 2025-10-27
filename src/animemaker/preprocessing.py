"""Preprocessing tools for preparing user inputs before generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass(slots=True)
class PreprocessedInputs:
    """Container for assets extracted or normalized from user inputs."""

    prompt: str | None
    duration_seconds: int
    reference_images: List[Path] = field(default_factory=list)
    manga_panels: List[Path] = field(default_factory=list)

    def total_visual_assets(self) -> int:
        """Return the number of prepared visual assets."""

        return len(self.reference_images) + len(self.manga_panels)


def normalise_prompt(prompt: str | None) -> str | None:
    """Lightweight normalisation for user prompts.

    For now this trims whitespace and converts empty strings to ``None``. In a
    production system this is where we would expand abbreviations, translate
    language variants, or query a long-form script writer.
    """

    if prompt is None:
        return None

    clean = prompt.strip()
    return clean or None


def collect_reference_images(paths: Sequence[str | Path]) -> List[Path]:
    """Validate and coerce user reference image inputs into :class:`Path` objects.

    This stub does not touch the filesystem; it simply records the desired
    assets. The downstream renderer would be responsible for loading or
    uploading the real files.
    """

    unique_paths: List[Path] = []
    seen = set()
    for raw in paths:
        path = Path(raw)
        if path in seen:
            continue
        seen.add(path)
        unique_paths.append(path)
    return unique_paths


def slice_manga_into_panels(pages: Iterable[str | Path]) -> List[Path]:
    """Represent the manga or manhwa pages that should be animated.

    A future implementation would detect panel boundaries, remove text bubbles,
    and inpaint the underlying artwork. The simplified stub mirrors those
    outputs so downstream planning logic can be exercised in tests.
    """

    panels: List[Path] = []
    for index, raw in enumerate(pages, start=1):
        panels.append(Path(raw).with_suffix(f".panel{index:03d}.png"))
    return panels


def prepare_inputs(
    *,
    prompt: str | None,
    duration_seconds: int,
    reference_images: Sequence[str | Path],
    manga_pages: Sequence[str | Path],
) -> PreprocessedInputs:
    """Aggregate all preprocessing tasks into a single call.

    The pipeline object uses this helper so unit tests can supply deterministic
    fixtures without standing up the real computer vision stack.
    """

    normalised_prompt = normalise_prompt(prompt)
    images = collect_reference_images(reference_images)
    panels = slice_manga_into_panels(manga_pages)
    return PreprocessedInputs(
        prompt=normalised_prompt,
        duration_seconds=duration_seconds,
        reference_images=images,
        manga_panels=panels,
    )
