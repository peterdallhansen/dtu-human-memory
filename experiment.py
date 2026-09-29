"""Full human-memory experiment runner.

Run this file for data collection. Use pilot.py for a short pipeline
and timing check before collecting final data.
"""

from pathlib import Path
import json
import re

from psychopy import core

from config import common, final_experiment
from config import free_recall, serial_capacity
from config import serial_chunking, serial_phonological
from runtime import MemoryExperiment


DATA_DIR = Path("data") / "final"


def section_text(experiment, config, key, **values):
    message = experiment.text(config, key, **values)
    if key == "intro":
        replacement = "FINAL EXPERIMENT" if experiment.language == "en" else "EKSPERIMENT"
        message = message.replace("PILOT", replacement)
    return message


def with_progress(experiment, message):
    return f"{message}\n\n{experiment.progress_text()}"


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


def run_free_recall(experiment):
    experiment.show_message(section_text(experiment, free_recall, "intro"))

    trial_configs = final_experiment.EXPERIMENTS["free_recall"]

    for trial, trial_config in enumerate(trial_configs, 1):
        words = experiment.rng.sample(
            free_recall.VOCABULARY[experiment.language],
            trial_config["list_length"],
        )
        list_id = f"random_{trial}"
        with experiment.trial(
            {
                "section": "free_recall",
                "condition": trial_config["condition"],
                "subcondition": trial_config["post_task"],
                "list_id": list_id,
                "sequence_length": len(words),
                "stimulus": "|".join(words),
                "presentation_duration_s": trial_config["word_duration"],
                "post_list_delay_s": (
                    common.POST_LIST_DELAY_S
                    if trial_config["post_task"] != "immediate"
                    else 0.0
                ),
                "notes": "final experiment",
            }
        ):
            ready = section_text(
                experiment,
                free_recall,
                "trial",
                trial=trial,
                total=len(trial_configs),
            )
            experiment.show_message(
                with_progress(experiment, ready),
                allow_skip=True,
            )
            experiment.show_fixation(0.75)

            experiment.present_items(
                words,
                duration=trial_config["word_duration"],
                isi=common.WORD_ISI,
            )

            distractor_start = ""
            distractor_response = ""
            distractor_correct = ""
            delay_s = 0.0

            if trial_config["post_task"] == "working_memory":
                distractor_start, distractor_response, distractor_correct = (
                    run_working_memory_distractor(
                        experiment,
                        common.POST_LIST_DELAY_S,
                    )
                )
                delay_s = common.POST_LIST_DELAY_S
            elif trial_config["post_task"] == "pause":
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
                    "condition": trial_config["condition"],
                    "subcondition": trial_config["post_task"],
                    "list_id": list_id,
                    "sequence_length": len(words),
                    "stimulus": "|".join(words),
                    "presentation_duration_s": trial_config["word_duration"],
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
                    "notes": "final experiment",
                }
            )


def run_capacity(experiment):
    experiment.show_message(section_text(experiment, serial_capacity, "intro"))

    settings = final_experiment.EXPERIMENTS["capacity"]
    lengths = settings["lengths"]

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
                "notes": "final experiment",
            }
        ):
            ready = section_text(
                experiment,
                serial_capacity,
                "trial",
                length=length,
            )
            experiment.show_message(
                with_progress(experiment, ready),
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
                    "notes": "final experiment",
                }
            )


def run_phonological(experiment):
    experiment.show_message(
        section_text(experiment, serial_phonological, "intro")
    )

    trial_configs = final_experiment.EXPERIMENTS["phonological"]
    letter_sets = {
        "confusable": serial_phonological.CONFUSABLE_LETTERS,
        "nonconfusable": serial_phonological.NONCONFUSABLE_LETTERS,
    }

    for trial_config in trial_configs:
        similarity = trial_config["condition"]
        task = trial_config["secondary_task"]
        letter_set = letter_sets[similarity]
        sequence = letter_set.copy()
        experiment.rng.shuffle(sequence)
        sequence = sequence[: trial_config["number_of_letters"]]
        with experiment.trial(
            {
                "section": "serial_phonological",
                "condition": similarity,
                "subcondition": task,
                "sequence_length": len(sequence),
                "stimulus": "".join(sequence),
                "presentation_duration_s": common.SERIAL_ITEM_DURATION,
                "post_list_delay_s": 0,
                "notes": "final experiment",
            }
        ):
            instruction = experiment.text(serial_phonological, task)
            ready = experiment.text(serial_phonological, "trial_ready")
            experiment.show_message(
                with_progress(experiment, instruction + "\n\n" + ready),
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
                    "notes": "final experiment",
                }
            )



def make_chunked_groups(
    experiment,
    language,
    group_count=serial_chunking.GROUPS_PER_TRIAL,
):
    return experiment.rng.sample(
        serial_chunking.BASES[language],
        group_count,
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
    experiment.show_message(section_text(experiment, serial_chunking, "intro"))

    settings = final_experiment.EXPERIMENTS["chunking"]
    conditions = settings["conditions"]

    for trial, condition in enumerate(conditions, 1):
        groups = make_chunked_groups(
            experiment,
            experiment.language,
            settings["groups_per_trial"],
        )
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
                "list_id": f"chunk_trial_{trial}",
                "sequence_length": len(target_sequence),
                "stimulus": "|".join(display_groups),
                "presentation_duration_s": common.CHUNK_GROUP_DURATION,
                "post_list_delay_s": 0,
                "notes": "final six-group chunking",
            }
        ):
            ready = experiment.text(serial_chunking, "trial_ready")
            experiment.show_message(
                with_progress(experiment, ready),
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
                    "list_id": f"chunk_trial_{trial}",
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
                    "notes": "final six-group chunking",
                }
            )


def main():
    experiment = MemoryExperiment(
        data_dir=DATA_DIR,
        experiment_version=final_experiment.EXPERIMENT_VERSION,
        total_trials=final_experiment.TOTAL_TRIALS,
        break_every=None,
    )

    try:
        experiment.show_message(experiment.final_text("initial"))

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

        experiment.show_message(
            experiment.final_text("complete", data_path=experiment.data_path)
        )
    finally:
        experiment.close()
        core.quit()


if __name__ == "__main__":
    main()
