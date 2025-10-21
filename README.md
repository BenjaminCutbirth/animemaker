# Animemaker

Animemaker is a planning toolkit for building an AI system that can generate
full-length animated episodes from a variety of inputs: natural language
prompts, reference images, or manga/manhwa pages. The code focuses on the
orchestration layer so that the heavy model work can be developed iteratively.

## Features

- **Preprocessing stubs** for normalising prompts, deduplicating reference
  imagery, and representing manga panels without speech bubbles.
- **Storyboard planner** that stretches a synopsis across the requested
  duration to yield a beat list suitable for downstream shot planning.
- **Visual planner** that decides whether to lean on text-to-video, image-to-
  video, or panel animation techniques for each beat and records dependent
  assets.
- **Audio planner** that drafts dialogue and music cues to cover the entire
  episode.
- **Pipeline orchestrator** tying everything together into a single project
  summary that other services can execute.

## Getting started

Install the package in editable mode and run the test suite:

```bash
pip install -e .
pytest
```

## Next steps

The current implementation is intentionally lightweight. Replace the stubs with
real computer vision, generative video, and audio models to achieve the goal of
rapidly producing anime episodes from textual and visual inspiration.
