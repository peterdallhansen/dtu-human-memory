"""Chunking configuration and participant-facing text."""

GROUPS_PER_TRIAL = 6
LETTERS_PER_GROUP = 3

BASES = {
    "en": [
        "CAT", "DOG", "SUN", "RED", "BOX", "KEY", "BUS", "MAP",
        "FOX", "JAR", "PEN", "CAR", "SKY", "CUP", "HAT", "LOG",
        "TEA", "FAN", "RAT", "NET", "MUG", "PIG", "BEE", "ANT",
        "JAM", "MAN", "COW", "HEN", "LID", "ICE", "MUD", "RUG",
        "BAT", "CAN", "FIG", "CAP", "INK", "TOP", "RIB", "TOY",
    ],
    "da": [
        "KAT", "HUS", "SOL", "GUL", "BUS", "LYS", "PEN", "BIL",
        "SKY", "BOG", "HAT", "SUR", "KOP", "FAR", "DAG", "MOR",
        "HUN", "GOD", "NYE", "MIN", "DIN", "VOR", "KAN", "VIL",
        "HAR", "MAD", "FOD", "ARM", "BEN", "LIV", "LAG", "SOM",
        "DER", "MEN", "HER", "ALT", "SER",
    ],
}


TEXT = {
    "en": {
        "intro": (
            "SERIAL RECALL: CHUNKING\n\n"
            "You will see six groups of three letters.\n"
            "Remember all eighteen letters in the SAME ORDER.\n\n"
            "Press SPACE to continue."
        ),
        "trial_ready": "Remember the letters in exact order.\n\nPress SPACE when ready.",
        "response": "Type all eighteen letters in the SAME ORDER.",
    },
    "da": {
        "intro": (
            "SERIEL GENKALDELSE: GRUPPERING\n\n"
            "Du vil se seks grupper med tre bogstaver.\n"
            "Husk alle atten bogstaver i SAMME RÆKKEFØLGE.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at fortsætte."
        ),
        "trial_ready": (
            "Husk bogstaverne i præcis rækkefølge.\n\n"
            "Tryk på MELLEMRUMSTASTEN, når du er klar."
        ),
        "response": "Indtast alle atten bogstaver i SAMME RÆKKEFØLGE.",
    },
}
