"""Visual planning for the AI-assisted animation pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .preprocessing import PreprocessedInputs
from .storyboard import Storyboard


@dataclass(slots=True)
class VisualAssetPlan:
    """Describe how each scene will be visualised."""

    beat_index: int
    technique: str
    asset_references: List[str] = field(default_factory=list)


@dataclass(slots=True)
class VisualPlan:
    """Aggregate of all visual asset plans."""

    frame_rate: int
    resolution: tuple[int, int]
    scenes: List[VisualAssetPlan]

    def as_dict(self) -> Dict[str, object]:
        return {
            "frame_rate": self.frame_rate,
            "resolution": self.resolution,
            "scenes": [scene.__dict__ for scene in self.scenes],
        }


class VisualPlanner:
    """Plan the generation strategy for each storyboard beat."""

    def __init__(self, *, default_frame_rate: int = 24, resolution: tuple[int, int] = (1920, 1080)) -> None:
        self.default_frame_rate = default_frame_rate
        self.resolution = resolution

    def build(self, inputs: PreprocessedInputs, storyboard: Storyboard) -> VisualPlan:
        scenes: List[VisualAssetPlan] = []
        for index, _ in enumerate(storyboard.beats):
            technique = self._choose_technique(inputs)
            references = self._list_references(inputs)
            scenes.append(
                VisualAssetPlan(
                    beat_index=index,
                    technique=technique,
                    asset_references=references,
                )
            )
        return VisualPlan(
            frame_rate=self.default_frame_rate,
            resolution=self.resolution,
            scenes=scenes,
        )

    def _choose_technique(self, inputs: PreprocessedInputs) -> str:
        if inputs.manga_panels:
            return "panel-animation"
        if inputs.reference_images:
            return "image-to-video-diffusion"
        return "text-to-video-diffusion"

    def _list_references(self, inputs: PreprocessedInputs) -> List[str]:
        references = [str(path) for path in inputs.reference_images]
        references.extend(str(panel) for panel in inputs.manga_panels)
        return references
