"""Run the standard analysis pipeline on final experiment sessions."""

from pathlib import Path

from analysis_utils import (
    analyse_capacity as _analyse_capacity,
    analyse_chunking as _analyse_chunking,
    analyse_errors as _analyse_errors,
    analyse_free_recall as _analyse_free_recall,
    analyse_phonological as _analyse_phonological,
    bootstrap_difference,
    bootstrap_mean,
    load_data as _load_data,
    make_paper_figures as _make_paper_figures,
    parse_binary_list,
    pilot_checks as _pilot_checks,
    serial_error_counts,
)
from analysis_utils import run_analysis


DATA_DIR = Path("data") / "final"
OUT_DIR = Path("final_analysis")
FILE_PATTERN = "final_*.csv"


def load_data():
    """Load final-session files using the current module-level paths."""
    return _load_data(DATA_DIR, FILE_PATTERN)


def analyse_free_recall(df):
    return _analyse_free_recall(df, OUT_DIR)


def analyse_capacity(df):
    return _analyse_capacity(df, OUT_DIR)


def analyse_phonological(df):
    return _analyse_phonological(df, OUT_DIR)


def analyse_chunking(df):
    return _analyse_chunking(df, OUT_DIR)


def analyse_errors(df):
    return _analyse_errors(df, OUT_DIR)


def pilot_checks(df):
    return _pilot_checks(df, OUT_DIR)


def make_paper_figures(df):
    """Export the composite figures and vector files used by the paper."""
    return _make_paper_figures(df, OUT_DIR)


def main():
    run_analysis(DATA_DIR, OUT_DIR, FILE_PATTERN, dataset_name="final experiment")


if __name__ == "__main__":
    main()
