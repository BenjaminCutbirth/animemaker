"""High level orchestration for planning an AI-generated anime episode."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from . import audio, preprocessing, rendering, storyboard


@dataclass(slots=True)
class AnimationRequest:
    """User supplied configuration for a generated episode."""

    duration_seconds: int
    prompt: Optional[str] = None
    reference_images: Sequence[str] = ()
    manga_pages: Sequence[str] = ()
    frame_rate: int = 24
    resolution: tuple[int, int] = (1920, 1080)

    def __post_init__(self) -> None:
        if self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be positive")
        if self.frame_rate <= 0:
            raise ValueError("frame_rate must be positive")


@dataclass(slots=True)
class AnimationProject:
    """Planned episode outcome before rendering begins."""

    request: AnimationRequest
    preprocessed: preprocessing.PreprocessedInputs
    storyboard: storyboard.Storyboard
    visual_plan: rendering.VisualPlan
    audio_plan: audio.AudioPlan

    def summary(self) -> dict[str, object]:
        """Return a serialisable snapshot of the project plan."""

        return {
            "duration": self.preprocessed.duration_seconds,
            "synopsis": self.storyboard.synopsis,
            "beats": [beat.description for beat in self.storyboard.beats],
            "visual": self.visual_plan.as_dict(),
            "audio": [cue.__dict__ for cue in self.audio_plan.cues],
        }


class AnimationPipeline:
    """Coordinate preprocessing, planning, and resource estimation."""

    def __init__(
        self,
        *,
        storyboard_planner: Optional[storyboard.StoryboardPlanner] = None,
        visual_planner: Optional[rendering.VisualPlanner] = None,
        audio_planner: Optional[audio.AudioPlanner] = None,
    ) -> None:
        self.storyboard_planner = storyboard_planner or storyboard.StoryboardPlanner()
        self.visual_planner = visual_planner or rendering.VisualPlanner()
        self.audio_planner = audio_planner or audio.AudioPlanner()

    def plan(self, request: AnimationRequest) -> AnimationProject:
        """Produce a structured plan for the requested animation."""

        preprocessed = preprocessing.prepare_inputs(
            prompt=request.prompt,
            duration_seconds=request.duration_seconds,
            reference_images=request.reference_images,
            manga_pages=request.manga_pages,
        )
        board = self.storyboard_planner.build(preprocessed)
        visuals = self.visual_planner.build(preprocessed, board)
        audio_plan = self.audio_planner.build(preprocessed, board)
        return AnimationProject(
            request=request,
            preprocessed=preprocessed,
            storyboard=board,
            visual_plan=visuals,
            audio_plan=audio_plan,
        )
