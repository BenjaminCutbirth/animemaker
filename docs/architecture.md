# Animemaker Planning Architecture

This repository sketches the orchestration layer required to turn arbitrary
inputs (text prompts, images, or sequential art) into a structured plan for
producing long-form animated content. The objective is to de-risk the
engineering effort by capturing how each subsystem should interact before
investing in expensive model training.

## Pipeline overview

1. **Preprocessing** – Normalises prompts, deduplicates reference imagery, and
   slices manga/manhwa pages into panel placeholders that can later be
   inpainted and animated.
2. **Storyboarding** – Generates a synopsis and a list of beats that span the
   desired duration. Beats are kept evenly distributed for now, but the module
   is designed to accept richer story graphs in the future.
3. **Visual planning** – Chooses the appropriate generation technique for each
   beat (text-to-video, image-to-video, or panel animation) and records which
   assets each scene depends on.
4. **Audio planning** – Drafts cues for dialogue, music, and ambience that will
   be fulfilled by text-to-speech or generative music models.

The :class:`animemaker.pipeline.AnimationPipeline` ties these components
together and returns an :class:`animemaker.pipeline.AnimationProject` summary
that downstream services can consume.

## Extending the prototype

* Swap the stub preprocessing helpers for full computer vision pipelines that
  remove text bubbles, separate foreground characters, and run camera motion
  estimation.
* Replace the simple beat generator with an LLM-backed writer that produces
  scripts, shot lists, and dialogue.
* Connect the visual planner to diffusion or NeRF based render farms, possibly
  backed by ControlNet-like conditioning for manga panels.
* Integrate character-voice cloning and generative music models into the audio
  planner to emit precise cues with timing metadata.

## Testing strategy

The unit tests focus on verifying that the orchestration behaves deterministically
and that duration constraints propagate correctly. As the project grows the test
suite should incorporate golden files for storyboard and audio plans alongside
smoke tests for the heavier model integrations.
