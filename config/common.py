"""Shared timing, window, and language configuration."""

PILOT_MODE = True

WINDOW_SIZE = (1100, 720)
FULLSCREEN = True

SLOW_WORD_DURATION = 2.0
FAST_WORD_DURATION = 0.75
WORD_ISI = 0.10
FREE_RECALL_MAX_RESPONSE_S = 45.0
POST_LIST_DELAY_S = 20.0

SERIAL_ITEM_DURATION = 0.80
SERIAL_ISI = 0.20
SERIAL_MAX_RESPONSE_S = 20.0

CHUNK_GROUP_DURATION = 1.20
CHUNK_ISI = 0.20

LANGUAGE_OPTIONS = ["Dansk", "English"]
LANGUAGE_CODES = {
    "Dansk": "da",
    "English": "en",
}

TEXT = {
    "en": {
        "typed_response": (
            "{prompt}\n\n"
            "{response}_\n\n"
            "Press ENTER when finished.  Time remaining: {remaining:0.0f} s"
        ),
        "skip_hint": "Click SKIP TRIAL before starting to skip this trial.",
        "skip_button": "SKIP TRIAL",
        "initial": (
            "HUMAN MEMORY MINI PROJECT - PILOT\n\n"
            "This is a shortened pilot version used to check timing,\n"
            "difficulty, instructions, and data saving.\n\n"
            "The full experiment should use more repetitions.\n\n"
            "Press SPACE to begin.\n\n"
            "Click SKIP TRIAL on the trial instruction screen to skip it."
        ),
        "complete": (
            "Pilot complete.\n\n"
            "Data were saved to:\n{data_path}\n\n"
            "Please note anything that felt too easy, too hard,\n"
            "too fast, confusing, or tiring.\n\n"
            "Press SPACE to finish."
        ),
    },
    "da": {
        "typed_response": (
            "{prompt}\n\n"
            "{response}_\n\n"
            "Tryk på ENTER, når du er færdig.  Tid tilbage: {remaining:0.0f} sek."
        ),
        "skip_hint": "Klik på SPRING OVER før start for at springe dette forsøg over.",
        "skip_button": "SPRING OVER",
        "initial": (
            "MINIPROJEKT OM MENNESKELIG HUKOMMELSE - PILOT\n\n"
            "Dette er en forkortet pilotversion, der bruges til at kontrollere\n"
            "timing, sværhedsgrad, instruktioner og datalagring.\n\n"
            "Det fulde eksperiment bør bruge flere gentagelser.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at begynde.\n\n"
            "Klik på SPRING OVER på forsøgsinstruktionsskærmen for at springe det over."
        ),
        "complete": (
            "Pilot gennemført.\n\n"
            "Data blev gemt i:\n{data_path}\n\n"
            "Notér venligst, om noget føltes for let, for svært,\n"
            "for hurtigt, forvirrende eller udmattende.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at afslutte."
        ),
    },
}


FINAL_TEXT = {
    "en": {
        "initial": (
            "HUMAN MEMORY EXPERIMENT\n\n"
            "You will complete several short memory tasks.\n"
            "Please read each instruction carefully and work as accurately as possible.\n\n"
            "You may take short breaks during the experiment.\n\n"
            "Press SPACE to begin.\n\n"
            "Click SKIP TRIAL on the trial instruction screen to skip it."
        ),
        "break": (
            "SHORT BREAK\n\n"
            "You have completed {completed} of {total} trials.\n\n"
            "Relax your eyes and continue when you feel ready.\n\n"
            "Press SPACE to continue."
        ),
        "complete": (
            "Experiment complete.\n\n"
            "Your data were saved to:\n{data_path}\n\n"
            "Thank you for participating.\n\n"
            "Press SPACE to finish."
        ),
        "progress": "Trial {trial} of {total}",
    },
    "da": {
        "initial": (
            "EKSPERIMENT OM MENNESKELIG HUKOMMELSE\n\n"
            "Du skal gennemføre flere korte hukommelsesopgaver.\n"
            "Læs hver instruktion grundigt, og arbejd så præcist som muligt.\n\n"
            "Du kan holde korte pauser undervejs.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at begynde.\n\n"
            "Klik på SPRING OVER på forsøgsinstruktionsskærmen for at springe det over."
        ),
        "break": (
            "KORT PAUSE\n\n"
            "Du har gennemført {completed} af {total} forsøg.\n\n"
            "Slap af i øjnene, og fortsæt, når du er klar.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at fortsætte."
        ),
        "complete": (
            "Eksperiment gennemført.\n\n"
            "Dine data blev gemt i:\n{data_path}\n\n"
            "Tak for din deltagelse.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at afslutte."
        ),
        "progress": "Forsøg {trial} af {total}",
    },
}
