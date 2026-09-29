import pytest

from runtime import MemoryExperiment, SkipTrial


class FakeMouse:
    def __init__(self, pressed):
        self.pressed = pressed

    def isPressedIn(self, shape, buttons):
        return self.pressed


def make_runtime(pressed=False):
    experiment = MemoryExperiment.__new__(MemoryExperiment)
    experiment.mouse = FakeMouse(pressed)
    experiment.skip_button = object()
    experiment._skip_button_pressed = False
    experiment.trial_index = 0
    return experiment


def test_skip_button_raises_skip_trial():
    experiment = make_runtime(pressed=True)

    with pytest.raises(SkipTrial):
        experiment.check_skip()


def test_skipped_trial_is_saved_and_trial_counter_continues():
    experiment = make_runtime()
    saved_rows = []
    experiment.save_trial = saved_rows.append

    with experiment.trial({
        "section": "serial_capacity",
        "condition": "length_8",
        "notes": "pilot",
    }):
        raise SkipTrial

    assert experiment.trial_index == 1
    assert saved_rows == [{
        "section": "serial_capacity",
        "condition": "length_8",
        "notes": "pilot; skipped",
        "response": "",
        "response_time_s": "",
        "correct_count": "",
        "accuracy": "",
        "whole_sequence_correct": "",
        "position_correct": "",
        "recall_source_positions": "",
        "distractor_start": "",
        "distractor_response": "",
        "distractor_correct_count": "",
        "tap_count": "",
        "tap_times_s": "",
        "skipped": 1,
    }]
