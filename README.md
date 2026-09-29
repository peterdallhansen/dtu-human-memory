# Human Memory Mini Project

PsychoPy pilot and final experiment for the DTU Human Memory Mini Project.

## Install

Python 3.11 is recommended.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run

Run the pilot from the project root:

```bash
python pilot.py
```

Run the final experiment after checking the pilot:

```bash
python experiment.py
```

Both runners save CSV files under `data/`.

On the trial instruction screen, click the `SKIP TRIAL` button in the
lower-right corner to move directly to the next trial. The button is not shown
during stimulus presentation or response entry, so it does not distract from
the task. The skipped trial is saved with `skipped=1` and excluded from
analysis summaries. `Escape` still quits the session.

## Analyse

```bash
python analyze_pilot.py
python analyze_experiment.py
```

Results are written to `pilot_analysis/` or `final_analysis/`.

The same pipelines are available interactively in `analyze_pilot.ipynb` and
`analyze_experiment.ipynb`. Both notebooks use `analysis_utils.py`, which
contains the shared loading, scoring, bootstrap, export, and quality-check
logic. `analyze_final.py` remains as a compatibility alias for
`analyze_experiment.py`.

## Test

```bash
python -m pytest
```

GitHub Actions runs the tests and a syntax check without opening PsychoPy.

## Data

Collected CSV files may contain participant identifiers and behavioural data.
They are ignored by Git. Do not publish them without de-identification and
the required consent and research approval.
