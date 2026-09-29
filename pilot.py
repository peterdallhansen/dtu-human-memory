"""Short pilot runner for the human-memory experiment.

Run this file before collecting final data to check timing, instructions,
difficulty, and data saving.
"""

import argparse
import json
import re
from pathlib import Path

from config import common, free_recall, serial_capacity
from config import serial_chunking, serial_phonological


DATA_DIR = Path("data")
EXPERIMENT_VERSION = "pilot_v5"
PILOT_CHUNKING_CONDITIONS = ["chunked"] * 3 + ["nonchunked"] * 3
EXPERIMENT_TRIAL_COUNTS = {
    "free": len(free_recall.CONDITIONS),
    "capacity": len(serial_capacity.LENGTHS),
    "phonological": 2 * len(serial_phonological.SECONDARY_TASKS),
    "chunking": len(PILOT_CHUNKING_CONDITIONS),
}
TOTAL_TRIALS = sum(EXPERIMENT_TRIAL_COUNTS.values())


core = None
MemoryExperiment = None


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Run the human-memory pilot or one of its sections."
    )
    parser.add_argument(
        "--experiment",
        nargs="+",
        action="append",
        choices=("all", *EXPERIMENT_TRIAL_COUNTS),
        default=None,
        metavar="SECTION",
        help="Section(s) to run in order (default: all).",
    )
    args = parser.parse_args(argv)
    selections = (
        [section for group in args.experiment for section in group]
        if args.experiment
        else ["all"]
    )
    if "all" in selections and len(selections) > 1:
        parser.error("'all' cannot be combined with another section")
    args.experiment = selections
    return args


def load_runtime():
    global core, MemoryExperiment

    from psychopy import core as psychopy_core
    from runtime import MemoryExperiment as memory_experiment

    core = psychopy_core
    MemoryExperiment = memory_experiment


def run_working_memory_distractor(experiment, seconds):
    start = experiment.rng.randrange(350, 900)
    response = ""
    clock = core.Clock()
    experiment.clear_key_events()

    while clock.getTime() < seconds:
        remaining = seconds - clock.getTime()
        experiment.small_text.text = experiment.text(
            free_recall,
            "working_memory",
            start=start,
            response=response,
            remaining=remaining,
        )
        experiment.small_text.draw()
        experiment.win.flip()

        keys = experiment.get_keys()
        experiment.check_escape(keys)

        for key in keys:
            name = experiment.key_name(key)
            if name == "backspace":
                response = response[:-1]
            elif name == "space":
                if response and not response.endswith(" "):
                    response += " "
            elif len(name) == 1 and name.isdigit():
                response += name

        core.wait(0.005)

    entered = [int(value) for value in re.findall(r"\d+", response)]
    expected = [start - 3 * (index + 1) for index in range(len(entered))]
    correct = sum(int(actual == wanted) for actual, wanted in zip(entered, expected))
    return start, response.strip(), correct


def run_quiet_pause(experiment, seconds):
    clock = core.Clock()
    try:
        while clock.getTime() < seconds:
            experiment.fixation.draw()
            experiment.small_text.text = experiment.text(free_recall, "pause")
            experiment.small_text.pos = (0, -0.15)
            experiment.small_text.draw()
            experiment.win.flip()
            keys = experiment.get_keys(["escape", "esc"])
            experiment.check_escape(keys)
            core.wait(0.02)
    finally:
        experiment.small_text.pos = (0, 0)


def make_random_free_recall_lists(experiment):
    vocabulary = free_recall.VOCABULARY[experiment.language]
    words_needed = len(free_recall.CONDITIONS) * free_recall.LIST_LENGTH
    sampled_words = experiment.rng.sample(vocabulary, words_needed)

    return [
        (
            f"random_{trial}",
            sampled_words[start : start + free_recall.LIST_LENGTH],
        )
        for trial, start in enumerate(
            range(0, words_needed, free_recall.LIST_LENGTH),
            1,
        )
    ]


def run_free_recall(experiment):
    experiment.show_message(experiment.text(free_recall, "intro"))

    all_lists = make_random_free_recall_lists(experiment)
    conditions = free_recall.CONDITIONS.copy()
    experiment.rng.shuffle(conditions)

    for trial, (condition, (list_id, words)) in enumerate(
        zip(conditions, all_lists),
        1,
    ):
        with experiment.trial(
            {
                "section": "free_recall",
                "condition": condition["condition"],
                "subcondition": condition["post_task"],
                "list_id": list_id,
                "sequence_length": len(words),
                "stimulus": "|".join(words),
                "presentation_duration_s": condition["word_duration"],
                "post_list_delay_s": (
                    common.POST_LIST_DELAY_S
                    if condition["post_task"] != "immediate"
                    else 0.0
                ),
                "notes": "pilot randomized vocabulary",
            }
        ):
            ready = experiment.text(
                free_recall,
                "trial",
                trial=trial,
                total=len(conditions),
            )
            experiment.show_message(ready, allow_skip=True)
            experiment.show_fixation(0.75)

            experiment.present_items(
                words,
                duration=condition["word_duration"],
                isi=common.WORD_ISI,
            )

            distractor_start = ""
            distractor_response = ""
            distractor_correct = ""
            delay_s = 0.0

            if condition["post_task"] == "working_memory":
                distractor_start, distractor_response, distractor_correct = (
                    run_working_memory_distractor(
                        experiment,
                        common.POST_LIST_DELAY_S,
                    )
                )
                delay_s = common.POST_LIST_DELAY_S
            elif condition["post_task"] == "pause":
                run_quiet_pause(experiment, common.POST_LIST_DELAY_S)
                delay_s = common.POST_LIST_DELAY_S

            response, response_time = experiment.typed_response(
                experiment.text(free_recall, "response"),
                max_seconds=common.FREE_RECALL_MAX_RESPONSE_S,
                mode="letters_spaces",
            )
            score = experiment.score_free_recall(words, response)

            experiment.save_trial(
                {
                    "section": "free_recall",
                    "condition": condition["condition"],
                    "subcondition": condition["post_task"],
                    "list_id": list_id,
                    "sequence_length": len(words),
                    "stimulus": "|".join(words),
                    "presentation_duration_s": condition["word_duration"],
                    "post_list_delay_s": delay_s,
                    "response": response,
                    "response_time_s": round(response_time, 3),
                    "correct_count": score["correct_count"],
                    "total_items": len(words),
                    "accuracy": round(score["accuracy"], 4),
                    "whole_sequence_correct": "",
                    "position_correct": json.dumps(score["position_correct"]),
                    "recall_source_positions": json.dumps(score["recall_source_positions"]),
                    "distractor_start": distractor_start,
                    "distractor_response": distractor_response,
                    "distractor_correct_count": distractor_correct,
                    "notes": "pilot randomized vocabulary",
                }
            )
        experiment.maybe_break()


def run_capacity(experiment):
    experiment.show_message(experiment.text(serial_capacity, "intro"))

    lengths = serial_capacity.LENGTHS.copy()
    experiment.rng.shuffle(lengths)

    for length in lengths:
        digits = experiment.rng.sample(list("0123456789"), length)
        with experiment.trial(
            {
                "section": "serial_capacity",
                "condition": f"length_{length}",
                "sequence_length": length,
                "stimulus": "".join(digits),
                "presentation_duration_s": common.SERIAL_ITEM_DURATION,
                "post_list_delay_s": 0,
                "notes": "pilot capacity",
            }
        ):
            experiment.show_message(
                experiment.text(serial_capacity, "trial", length=length),
                allow_skip=True,
            )
            experiment.show_fixation(0.5)
            experiment.present_items(
                digits,
                duration=common.SERIAL_ITEM_DURATION,
                isi=common.SERIAL_ISI,
            )

            response, response_time = experiment.typed_response(
                experiment.text(serial_capacity, "response"),
                max_seconds=common.SERIAL_MAX_RESPONSE_S,
                mode="digits",
            )
            score = experiment.score_serial(digits, response)

            experiment.save_trial(
                {
                    "section": "serial_capacity",
                    "condition": f"length_{length}",
                    "sequence_length": length,
                    "stimulus": "".join(digits),
                    "presentation_duration_s": common.SERIAL_ITEM_DURATION,
                    "post_list_delay_s": 0,
                    "response": score["response_clean"],
                    "response_time_s": round(response_time, 3),
                    "correct_count": score["correct_count"],
                    "total_items": length,
                    "accuracy": round(score["accuracy"], 4),
                    "whole_sequence_correct": score["whole_sequence_correct"],
                    "position_correct": json.dumps(score["position_correct"]),
                    "notes": "pilot capacity",
                }
            )
        experiment.maybe_break()


def run_phonological(experiment):
    experiment.show_message(experiment.text(serial_phonological, "intro"))

    conditions = [
        (similarity, task, letters)
        for similarity, letters in [
            ("confusable", serial_phonological.CONFUSABLE_LETTERS),
            ("nonconfusable", serial_phonological.NONCONFUSABLE_LETTERS),
        ]
        for task in serial_phonological.SECONDARY_TASKS
    ]
    experiment.rng.shuffle(conditions)

    for similarity, task, letter_set in conditions:
        sequence = letter_set.copy()
        experiment.rng.shuffle(sequence)
        with experiment.trial(
            {
                "section": "serial_phonological",
                "condition": similarity,
                "subcondition": task,
                "sequence_length": len(sequence),
                "stimulus": "".join(sequence),
                "presentation_duration_s": common.SERIAL_ITEM_DURATION,
                "post_list_delay_s": 0,
                "notes": "pilot sound/suppression/tapping",
            }
        ):
            instruction = experiment.text(serial_phonological, task)
            ready = experiment.text(serial_phonological, "trial_ready")
            experiment.show_message(
                instruction + "\n\n" + ready,
                allow_skip=True,
            )
            experiment.show_fixation(0.5)
            tap_times = experiment.present_items(
                sequence,
                duration=common.SERIAL_ITEM_DURATION,
                isi=common.SERIAL_ISI,
                collect_taps=(task == "tapping"),
            )

            response, response_time = experiment.typed_response(
                experiment.text(serial_phonological, "response"),
                max_seconds=common.SERIAL_MAX_RESPONSE_S,
                mode="letters",
            )
            score = experiment.score_serial(sequence, response)

            experiment.save_trial(
                {
                    "section": "serial_phonological",
                    "condition": similarity,
                    "subcondition": task,
                    "sequence_length": len(sequence),
                    "stimulus": "".join(sequence),
                    "presentation_duration_s": common.SERIAL_ITEM_DURATION,
                    "post_list_delay_s": 0,
                    "response": score["response_clean"],
                    "response_time_s": round(response_time, 3),
                    "correct_count": score["correct_count"],
                    "total_items": len(sequence),
                    "accuracy": round(score["accuracy"], 4),
                    "whole_sequence_correct": score["whole_sequence_correct"],
                    "position_correct": json.dumps(score["position_correct"]),
                    "tap_count": len(tap_times),
                    "tap_times_s": json.dumps([round(value, 3) for value in tap_times]),
                    "notes": "pilot sound/suppression/tapping",
                }
            )
        experiment.maybe_break()


def make_chunked_groups(experiment, language):
    return experiment.rng.sample(
        serial_chunking.BASES[language],
        serial_chunking.GROUPS_PER_TRIAL,
    )


def make_nonchunked_groups(experiment, groups):
    real_chunks = set(serial_chunking.BASES[experiment.language])
    letters = list("".join(groups))
    group_size = len(groups[0])

    for _ in range(1000):
        experiment.rng.shuffle(letters)
        candidate = [
            "".join(letters[start : start + group_size])
            for start in range(0, len(letters), group_size)
        ]
        if all(group not in real_chunks for group in candidate):
            return candidate

    return candidate


def run_chunking(experiment):
    experiment.show_message(experiment.text(serial_chunking, "intro"))

    conditions = PILOT_CHUNKING_CONDITIONS.copy()
    experiment.rng.shuffle(conditions)

    for condition in conditions:
        groups = make_chunked_groups(experiment, experiment.language)
        display_groups = (
            groups
            if condition == "chunked"
            else make_nonchunked_groups(experiment, groups)
        )
        target_sequence = list("".join(display_groups))
        with experiment.trial(
            {
                "section": "serial_chunking",
                "condition": condition,
                "sequence_length": len(target_sequence),
                "stimulus": "|".join(display_groups),
                "presentation_duration_s": common.CHUNK_GROUP_DURATION,
                "post_list_delay_s": 0,
                "notes": "pilot six-group chunking",
            }
        ):
            experiment.show_message(
                experiment.text(serial_chunking, "trial_ready"),
                allow_skip=True,
            )
            experiment.show_fixation(0.5)
            experiment.present_items(
                display_groups,
                duration=common.CHUNK_GROUP_DURATION,
                isi=common.CHUNK_ISI,
            )

            response, response_time = experiment.typed_response(
                experiment.text(serial_chunking, "response"),
                max_seconds=common.SERIAL_MAX_RESPONSE_S,
                mode="letters",
            )
            score = experiment.score_serial(target_sequence, response)

            experiment.save_trial(
                {
                    "section": "serial_chunking",
                    "condition": condition,
                    "sequence_length": len(target_sequence),
                    "stimulus": "|".join(display_groups),
                    "presentation_duration_s": common.CHUNK_GROUP_DURATION,
                    "post_list_delay_s": 0,
                    "response": score["response_clean"],
                    "response_time_s": round(response_time, 3),
                    "correct_count": score["correct_count"],
                    "total_items": len(target_sequence),
                    "accuracy": round(score["accuracy"], 4),
                    "whole_sequence_correct": score["whole_sequence_correct"],
                    "position_correct": json.dumps(score["position_correct"]),
                    "notes": "pilot six-group chunking",
                }
            )
        experiment.maybe_break()


def run_selected_experiments(experiment, selections):
    if selections == ["all"]:
        task_order = ["free", "serial"]
        if sum(ord(char) for char in experiment.participant_id) % 2 == 1:
            task_order.reverse()

        for task in task_order:
            if task == "free":
                run_free_recall(experiment)
            else:
                run_capacity(experiment)
                run_phonological(experiment)
                run_chunking(experiment)
        return

    runners = {
        "free": run_free_recall,
        "capacity": run_capacity,
        "phonological": run_phonological,
        "chunking": run_chunking,
    }
    for selection in selections:
        runners[selection](experiment)


def main(argv=None):
    args = parse_args(argv)
    load_runtime()
    experiment = MemoryExperiment(
        data_dir=DATA_DIR,
        experiment_version=EXPERIMENT_VERSION,
        total_trials=(
            TOTAL_TRIALS
            if args.experiment == ["all"]
            else sum(EXPERIMENT_TRIAL_COUNTS[name] for name in args.experiment)
        ),
        break_every=None,
        filename_prefix="pilot",
        seed_scope="session",
        default_participant_id="pilot",
    )

    try:
        experiment.show_message(experiment.text(common, "initial"))

        run_selected_experiments(experiment, args.experiment)

        experiment.show_message(
            experiment.text(common, "complete", data_path=experiment.data_path)
        )
    finally:
        experiment.close()
        core.quit()


if __name__ == "__main__":
    main()
