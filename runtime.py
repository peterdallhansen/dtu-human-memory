"""Shared PsychoPy runtime for the pilot and final memory experiments."""

from contextlib import contextmanager
from datetime import datetime
import csv
from pathlib import Path
import random
import re

from psychopy import core, event, gui, visual
from psychopy.hardware import keyboard

from config import common


FIELDNAMES = [
    "participant_id",
    "language",
    "experiment_version",
    "session_id",
    "timestamp",
    "section",
    "repetition",
    "trial_index",
    "condition",
    "subcondition",
    "list_id",
    "sequence_length",
    "stimulus",
    "presentation_duration_s",
    "post_list_delay_s",
    "response",
    "response_time_s",
    "correct_count",
    "total_items",
    "accuracy",
    "whole_sequence_correct",
    "position_correct",
    "recall_source_positions",
    "distractor_start",
    "distractor_response",
    "distractor_correct_count",
    "tap_count",
    "tap_times_s",
    "skipped",
    "notes",
]


class SkipTrial(Exception):
    """Signal that the participant wants to leave the active trial."""


class MemoryExperiment:
    """Own PsychoPy state, keyboard handling, scoring, and trial storage."""

    def __init__(
        self,
        data_dir,
        experiment_version,
        total_trials,
        break_every,
        filename_prefix="final",
        seed_scope="session",
        default_participant_id="unknown",
    ):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.experiment_version = experiment_version
        self.total_trials = total_trials
        self.break_every = break_every
        self.filename_prefix = filename_prefix

        self._show_participant_dialog(default_participant_id)

        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        if seed_scope == "session":
            seed_suffix = self.session_id
        elif seed_scope == "day":
            seed_suffix = datetime.now().date().isoformat()
        else:
            raise ValueError("seed_scope must be 'session' or 'day'")

        self.rng = random.Random(
            f"{self.participant_id}_{self.language}_{seed_suffix}"
        )

        self.win = visual.Window(
            size=common.WINDOW_SIZE,
            fullscr=common.FULLSCREEN,
            color="black",
            units="height",
        )
        self.kb = keyboard.Keyboard()
        self.mouse = event.Mouse(win=self.win)
        self._skip_button_pressed = False

        self.main_text = visual.TextStim(
            self.win,
            text="",
            color="white",
            height=0.045,
            wrapWidth=1.35,
        )
        self.small_text = visual.TextStim(
            self.win,
            text="",
            color="white",
            height=0.032,
            wrapWidth=1.35,
        )
        self.stim_text = visual.TextStim(
            self.win,
            text="",
            color="white",
            height=0.12,
        )
        self.fixation = visual.TextStim(
            self.win,
            text="+",
            color="white",
            height=0.08,
        )
        self.skip_button = visual.Rect(
            self.win,
            width=0.24,
            height=0.065,
            pos=(0.56, -0.43),
            fillColor=(-0.25, -0.25, -0.25),
            lineColor="white",
            units="height",
        )
        self.skip_button_text = visual.TextStim(
            self.win,
            text=self.text(common, "skip_button"),
            color="white",
            height=0.024,
            pos=(0.56, -0.43),
        )

        safe_pid = re.sub(r"[^A-Za-z0-9_-]+", "_", self.participant_id)
        self.data_path = self.data_dir / (
            f"{self.filename_prefix}_{safe_pid}_{self.language}_{self.session_id}.csv"
        )
        with self.data_path.open("w", newline="", encoding="utf-8") as data_file:
            csv.DictWriter(data_file, fieldnames=FIELDNAMES).writeheader()

        self.trial_index = 0
        self.closed = False

    def _show_participant_dialog(self, default_participant_id):
        dialog = gui.Dlg(title="Human Memory Experiment / Eksperiment om hukommelse")
        dialog.addField("Participant ID / Deltager-ID:")
        dialog.addField("Language / Sprog:", choices=common.LANGUAGE_OPTIONS)
        dialog.show()

        if not dialog.OK:
            core.quit()

        self.participant_id = str(dialog.data[0]).strip() or default_participant_id
        language_label = str(dialog.data[1])
        self.language = common.LANGUAGE_CODES[language_label]
        self.language_label = language_label

    def text(self, config, key, **values):
        return config.TEXT[self.language][key].format(**values)

    def final_text(self, key, **values):
        return common.FINAL_TEXT[self.language][key].format(**values)

    def progress_text(self):
        return self.final_text(
            "progress",
            trial=self.trial_index,
            total=self.total_trials,
        )

    def show_message(self, message, continue_key="space", allow_skip=False):
        if allow_skip:
            message = f"{message}\n\n{self.text(common, 'skip_hint')}"

        self.main_text.text = message
        self.main_text.draw()
        if allow_skip:
            self.draw_skip_button()
        self.win.flip()
        self.clear_key_events()

        while True:
            keys = self.get_keys([continue_key, "escape", "esc"])
            self.check_escape(keys)
            if allow_skip:
                self.check_skip()
            if any(self.key_name(key) == continue_key for key in keys):
                return
            core.wait(0.01)

    def show_fixation(self, seconds=0.5):
        self.fixation.draw()
        self.win.flip()
        core.wait(seconds)

    def key_name(self, key):
        return key if isinstance(key, str) else key.name

    def clear_key_events(self):
        # PsychoPy 2026.2 can expose a broken timestamp shape through the
        # Keyboard wrapper when Psychtoolbox HID is unavailable on macOS.
        if self.kb.getBackend() == "event":
            event.clearEvents("keyboard")
        else:
            self.kb.clearEvents()

    def get_keys(self, key_list=None):
        if self.kb.getBackend() == "event":
            return event.getKeys(keyList=key_list)
        return self.kb.getKeys(
            keyList=key_list,
            waitRelease=False,
            clear=True,
        )

    def check_escape(self, keys):
        if any(self.key_name(key) in ("escape", "esc") for key in keys):
            self.close()
            core.quit()

    def draw_skip_button(self):
        self.skip_button.draw()
        self.skip_button_text.draw()

    def check_skip(self):
        pressed = self.mouse.isPressedIn(self.skip_button, buttons=[0])
        if pressed and not self._skip_button_pressed:
            self._skip_button_pressed = True
            raise SkipTrial
        self._skip_button_pressed = pressed

    def typed_response(self, prompt, max_seconds, mode, enter_ends=True):
        response = ""
        clock = core.Clock()
        self.clear_key_events()

        while clock.getTime() < max_seconds:
            remaining = max_seconds - clock.getTime()
            self.small_text.text = self.text(
                common,
                "typed_response",
                prompt=prompt,
                response=response,
                remaining=remaining,
            )
            self.small_text.draw()
            self.win.flip()

            keys = self.get_keys()
            self.check_escape(keys)

            for key in keys:
                name = self.key_name(key)

                if name in ("return", "enter") and enter_ends:
                    return response.strip(), clock.getTime()

                if name == "backspace":
                    response = response[:-1]
                    continue

                if name == "space":
                    if "spaces" in mode and response and not response.endswith(" "):
                        response += " "
                    continue

                if len(name) == 1:
                    if mode.startswith("letters") and name.isalpha():
                        response += name.lower()
                    elif mode.startswith("digits") and name.isdigit():
                        response += name
                    elif mode.startswith("alnum") and name.isalnum():
                        response += name.lower()

            core.wait(0.005)

        return response.strip(), max_seconds

    def present_items(self, items, duration, isi, collect_taps=False):
        tap_clock = core.Clock()
        tap_times = []
        self.clear_key_events()

        for item in items:
            item_clock = core.Clock()

            while item_clock.getTime() < duration:
                self.stim_text.text = str(item)
                self.stim_text.draw()
                self.win.flip()

                keys = self.get_keys(["space", "escape", "esc"])
                self.check_escape(keys)

                if collect_taps:
                    for key in keys:
                        if self.key_name(key) == "space":
                            tap_times.append(tap_clock.getTime())

            self.win.flip()
            if isi > 0:
                core.wait(isi)

        return tap_times

    @staticmethod
    def normalize_word_response(response):
        return re.findall(r"[^\W\d_]+", response.lower(), flags=re.UNICODE)

    @classmethod
    def score_free_recall(cls, target_words, response):
        recalled_words = cls.normalize_word_response(response)
        recalled_unique = set(recalled_words)
        position_correct = [
            int(target.lower() in recalled_unique) for target in target_words
        ]
        target_to_pos = {
            word.lower(): index + 1
            for index, word in enumerate(target_words)
        }

        source_positions = []
        already_used = set()
        for word in recalled_words:
            if word in target_to_pos and word not in already_used:
                source_positions.append(target_to_pos[word])
                already_used.add(word)

        return {
            "correct_count": sum(position_correct),
            "accuracy": sum(position_correct) / len(target_words),
            "position_correct": position_correct,
            "recall_source_positions": source_positions,
        }

    @staticmethod
    def score_serial(target, response):
        clean = re.sub(r"[\W_]", "", response, flags=re.UNICODE).upper()
        target = "".join(target).upper()
        position_correct = [
            int(index < len(clean) and clean[index] == target_char)
            for index, target_char in enumerate(target)
        ]

        return {
            "response_clean": clean,
            "correct_count": sum(position_correct),
            "accuracy": sum(position_correct) / len(target),
            "whole_sequence_correct": int(clean == target),
            "position_correct": position_correct,
        }

    def save_trial(self, row):
        complete = {name: "" for name in FIELDNAMES}
        complete.update(row)
        complete.update(
            {
                "participant_id": self.participant_id,
                "language": self.language,
                "experiment_version": self.experiment_version,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "trial_index": self.trial_index,
                "skipped": row.get("skipped", 0),
            }
        )

        with self.data_path.open("a", newline="", encoding="utf-8") as data_file:
            writer = csv.DictWriter(data_file, fieldnames=FIELDNAMES)
            writer.writerow(complete)
            data_file.flush()

    def save_skipped_trial(self, row):
        skipped_row = dict(row)
        for field in (
            "response",
            "response_time_s",
            "correct_count",
            "accuracy",
            "whole_sequence_correct",
            "position_correct",
            "recall_source_positions",
            "distractor_start",
            "distractor_response",
            "distractor_correct_count",
            "tap_count",
            "tap_times_s",
        ):
            skipped_row[field] = ""

        notes = str(skipped_row.get("notes", "")).strip()
        skipped_row["notes"] = f"{notes}; skipped" if notes else "skipped"
        skipped_row["skipped"] = 1
        self.save_trial(skipped_row)

    @contextmanager
    def trial(self, row=None):
        self._skip_button_pressed = self.mouse.isPressedIn(
            self.skip_button,
            buttons=[0],
        )
        self.next_trial()
        try:
            yield
        except SkipTrial:
            self.save_skipped_trial(row or {})

    def next_trial(self):
        self.trial_index += 1

    def maybe_break(self):
        if (
            self.break_every
            and self.trial_index < self.total_trials
            and self.trial_index % self.break_every == 0
        ):
            self.show_message(
                self.final_text(
                    "break",
                    completed=self.trial_index,
                    total=self.total_trials,
                )
            )

    def close(self):
        if not self.closed:
            self.closed = True
            self.win.close()
