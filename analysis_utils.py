"""Shared analysis functions for pilot and final experiment sessions."""

from pathlib import Path
import ast
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _prepare_output_dir(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def load_data(data_dir, file_pattern):
    """Load and pool all matching session CSV files."""
    data_dir = Path(data_dir)
    files = sorted(data_dir.glob(file_pattern))
    if not files:
        raise FileNotFoundError(
            f"No CSV files found for {file_pattern!r} in {data_dir}. "
            "Run the experiment first."
        )

    frames = []
    empty_columns = None
    for path in files:
        df = pd.read_csv(path)
        if empty_columns is None:
            empty_columns = list(df.columns)
        if df.empty:
            continue
        df["source_file"] = path.name
        frames.append(df)

    if not frames:
        columns = empty_columns or []
        if "source_file" not in columns:
            columns.append("source_file")
        return pd.DataFrame(columns=columns)

    return pd.concat(frames, ignore_index=True)


def skipped_trial_count(df):
    """Return the number of rows explicitly marked as skipped."""
    if "skipped" not in df.columns:
        return 0
    skipped = pd.to_numeric(df["skipped"], errors="coerce").fillna(0)
    return int((skipped == 1).sum())


def completed_trials(df):
    """Return trial rows that contain participant responses or outcomes."""
    if "skipped" not in df.columns:
        return df.copy()
    skipped = pd.to_numeric(df["skipped"], errors="coerce").fillna(0)
    return df.loc[skipped != 1].copy()


def parse_binary_list(value):
    if pd.isna(value) or str(value).strip() == "":
        return []
    try:
        parsed = ast.literal_eval(str(value))
        return [int(item) for item in parsed]
    except Exception:
        return []


def bootstrap_mean(values, n_boot=10000, seed=12345):
    """Return a mean and percentile bootstrap confidence interval."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan, np.nan, np.nan

    estimate = float(np.mean(values))
    if len(values) < 2:
        return estimate, np.nan, np.nan

    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(n_boot, len(values)), replace=True)
    boot_means = samples.mean(axis=1)
    lower, upper = np.quantile(boot_means, [0.025, 0.975])
    return estimate, float(lower), float(upper)


def bootstrap_difference(a, b, n_boot=10000, seed=12345):
    """Return mean(a) - mean(b) and a percentile bootstrap interval."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]

    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan, np.nan

    estimate = float(a.mean() - b.mean())
    if len(a) < 2 or len(b) < 2:
        return estimate, np.nan, np.nan

    rng = np.random.default_rng(seed)
    boot_a = rng.choice(a, size=(n_boot, len(a)), replace=True).mean(axis=1)
    boot_b = rng.choice(b, size=(n_boot, len(b)), replace=True).mean(axis=1)
    lower, upper = np.quantile(boot_a - boot_b, [0.025, 0.975])
    return estimate, float(lower), float(upper)


def serial_error_counts(target, response):
    """Classify position-level serial-recall errors."""
    target = re.sub(r"[\W_]", "", str(target), flags=re.UNICODE).upper()
    response = re.sub(r"[\W_]", "", str(response), flags=re.UNICODE).upper()

    counts = {
        "correct": 0,
        "omission": 0,
        "transposition": 0,
        "intrusion": 0,
    }

    for index, target_item in enumerate(target):
        if index >= len(response):
            counts["omission"] += 1
            continue

        recalled = response[index]
        if recalled == target_item:
            counts["correct"] += 1
        elif recalled in target:
            counts["transposition"] += 1
        else:
            counts["intrusion"] += 1

    if len(response) > len(target):
        counts["intrusion"] += len(response) - len(target)

    return counts


def analyse_free_recall(df, out_dir):
    out_dir = _prepare_output_dir(out_dir)
    free = completed_trials(df)
    free = free[free["section"] == "free_recall"].copy()

    if free.empty:
        print("\nNo free-recall data.")
        return

    curves = []
    trial_regions = []

    for _, row in free.iterrows():
        correctness = parse_binary_list(row["position_correct"])
        if len(correctness) < 12:
            continue

        for position, correct in enumerate(correctness, start=1):
            curves.append({
                "participant_id": row["participant_id"],
                "condition": row["condition"],
                "trial_index": row["trial_index"],
                "position": position,
                "correct": correct,
            })

        early = np.mean(correctness[:4])
        middle = np.mean(correctness[4:-4])
        late = np.mean(correctness[-4:])
        trial_regions.append({
            "participant_id": row["participant_id"],
            "condition": row["condition"],
            "trial_index": row["trial_index"],
            "early": early,
            "middle": middle,
            "late": late,
            "primacy": early - middle,
            "recency": late - middle,
        })

    curves = pd.DataFrame(curves)
    regions = pd.DataFrame(trial_regions)

    if curves.empty:
        print("\nFree-recall rows found, but position data could not be parsed.")
        return

    curve_summary = (
        curves.groupby(["condition", "position"], as_index=False)["correct"]
        .mean()
    )

    plt.figure(figsize=(9, 5))
    for condition, sub in curve_summary.groupby("condition"):
        plt.plot(
            sub["position"],
            sub["correct"],
            marker="o",
            label=condition,
        )

    plt.xlabel("Serial position")
    plt.ylabel("Proportion recalled")
    plt.ylim(-0.05, 1.05)
    max_position = int(curves["position"].max())
    plt.xticks(range(1, max_position + 1))
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "free_recall_serial_position.png", dpi=180)
    plt.close()

    summary_rows = []
    for condition, sub in regions.groupby("condition"):
        for metric in ["early", "middle", "late", "primacy", "recency"]:
            estimate, lower, upper = bootstrap_mean(sub[metric].values)
            summary_rows.append({
                "condition": condition,
                "metric": metric,
                "estimate": estimate,
                "ci95_low": lower,
                "ci95_high": upper,
                "n_trials": len(sub),
            })

    pd.DataFrame(summary_rows).to_csv(
        out_dir / "free_recall_region_summary.csv",
        index=False,
    )

    print("\n=== FREE RECALL: EARLY / MIDDLE / LATE ===")
    print(
        regions.groupby("condition")[
            ["early", "middle", "late", "primacy", "recency"]
        ].mean().round(3)
    )

    def metric_values(condition, metric):
        return regions.loc[regions["condition"] == condition, metric].values

    comparisons = [
        (
            "Presentation-rate effect on primacy",
            "slow_immediate",
            "fast_immediate",
            "primacy",
        ),
        (
            "Presentation-rate control on recency",
            "slow_immediate",
            "fast_immediate",
            "recency",
        ),
        (
            "WM-task effect on recency",
            "slow_immediate",
            "slow_wm",
            "recency",
        ),
        (
            "WM-task selectivity on primacy",
            "slow_immediate",
            "slow_wm",
            "primacy",
        ),
        (
            "Pause control on recency",
            "slow_immediate",
            "slow_pause",
            "recency",
        ),
        (
            "Filled vs unfilled delay on recency",
            "slow_pause",
            "slow_wm",
            "recency",
        ),
    ]

    effect_rows = []
    for label, a, b, metric in comparisons:
        estimate, lower, upper = bootstrap_difference(
            metric_values(a, metric),
            metric_values(b, metric),
        )
        effect_rows.append({
            "comparison": label,
            "metric": metric,
            "A": a,
            "B": b,
            "estimate_A_minus_B": estimate,
            "ci95_low": lower,
            "ci95_high": upper,
        })

    pd.DataFrame(effect_rows).to_csv(
        out_dir / "free_recall_planned_effects.csv",
        index=False,
    )

    print("\n=== FREE RECALL: PLANNED EFFECTS (A - B) ===")
    print(
        pd.DataFrame(effect_rows)[[
            "comparison",
            "estimate_A_minus_B",
            "ci95_low",
            "ci95_high",
        ]].round(3).to_string(index=False)
    )


def analyse_capacity(df, out_dir):
    out_dir = _prepare_output_dir(out_dir)
    capacity = completed_trials(df)
    capacity = capacity[capacity["section"] == "serial_capacity"].copy()

    if capacity.empty:
        print("\nNo capacity data.")
        return

    summary = (
        capacity.groupby("sequence_length")
        .agg(
            mean_position_accuracy=("accuracy", "mean"),
            whole_sequence_accuracy=("whole_sequence_correct", "mean"),
            n_trials=("accuracy", "size"),
        )
        .reset_index()
        .sort_values("sequence_length")
    )
    summary.to_csv(out_dir / "serial_capacity_summary.csv", index=False)

    plt.figure(figsize=(7, 5))
    plt.plot(
        summary["sequence_length"],
        summary["mean_position_accuracy"],
        marker="o",
        label="Position accuracy",
    )
    plt.plot(
        summary["sequence_length"],
        summary["whole_sequence_accuracy"],
        marker="o",
        label="Whole-sequence accuracy",
    )
    plt.xlabel("Sequence length")
    plt.ylabel("Accuracy")
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "serial_capacity.png", dpi=180)
    plt.close()

    print("\n=== SERIAL CAPACITY ===")
    print(summary.round(3).to_string(index=False))


def analyse_phonological(df, out_dir):
    out_dir = _prepare_output_dir(out_dir)
    phonological = completed_trials(df)
    phonological = phonological[
        phonological["section"] == "serial_phonological"
    ].copy()

    if phonological.empty:
        print("\nNo phonological/secondary-task data.")
        return

    summary = (
        phonological.groupby(["condition", "subcondition"])
        .agg(
            mean_accuracy=("accuracy", "mean"),
            whole_sequence_accuracy=("whole_sequence_correct", "mean"),
            mean_taps=("tap_count", "mean"),
            n_trials=("accuracy", "size"),
        )
        .reset_index()
    )
    summary.to_csv(
        out_dir / "phonological_secondary_task_summary.csv",
        index=False,
    )

    print("\n=== PHONOLOGICAL SIMILARITY / SECONDARY TASKS ===")
    print(summary.round(3).to_string(index=False))

    def values(similarity=None, task=None):
        sub = phonological
        if similarity is not None:
            sub = sub[sub["condition"] == similarity]
        if task is not None:
            sub = sub[sub["subcondition"] == task]
        return sub["accuracy"].astype(float).values

    planned = [
        (
            "Phonological similarity effect under normal recall",
            values("nonconfusable", "normal"),
            values("confusable", "normal"),
        ),
        (
            "Articulatory suppression cost",
            values(None, "normal"),
            values(None, "suppression"),
        ),
        (
            "Finger-tapping control",
            values(None, "normal"),
            values(None, "tapping"),
        ),
    ]

    rows = []
    for label, a, b in planned:
        estimate, lower, upper = bootstrap_difference(a, b)
        rows.append({
            "comparison": label,
            "estimate_A_minus_B": estimate,
            "ci95_low": lower,
            "ci95_high": upper,
        })

    pd.DataFrame(rows).to_csv(
        out_dir / "phonological_planned_effects.csv",
        index=False,
    )

    print("\n=== PHONOLOGICAL PLANNED EFFECTS (A - B) ===")
    print(pd.DataFrame(rows).round(3).to_string(index=False))


def analyse_chunking(df, out_dir):
    out_dir = _prepare_output_dir(out_dir)
    chunking = completed_trials(df)
    chunking = chunking[chunking["section"] == "serial_chunking"].copy()

    if chunking.empty:
        print("\nNo chunking data.")
        return

    summary_rows = []
    for condition, sub in chunking.groupby("condition"):
        estimate, lower, upper = bootstrap_mean(
            sub["accuracy"].astype(float).values
        )
        summary_rows.append({
            "condition": condition,
            "mean_accuracy": estimate,
            "ci95_low": lower,
            "ci95_high": upper,
            "n_trials": len(sub),
        })

    summary = pd.DataFrame(summary_rows)
    summary.to_csv(out_dir / "chunking_summary.csv", index=False)

    chunked = chunking.loc[
        chunking["condition"] == "chunked", "accuracy"
    ].astype(float).values
    nonchunked = chunking.loc[
        chunking["condition"] == "nonchunked", "accuracy"
    ].astype(float).values
    estimate, lower, upper = bootstrap_difference(chunked, nonchunked)
    pd.DataFrame([{
        "comparison": "chunked - nonchunked",
        "estimate": estimate,
        "ci95_low": lower,
        "ci95_high": upper,
    }]).to_csv(out_dir / "chunking_effect.csv", index=False)

    print("\n=== CHUNKING ===")
    print(summary.round(3).to_string(index=False))
    print("\nChunking effect (chunked - nonchunked):")
    print(pd.DataFrame([{
        "comparison": "chunked - nonchunked",
        "estimate": estimate,
        "ci95_low": lower,
        "ci95_high": upper,
    }]).round(3).to_string(index=False))


def analyse_errors(df, out_dir):
    out_dir = _prepare_output_dir(out_dir)
    df = completed_trials(df)
    serial = df[df["section"].astype(str).str.startswith("serial_")].copy()
    rows = []

    for _, row in serial.iterrows():
        target = str(row["stimulus"]).replace("|", "")
        response = str(row["response"])
        counts = serial_error_counts(target, response)
        for error_type, count in counts.items():
            rows.append({
                "participant_id": row["participant_id"],
                "section": row["section"],
                "condition": row["condition"],
                "subcondition": row["subcondition"],
                "error_type": error_type,
                "count": count,
            })

    error_df = pd.DataFrame(rows)
    if error_df.empty:
        return

    summary = (
        error_df.groupby(["section", "error_type"])["count"]
        .sum()
        .reset_index()
    )
    summary.to_csv(out_dir / "serial_error_types.csv", index=False)

    print("\n=== SERIAL RECALL ERROR TYPES ===")
    print(summary.to_string(index=False))


def quality_checks(df, out_dir):
    out_dir = _prepare_output_dir(out_dir)
    skipped = skipped_trial_count(df)
    df = completed_trials(df)
    checks = []

    for section, sub in df.groupby("section"):
        mean_accuracy = pd.to_numeric(
            sub["accuracy"],
            errors="coerce",
        ).mean()

        if mean_accuracy > 0.90:
            message = "Possible ceiling: consider making this section harder."
        elif mean_accuracy < 0.10:
            message = "Possible floor: consider making this section easier."
        else:
            message = "Mean accuracy is away from extreme floor/ceiling."

        checks.append({
            "section": section,
            "mean_accuracy": mean_accuracy,
            "check": message,
        })

    tapping = df[
        (df["section"] == "serial_phonological")
        & (df["subcondition"] == "tapping")
    ]
    if not tapping.empty:
        mean_taps = pd.to_numeric(
            tapping["tap_count"],
            errors="coerce",
        ).mean()
        checks.append({
            "section": "finger_tapping_compliance",
            "mean_accuracy": np.nan,
            "check": f"Mean logged taps per tapping trial: {mean_taps:.1f}",
        })

    working_memory = df[
        (df["section"] == "free_recall")
        & (df["condition"] == "slow_wm")
    ]
    if not working_memory.empty:
        mean_correct = pd.to_numeric(
            working_memory["distractor_correct_count"],
            errors="coerce",
        ).mean()
        checks.append({
            "section": "working_memory_compliance",
            "mean_accuracy": np.nan,
            "check": (
                "Mean correctly typed backward-counting responses: "
                f"{mean_correct:.1f}"
            ),
        })

    if skipped:
        checks.append({
            "section": "skipped_trials",
            "mean_accuracy": np.nan,
            "check": f"{skipped} trial(s) skipped and excluded from summaries.",
        })

    checks_df = pd.DataFrame(checks)
    checks_df.to_csv(out_dir / "pilot_checks.csv", index=False)

    print("\n=== QUALITY CHECKS ===")
    print(checks_df.to_string(index=False))


# Kept as an alias because the quality checks are also used for final sessions.
pilot_checks = quality_checks


def run_analysis(data_dir, out_dir, file_pattern, dataset_name):
    """Run all standard analyses and return the pooled trial dataframe."""
    out_dir = _prepare_output_dir(out_dir)
    df = load_data(data_dir, file_pattern)

    if df.empty:
        print(
            f"No completed trial rows found in {data_dir} matching "
            f"{file_pattern!r}."
        )
        return df

    print(
        f"Loaded {len(df)} trials from "
        f"{df['source_file'].nunique()} non-empty {dataset_name} file(s)."
    )
    print(f"Participants: {df['participant_id'].nunique()}")
    skipped = skipped_trial_count(df)
    if skipped:
        print(f"Skipped trials excluded from summaries: {skipped}")

    analyse_free_recall(df, out_dir)
    analyse_capacity(df, out_dir)
    analyse_phonological(df, out_dir)
    analyse_chunking(df, out_dir)
    analyse_errors(df, out_dir)
    quality_checks(df, out_dir)

    print(
        "\nAnalysis complete.\n"
        f"Tables and figures were saved in: {out_dir.resolve()}"
    )
    return df
