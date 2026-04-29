# Report Folder

This folder contains the final submission documents for the project.

## Files in This Folder

Main report:
- `report.docx`

Main presentation:
- `presentation.pptx`

Supporting assets:
- `assets/workflow.png`
- `assets/demo_strip.png`

External result figure used by the documents:
- `../experiments/results/plots.png`

## Source of the Documents

These files are generated from:
- `../scripts/generate_report_docx.py`
- `../scripts/generate_presentation.py`
- `../scripts/generate_submission_assets.py`

## Regeneration Workflow

If benchmark values or visual assets change, regenerate in this order:

```bash
python src/main.py --mode benchmark
python src/main.py --mode demo
python scripts/generate_submission_assets.py
python scripts/generate_report_docx.py
python scripts/generate_presentation.py
```

## Final Check

- verify that `report.docx` uses the latest values from `../experiments/results/runtime.csv`
- verify that `presentation.pptx` uses the latest plot and workflow images
- verify that the figures are readable and not text-overlapped
- fill in any remaining manual placeholders such as the instructor name
