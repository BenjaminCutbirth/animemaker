# Google Colab Quickstart

This guide walks through a minimal setup for experimenting with the `animemaker` planning
pipeline inside a fresh [Google Colab](https://colab.research.google.com/) runtime.

## 1. Prepare the environment

1. Open a new Colab notebook.
2. Update `pip` (optional but recommended) and install the package directly from GitHub.
   Replace `YOUR_GITHUB_USERNAME` with the owner of the repository you forked or cloned.

   ```python
   %pip install --upgrade pip
   %pip install git+https://github.com/YOUR_GITHUB_USERNAME/animemaker.git
   ```

   If you are working from an unpublished repository, upload a `.zip` export to Colab and
   run `pip install animemaker-<version>.zip` instead.

## 2. Verify the installation

After the installation finishes, import the package to confirm it is available.

```python
import animemaker
animemaker.__version__
```

A version string should be displayed without errors.

## 3. Run the demo planner

The repository ships with a lightweight CLI utility that exercises the pipeline end-to-end.
Clone the repository (or mount Google Drive) if you need local access to the example script.

```python
!git clone https://github.com/YOUR_GITHUB_USERNAME/animemaker.git
%cd animemaker
!python examples/colab_demo.py --duration 120 --prompt "High-energy mecha battle" --frame-rate 12
```

The script prints a JSON summary of the planned episode structure so you can verify the
pacing, storyboard beats, visual plan, and audio cues produced by the default planners.

## 4. Experiment with your own inputs

Update the arguments passed to `colab_demo.py` to try different prompts, durations,
reference images, or manga pages stored in the Colab runtime. For example:

```python
!python examples/colab_demo.py \
    --duration 180 \
    --prompt "Slice-of-life cafe scene with gentle piano" \
    --reference-images sample_frame1.png sample_frame2.png \
    --manga-pages chapter1_page1.png chapter1_page2.png
```

The CLI displays the generated storyboard synopsis, beat descriptions, and high-level
rendering strategy so you can inspect how the pipeline adapts to your inputs before wiring
it into a larger workflow.

---

Need a shareable notebook instead? Use `File → Save a copy in Drive` after following these
steps to keep your configuration for later reuse.
