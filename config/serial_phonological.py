"""Phonological-similarity and secondary-task configuration."""

CONFUSABLE_LETTERS = list("BCD GPT".replace(" ", ""))
NONCONFUSABLE_LETTERS = list("FJKQRY")
SECONDARY_TASKS = ["normal", "suppression", "tapping"]


TEXT = {
    "en": {
        "intro": (
            "SERIAL RECALL: SOUND AND SECONDARY TASKS\n\n"
            "You will see six letters, one at a time.\n"
            "Type the letters afterwards in the SAME ORDER.\n\n"
            "Some trials include an additional task.\n\n"
            "Press SPACE to continue."
        ),
        "normal": "No secondary task.\nJust remember the letters in order.",
        "suppression": (
            "ARTICULATORY SUPPRESSION\n\n"
            "While the letters are appearing, repeatedly say\n"
            '"THE, THE, THE..." out loud at about 2 times per second.\n\n'
            "Keep speaking until the final letter disappears."
        ),
        "tapping": (
            "FINGER TAPPING\n\n"
            "While the letters are appearing, repeatedly tap the SPACEBAR\n"
            "with your non-dominant index finger at about 2 times per second.\n\n"
            "Keep tapping until the final letter disappears."
        ),
        "trial_ready": "Press SPACE when ready.",
        "response": "Type the six letters in the SAME ORDER.",
    },
    "da": {
        "intro": (
            "SERIEL GENKALDELSE: LYD OG SEKUNDÆRE OPGAVER\n\n"
            "Du vil se seks bogstaver, ét ad gangen.\n"
            "Bagefter skal du skrive bogstaverne i SAMME RÆKKEFØLGE.\n\n"
            "Nogle forsøg indeholder en ekstra opgave.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at fortsætte."
        ),
        "normal": "Ingen sekundær opgave.\nHusk blot bogstaverne i rækkefølge.",
        "suppression": (
            "ARTIKULATORISK UNDERTRYKKELSE\n\n"
            "Mens bogstaverne vises, skal du gentage\n"
            '"DET, DET, DET..." højt cirka to gange i sekundet.\n\n'
            "Bliv ved med at tale, indtil det sidste bogstav forsvinder."
        ),
        "tapping": (
            "FINGERTAPNING\n\n"
            "Mens bogstaverne vises, skal du gentagne gange trykke på\n"
            "MELLEMRUMSTASTEN med den ikke-dominante pegefinger cirka to\n"
            "gange i sekundet.\n\n"
            "Bliv ved med at tappe, indtil det sidste bogstav forsvinder."
        ),
        "trial_ready": "Tryk på MELLEMRUMSTASTEN, når du er klar.",
        "response": "Indtast de seks bogstaver i SAMME RÆKKEFØLGE.",
    },
}
