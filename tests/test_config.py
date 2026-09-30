from random import Random
from types import SimpleNamespace

from config import free_recall, final_experiment, serial_chunking
from pilot import (
    EXPERIMENT_TRIAL_COUNTS,
    PILOT_CHUNKING_CONDITIONS,
    TOTAL_TRIALS,
    make_chunked_groups,
    make_nonchunked_groups,
    make_random_free_recall_lists,
    parse_args,
)


def test_final_trial_count_matches_documented_design():
    assert final_experiment.TOTAL_TRIALS == 14
    assert len(final_experiment.EXPERIMENTS["free_recall"]) == 4
    assert final_experiment.EXPERIMENTS["capacity"]["lengths"] == [4, 6, 8, 10]
    assert len(final_experiment.EXPERIMENTS["phonological"]) == 4
    assert final_experiment.EXPERIMENTS["chunking"]["groups_per_trial"] == 6
    assert len(final_experiment.EXPERIMENTS["chunking"]["conditions"]) == 2
    assert not hasattr(final_experiment, "BREAK_EVERY_TRIALS")
    assert not hasattr(final_experiment, "TRIALS_PER_REPETITION")


def test_free_recall_vocabulary_is_flat_and_unique():
    for language, words in free_recall.VOCABULARY.items():
        assert len(words) >= free_recall.LIST_LENGTH, language
        assert len(words) == len(set(words)), language
        assert all(isinstance(word, str) and word for word in words), language


def test_pilot_free_recall_samples_distinct_words_from_full_pool():
    experiment = SimpleNamespace(language="en", rng=Random(1234))

    sampled_lists = make_random_free_recall_lists(experiment)
    sampled_words = [word for _, words in sampled_lists for word in words]
    vocabulary = set(free_recall.VOCABULARY["en"])

    assert len(sampled_lists) == len(free_recall.CONDITIONS)
    assert all(len(words) == free_recall.LIST_LENGTH for _, words in sampled_lists)
    assert len(sampled_words) == len(set(sampled_words))
    assert set(sampled_words) <= vocabulary


def test_pilot_cli_selects_a_single_experiment():
    assert parse_args(["--experiment", "chunking"]).experiment == ["chunking"]
    assert parse_args(["--experiment", "chunking", "phonological"]).experiment == [
        "chunking",
        "phonological",
    ]
    assert parse_args(["--experiment", "chunking", "chunking"]).experiment == [
        "chunking",
        "chunking",
    ]
    assert parse_args([]).experiment == ["all"]
    assert TOTAL_TRIALS == sum(EXPERIMENT_TRIAL_COUNTS.values())


def test_chunking_pools_have_unique_three_letter_chunks():
    for language, chunks in serial_chunking.BASES.items():
        assert len(chunks) >= serial_chunking.GROUPS_PER_TRIAL, language
        assert len(chunks) == len(set(chunks)), language
        assert all(len(chunk) == serial_chunking.LETTERS_PER_GROUP for chunk in chunks)

    assert PILOT_CHUNKING_CONDITIONS == [
        "chunked",
        "chunked",
        "chunked",
        "nonchunked",
        "nonchunked",
        "nonchunked",
    ]
    assert EXPERIMENT_TRIAL_COUNTS["chunking"] == 6


def test_chunking_permutations_preserve_real_chunks_and_letters():
    experiment = SimpleNamespace(language="en", rng=Random(1234))
    groups = make_chunked_groups(experiment, "en")
    real = make_chunked_groups(
        SimpleNamespace(language="en", rng=Random(5678)),
        "en",
    )
    fake = make_nonchunked_groups(
        SimpleNamespace(language="en", rng=Random(1234)),
        groups,
    )
    real_chunks = set(serial_chunking.BASES["en"])

    assert len(groups) == serial_chunking.GROUPS_PER_TRIAL
    assert len(real) == serial_chunking.GROUPS_PER_TRIAL
    assert set(groups) <= real_chunks
    assert set(real) <= real_chunks
    assert len(fake) == serial_chunking.GROUPS_PER_TRIAL
    assert all(group not in real_chunks for group in fake)
    assert sorted("".join(fake)) == sorted("".join(groups))
