# Scripts

This folder contains utility scripts used to regenerate figures, reports, and slide decks for the project submission.

## Files

`generate_submission_assets.py`
- Generates document-ready assets from project outputs.
- Currently produces:
  - `report/assets/workflow.png`
  - `report/assets/demo_strip.png`
- Reads:
  - `demo/synthetic_bicep_curl.mp4`
  - repository metadata needed to draw the workflow figure

`generate_report_docx.py`
- Generates the formal Word report.
- Current primary output:
  - `report/report.docx`
- Reads:
  - `experiments/results/runtime.csv`
  - `experiments/results/plots.png`
  - `report/assets/workflow.png`
  - `report/assets/demo_strip.png`

`generate_presentation.py`
- Generates the English PowerPoint presentation.
- Current primary output:
  - `report/presentation.pptx`
- Reads:
  - `experiments/results/runtime.csv`
  - `experiments/results/plots.png`
  - `report/assets/workflow.png`
  - `report/assets/demo_strip.png`

`generate_presentation_th.py`
- Generates an optional Thai-language PowerPoint deck.
- This script is kept in the repository for alternative presentation output, but its result is not part of the current default `report/` submission set.

`submission_metrics.py`
- Shared benchmark metadata loader used by the document generators.
- Reads:
  - `experiments/results/runtime.csv`

## Typical Usage

If you only need to refresh report figures:

```bash
python scripts/generate_submission_assets.py
```

If you need to regenerate the benchmark and all documents:

```bash
python src/main.py --mode benchmark
python src/main.py --mode demo
python scripts/generate_submission_assets.py
python scripts/generate_report_docx.py
python scripts/generate_presentation.py
```

## Notes

- These scripts assume they are run from the repository root.
- They use repository-relative paths internally, so moving them without updating path logic will break generation.
- If a target `.docx` or `.pptx` file is open in Word or PowerPoint, regeneration may fail due to a file lock.
- `generate_submission_assets.py` should be run after `python src/main.py --mode demo` so the latest demo video exists before extracting `demo_strip.png`.
