"""Storyboard planning utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .preprocessing import PreprocessedInputs


@dataclass(slots=True)
class StoryBeat:
    """A single moment of the planned episode."""

    description: str
    start_time: float
    end_time: float


@dataclass(slots=True)
class Storyboard:
    """Collection of beats and metadata for the episode."""

    beats: List[StoryBeat]
    synopsis: str

    def ensure_duration(self, target_duration: int) -> None:
        """Normalise the final beat to align with the requested duration."""

        if not self.beats:
            return
        self.beats[-1].end_time = float(target_duration)


class StoryboardPlanner:
    """Generate a coarse storyboard from preprocessed inputs."""

    def build(self, inputs: PreprocessedInputs) -> Storyboard:
        synopsis = self._draft_synopsis(inputs)
        beats = self._draft_beats(inputs, synopsis)
        storyboard = Storyboard(beats=beats, synopsis=synopsis)
        storyboard.ensure_duration(inputs.duration_seconds)
        return storyboard

    def _draft_synopsis(self, inputs: PreprocessedInputs) -> str:
        if inputs.prompt:
            return inputs.prompt
        if inputs.manga_panels:
            return "Animated adaptation of provided sequential art"
        if inputs.reference_images:
            return "Original vignette inspired by reference imagery"
        return "Original animation concept"

    def _draft_beats(
        self, inputs: PreprocessedInputs, synopsis: str
    ) -> List[StoryBeat]:
        num_beats = max(3, int(inputs.duration_seconds // 30) or 1)
        segment_length = inputs.duration_seconds / num_beats
        beats: List[StoryBeat] = []
        time_cursor = 0.0
        for index in range(num_beats):
            start_time = time_cursor
            end_time = start_time + segment_length
            description = f"Segment {index + 1}: {synopsis}" if synopsis else "Segment"
            beats.append(StoryBeat(description=description, start_time=start_time, end_time=end_time))
            time_cursor = end_time
        return beats
