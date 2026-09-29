import numpy as np

from analysis_utils import (
    bootstrap_difference,
    bootstrap_mean,
    completed_trials,
    parse_binary_list,
    serial_error_counts,
    skipped_trial_count,
)


def test_parse_binary_list_returns_integers():
    assert parse_binary_list("[1, 0, 1]") == [1, 0, 1]
    assert parse_binary_list("") == []
    assert parse_binary_list("not a list") == []


def test_bootstrap_mean_handles_small_samples():
    estimate, lower, upper = bootstrap_mean([1, 2, 3], n_boot=500)

    assert estimate == 2.0
    assert lower <= estimate <= upper

    estimate, lower, upper = bootstrap_mean([1])
    assert estimate == 1.0
    assert np.isnan(lower)
    assert np.isnan(upper)


def test_bootstrap_difference_is_a_minus_b():
    estimate, _, _ = bootstrap_difference([1, 2, 3], [0, 1, 2], n_boot=500)

    assert estimate == 1.0


def test_serial_error_counts_are_position_based():
    counts = serial_error_counts("ABCD", "ABXC")

    assert counts == {
        "correct": 2,
        "omission": 0,
        "transposition": 1,
        "intrusion": 1,
    }


def test_skipped_trials_are_excluded_from_analysis_rows():
    import pandas as pd

    data = pd.DataFrame({"accuracy": [1.0, ""], "skipped": [0, 1]})

    assert skipped_trial_count(data) == 1
    assert len(completed_trials(data)) == 1
