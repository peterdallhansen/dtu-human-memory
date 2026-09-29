from config import free_recall, final_experiment, serial_chunking


def test_final_trial_count_matches_documented_design():
    assert final_experiment.TOTAL_TRIALS == 68


def test_final_free_recall_pool_has_unique_length_fifteen_lists():
    for language, lists in free_recall.FINAL_LISTS.items():
        assert len(lists) == 16
        assert all(len(words) == 15 for words in lists.values()), language


def test_final_chunking_pool_has_nine_letter_bases():
    for language, bases in serial_chunking.FINAL_BASES.items():
        assert len(bases) == 16
        assert all(len(groups) == 3 for groups in bases), language
        assert all(len(group) == 3 for groups in bases for group in groups), language
