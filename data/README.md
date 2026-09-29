# Local Data

The experiment writes pilot CSV files directly to this directory and final
session CSV files to `data/final/`. These files may contain participant IDs,
typed responses, timestamps, and behavioural measurements, so CSV files are
ignored by Git in this project.

Before sharing any data, de-identify it and confirm that release is allowed by
the relevant consent and research approvals. The analysis scripts read local
files matching `pilot_*.csv` or `final_*.csv` and do not download data.
