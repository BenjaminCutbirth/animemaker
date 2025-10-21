"""Audio planning utilities for the AI-assisted anime pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .preprocessing import PreprocessedInputs
from .storyboard import Storyboard


@dataclass(slots=True)
class AudioCue:
    """Represents a unit of sound to be generated."""

    beat_index: int
    cue_type: str
    description: str


@dataclass(slots=True)
class AudioPlan:
    """Collection of cues including dialogue, music, and effects."""

    cues: List[AudioCue]

    def dialogue_cues(self) -> List[AudioCue]:
        return [cue for cue in self.cues if cue.cue_type == "dialogue"]


class AudioPlanner:
    """Derive the sound design requirements for the episode."""

    def build(self, inputs: PreprocessedInputs, storyboard: Storyboard) -> AudioPlan:
        cues: List[AudioCue] = []
        for index, _ in enumerate(storyboard.beats):
            if inputs.prompt:
                cues.append(
                    AudioCue(
                        beat_index=index,
                        cue_type="dialogue",
                        description=f"Dialogue inspired by: {inputs.prompt[:60]}",
                    )
                )
            cues.append(
                AudioCue(
                    beat_index=index,
                    cue_type="music",
                    description="Dynamic score matched to beat energy",
                )
            )
        return AudioPlan(cues=cues)
