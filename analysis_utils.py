"""Shared analysis functions for pilot and final experiment sessions."""

from pathlib import Path
import ast
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PAPER_COLORS = {
    "slow_immediate": "#1b4965",
    "fast_immediate": "#ca6702",
    "slow_wm": "#9b2226",
    "slow_pause": "#2a9d8f",
    "confusable": "#9b2226",
    "nonconfusable": "#1b4965",
    "normal": "#1b4965",
    "tapping": "#2a9d8f",
    "suppression": "#ca6702",
    "chunked": "#2a9d8f",
    "nonchunked": "#1b4965",
}

PAPER_LABELS = {
    "slow_immediate": "Immediate",
    "fast_immediate": "Fast presentation",
    "slow_wm": "Working-memory task",
    "slow_pause": "Quiet pause",
    "confusable": "Phonologically similar",
    "nonconfusable": "Phonologically dissimilar",
    "normal": "Normal",
    "tapping": "Finger tapping",
    "suppression": "Articulatory suppression",
    "chunked": "Chunked",
    "nonchunked": "Unchunked",
}


def _paper_style():
    """Use a restrained style suitable for figures imported into a paper."""
    return {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "grid.color": "#d9dde2",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.7,
        "legend.frameon": False,
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    }


def _save_paper_figure(fig, out_dir, stem):
    """Export raster and vector versions for inspection and Overleaf."""
    for extension, kwargs in (("pdf", {}), ("svg", {}), ("png", {"dpi": 300})):
        fig.savefig(
            Path(out_dir) / f"{stem}.{extension}",
            bbox_inches="tight",
            pad_inches=0.03,
            **kwargs,
        )


def _ci_band(ax, x, values, color, label, marker="o"):
    estimates = []
    lowers = []
    uppers = []
    for value in values:
        estimate, lower, upper = bootstrap_mean(value)
        estimates.append(estimate)
        lowers.append(lower)
        uppers.append(upper)
    estimates = np.asarray(estimates, dtype=float)
    lowers = np.asarray(lowers, dtype=float)
    uppers = np.asarray(uppers, dtype=float)
    ax.plot(x, estimates, color=color, marker=marker, linewidth=1.8, markersize=3.8,
            label=label, zorder=3)
    if np.isfinite(lowers).all() and np.isfinite(uppers).all():
        ax.fill_between(x, lowers, uppers, color=color, alpha=0.16, linewidth=0,
                        zorder=1)
    return estimates, lowers, uppers


def _bar_with_ci(ax, summary, order, title, ylabel="Proportion correct"):
    summary = summary.set_index("condition").reindex(order).dropna(how="all").reset_index()
    x = np.arange(len(summary))
    colors = [PAPER_COLORS.get(condition, "#4c566a") for condition in summary["condition"]]
    ax.bar(x, summary["estimate"], color=colors, width=0.62, alpha=0.92)
    error_low = summary["estimate"] - summary["ci95_low"]
    error_high = summary["ci95_high"] - summary["estimate"]
    finite = np.isfinite(error_low) & np.isfinite(error_high)
    if finite.any():
        ax.errorbar(x[finite], summary.loc[finite, "estimate"],
                    yerr=[error_low[finite], error_high[finite]], fmt="none",
                    ecolor="#222222", elinewidth=1, capsize=3, capthick=1, zorder=4)
    ax.set_xticks(x, [PAPER_LABELS.get(c, c) for c in summary["condition"]], rotation=20,
                  ha="right")
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1.05)
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    ax.grid(axis="y")
    return summary


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
        label="Item-level accuracy",
    )
    plt.xlabel("Sequence length")
    plt.ylabel("Proportion of items recalled correctly")
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
            values("nonconfusable", "normal"),
            values("nonconfusable", "suppression"),
        ),
        (
            "Finger-tapping control",
            values("nonconfusable", "normal"),
            values("nonconfusable", "tapping"),
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


def make_paper_figures(df, out_dir):
    """Create the four composite figures described in the paper plan.

    Confidence intervals are percentile bootstrap intervals over completed
    trials. The corresponding CSV files make every plotted value auditable.
    Missing sections are skipped rather than producing misleading empty plots.
    """
    out_dir = _prepare_output_dir(out_dir)
    df = completed_trials(df)
    plt.rcParams.update(_paper_style())

    # Figure 1 and 2: free recall serial-position curves and region effects.
    free = df[df["section"] == "free_recall"].copy()
    curves = []
    regions = []
    for _, row in free.iterrows():
        correctness = parse_binary_list(row.get("position_correct", ""))
        if len(correctness) < 3:
            continue
        curves.extend({
            "condition": row["condition"],
            "position": position,
            "correct": correct,
        } for position, correct in enumerate(correctness, start=1))
        edge = min(4, len(correctness) // 3)
        regions.append({
            "condition": row["condition"],
            "early": np.mean(correctness[:edge]),
            "middle": np.mean(correctness[edge:-edge]),
            "late": np.mean(correctness[-edge:]),
            "primacy": np.mean(correctness[:edge]) - np.mean(correctness[edge:-edge]),
            "recency": np.mean(correctness[-edge:]) - np.mean(correctness[edge:-edge]),
        })

    if curves:
        curves = pd.DataFrame(curves)
        regions = pd.DataFrame(regions)
        position_values = []
        curve_rows = []
        for condition, sub in curves.groupby("condition"):
            positions = sorted(sub["position"].unique())
            position_values.extend(positions)

        fig, ax = plt.subplots(figsize=(6.4, 4.0), constrained_layout=True)
        for condition, sub in curves.groupby("condition"):
            positions = sorted(sub["position"].unique())
            values = [sub.loc[sub["position"] == position, "correct"].values
                      for position in positions]
            estimates, lowers, uppers = _ci_band(
                ax, positions, values, PAPER_COLORS.get(condition, "#4c566a"),
                PAPER_LABELS.get(condition, condition))
            curve_rows.extend({
                "condition": condition,
                "position": position,
                "estimate": estimate,
                "ci95_low": lower,
                "ci95_high": upper,
                "n_trials": len(values[index]),
            } for index, (position, estimate, lower, upper) in enumerate(
                zip(positions, estimates, lowers, uppers)
            ))
        ax.set_title("Free-recall serial-position curves", loc="left", fontweight="bold")
        ax.set_xlabel("Word position")
        ax.set_ylabel("Proportion recalled")
        ax.set_ylim(0, 1.05)
        ax.set_xlim(min(position_values) - 0.3, max(position_values) + 0.3)
        ax.set_xticks(position_values)
        ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
        ax.grid(axis="y")
        ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.17))
        _save_paper_figure(fig, out_dir, "figure_1_free_recall")
        plt.close(fig)
        pd.DataFrame(curve_rows).to_csv(out_dir / "figure_1_free_recall.csv", index=False)

        region_rows = []
        for condition, sub in regions.groupby("condition"):
            for metric in ("early", "middle", "late", "primacy", "recency"):
                estimate, lower, upper = bootstrap_mean(sub[metric].values)
                region_rows.append({
                    "condition": condition,
                    "metric": metric,
                    "estimate": estimate,
                    "ci95_low": lower,
                    "ci95_high": upper,
                    "n_trials": len(sub),
                })
        region_summary = pd.DataFrame(region_rows)
        region_summary.to_csv(out_dir / "figure_2_free_recall_effects.csv", index=False)

        fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.2), sharey=True,
                                 constrained_layout=True)
        for ax, metric, title, order in (
            (axes[0], "primacy", "A  Primacy effect", ["slow_immediate", "fast_immediate"]),
            (axes[1], "recency", "B  Recency effect",
             ["slow_immediate", "slow_wm", "slow_pause"]),
        ):
            _bar_with_ci(
                ax,
                region_summary[region_summary["metric"] == metric].rename(
                    columns={"estimate": "estimate", "ci95_low": "ci95_low",
                             "ci95_high": "ci95_high"}),
                order,
                title,
                ylabel="Effect relative to middle",
            )
            ax.axhline(0, color="#222222", linewidth=0.8)
        axes[0].set_ylabel("Proportion difference")
        _save_paper_figure(fig, out_dir, "figure_2_primacy_recency")
        plt.close(fig)

    # Figure 3: item-level accuracy is the primary capacity measure.
    capacity = df[df["section"] == "serial_capacity"].copy()
    if not capacity.empty:
        rows = []
        for length, sub in capacity.groupby("sequence_length"):
            values = pd.to_numeric(sub["accuracy"], errors="coerce").dropna().values
            estimate, lower, upper = bootstrap_mean(values)
            rows.append({"sequence_length": int(length), "estimate": estimate,
                         "ci95_low": lower, "ci95_high": upper, "n_trials": len(values)})
        summary = pd.DataFrame(rows).sort_values("sequence_length")
        summary.to_csv(out_dir / "figure_3_serial_capacity.csv", index=False)
        fig, ax = plt.subplots(figsize=(5.4, 3.7), constrained_layout=True)
        x = summary["sequence_length"].to_numpy()
        ax.plot(x, summary["estimate"], color="#1b4965", marker="o", linewidth=1.8,
                markersize=5)
        if summary["ci95_low"].notna().all():
            ax.fill_between(x, summary["ci95_low"], summary["ci95_high"],
                            color="#1b4965", alpha=0.16, linewidth=0)
        ax.set_title("Serial-recall capacity", loc="left", fontweight="bold")
        ax.set_xlabel("Sequence length")
        ax.set_ylabel("Proportion of items recalled correctly")
        ax.set_ylim(0, 1.05)
        ax.set_xticks(x)
        ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
        ax.grid(axis="y")
        _save_paper_figure(fig, out_dir, "figure_3_serial_capacity")
        plt.close(fig)

    # Figure 4: phonological similarity, error composition, chunking, and controls.
    phonological = df[df["section"] == "serial_phonological"].copy()
    chunking = df[df["section"] == "serial_chunking"].copy()
    if not phonological.empty or not chunking.empty:
        fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.6), constrained_layout=True)

        similarity_rows = []
        for condition, sub in phonological[
            phonological["subcondition"] == "normal"
        ].groupby("condition"):
            estimate, lower, upper = bootstrap_mean(
                pd.to_numeric(sub["accuracy"], errors="coerce")
            )
            similarity_rows.append({
                "condition": condition,
                "estimate": estimate,
                "ci95_low": lower,
                "ci95_high": upper,
            })
        if similarity_rows:
            _bar_with_ci(
                axes[0, 0],
                pd.DataFrame(similarity_rows),
                ["nonconfusable", "confusable"],
                "A  Phonological similarity",
            )
        else:
            axes[0, 0].set_visible(False)

        chunk_rows = []
        for condition, sub in chunking.groupby("condition"):
            estimate, lower, upper = bootstrap_mean(pd.to_numeric(sub["accuracy"], errors="coerce"))
            chunk_rows.append({"condition": condition, "estimate": estimate,
                               "ci95_low": lower, "ci95_high": upper})
        if chunk_rows:
            _bar_with_ci(axes[0, 1], pd.DataFrame(chunk_rows),
                         ["nonchunked", "chunked"], "B  Chunking")
        else:
            axes[0, 1].set_visible(False)

        task_rows = []
        control_phonological = phonological[
            phonological["condition"] == "nonconfusable"
        ]
        for condition, sub in control_phonological.groupby("subcondition"):
            estimate, lower, upper = bootstrap_mean(pd.to_numeric(sub["accuracy"], errors="coerce"))
            task_rows.append({"condition": condition, "estimate": estimate,
                              "ci95_low": lower, "ci95_high": upper})
        if task_rows:
            _bar_with_ci(axes[1, 0], pd.DataFrame(task_rows),
                         ["normal", "tapping", "suppression"],
                         "C  Interference controls (nonconfusable letters)")
        else:
            axes[1, 0].set_visible(False)

        error_rows = []
        for _, row in phonological.iterrows():
            counts = serial_error_counts(str(row["stimulus"]).replace("|", ""), str(row["response"]))
            total_errors = sum(count for kind, count in counts.items() if kind != "correct")
            if total_errors:
                error_rows.extend({"condition": row["subcondition"],
                                   "error_type": error_type, "proportion": count / total_errors}
                                  for error_type, count in counts.items()
                                  if error_type != "correct")
        if error_rows:
            error_summary = pd.DataFrame(error_rows).groupby(["condition", "error_type"])["proportion"].mean().unstack(fill_value=0)
            error_summary = error_summary.reindex(columns=["transposition", "omission", "intrusion"], fill_value=0)
            error_summary.plot(kind="bar", stacked=True, ax=axes[1, 1],
                               color=["#9b2226", "#ca6702", "#6c757d"], width=0.65)
            axes[1, 1].set_title("D  Error composition", loc="left", fontweight="bold")
            axes[1, 1].set_xlabel("")
            axes[1, 1].set_ylabel("Proportion of errors")
            axes[1, 1].set_xticklabels(
                [PAPER_LABELS.get(label, label.title()) for label in error_summary.index],
                rotation=20,
                ha="right",
            )
            axes[1, 1].set_ylim(0, 1.05)
            axes[1, 1].yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
            axes[1, 1].legend(["Order", "Omission", "Intrusion"], loc="upper right", fontsize=7)
            axes[1, 1].grid(axis="y")
        else:
            axes[1, 1].set_visible(False)
        _save_paper_figure(fig, out_dir, "figure_4_serial_manipulations")
        plt.close(fig)


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
    make_paper_figures(df, out_dir)

    print(
        "\nAnalysis complete.\n"
        f"Tables and figures were saved in: {out_dir.resolve()}"
    )
    return df
