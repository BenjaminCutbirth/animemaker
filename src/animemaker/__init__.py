"""High-level package exports for the Animemaker planning toolkit."""

from .pipeline import AnimationPipeline, AnimationProject, AnimationRequest

__version__ = "0.1.0"

__all__ = [
    "AnimationPipeline",
    "AnimationProject",
    "AnimationRequest",
    "__version__",
]
