"""Unit tests for the high-level animation pipeline."""

from animemaker.pipeline import AnimationPipeline, AnimationRequest


def test_plan_duration_matches_request():
    request = AnimationRequest(
        duration_seconds=120,
        prompt="Epic showdown between hero and rival",
        reference_images=["hero.png"],
    )
    pipeline = AnimationPipeline()
    project = pipeline.plan(request)

    assert project.preprocessed.duration_seconds == request.duration_seconds
    assert project.storyboard.beats[-1].end_time == float(request.duration_seconds)


def test_plan_uses_manga_panels_for_visual_strategy():
    request = AnimationRequest(
        duration_seconds=60,
        manga_pages=["chapter1/page1.png", "chapter1/page2.png"],
    )
    project = AnimationPipeline().plan(request)

    assert project.visual_plan.scenes
    assert all(scene.technique == "panel-animation" for scene in project.visual_plan.scenes)
    assert project.preprocessed.total_visual_assets() == 2
