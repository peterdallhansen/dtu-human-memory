"""Design settings for the full memory experiment."""

from . import serial_chunking

EXPERIMENTS = {
    "free_recall": [
        {
            "condition": "slow_immediate",
            "word_duration": 2.0,
            "list_length": 15,
            "post_task": "immediate",
        },
        {
            "condition": "fast_immediate",
            "word_duration": 0.75,
            "list_length": 15,
            "post_task": "immediate",
        },
        {
            "condition": "slow_wm",
            "word_duration": 2.0,
            "list_length": 15,
            "post_task": "working_memory",
        },
        {
            "condition": "slow_pause",
            "word_duration": 2.0,
            "list_length": 15,
            "post_task": "pause",
        },
    ],
    "capacity": {
        "lengths": [4, 6, 8, 10],
    },
    "phonological": [
        {
            "condition": "confusable",
            "secondary_task": "normal",
            "number_of_letters": 6,
        },
        {
            "condition": "nonconfusable",
            "secondary_task": "normal",
            "number_of_letters": 6,
        },
        {
            "condition": "nonconfusable",
            "secondary_task": "suppression",
            "number_of_letters": 6,
        },
        {
            "secondary_task": "tapping",
            "condition": "nonconfusable",
            "number_of_letters": 6,
        },
    ],
    "chunking": {
        "groups_per_trial": 6,
        "letters_per_group": 3,
        "conditions": ["chunked", "nonchunked"],
    },
}


def trial_count(settings):
    if isinstance(settings, list):
        return len(settings)
    if "lengths" in settings:
        return len(settings["lengths"])
    if "conditions" in settings:
        return len(settings["conditions"])
    return 1


TOTAL_TRIALS = sum(trial_count(settings) for settings in EXPERIMENTS.values())

EXPERIMENT_VERSION = "final_v9"
