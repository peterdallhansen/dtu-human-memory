"""Chunking configuration and participant-facing text."""

BASES = {
    "en": [
        ["CAT", "DOG", "SUN"],
        ["RED", "BUS", "MAP"],
        ["PEN", "CAR", "SKY"],
        ["BOX", "TEA", "FAN"],
    ],
    "da": [
        ["KAT", "HUS", "SOL"],
        ["GUL", "BUS", "LYS"],
        ["PEN", "BIL", "SKY"],
        ["BOG", "HAT", "SUR"],
    ],
}


FINAL_BASES = {
    "en": BASES["en"] + [
        ["RAT", "PIG", "CAR"],
        ["MAN", "HAT", "RED"],
        ["JAR", "KEY", "BOX"],
        ["CUP", "MAP", "SUN"],
        ["FOX", "LOG", "NET"],
        ["BEE", "ANT", "JAM"],
        ["ICE", "MUD", "RUG"],
        ["PEN", "INK", "TOP"],
        ["BAT", "CAN", "FIG"],
        ["COW", "HEN", "FAN"],
        ["BUS", "CAP", "LID"],
        ["DOG", "RIB", "TOY"],
    ],
    "da": BASES["da"] + [
        ["FAR", "MOR", "HUN"],
        ["GOD", "DAG", "NYE"],
        ["MIN", "DIN", "VOR"],
        ["KAN", "VIL", "HAR"],
        ["MAD", "KOP", "HAT"],
        ["FOD", "ARM", "BEN"],
        ["LYS", "LIV", "LAG"],
        ["HUS", "BIL", "BUS"],
        ["FAR", "SOM", "DER"],
        ["MOR", "MEN", "HER"],
        ["ALT", "GOD", "DAG"],
        ["KAN", "SER", "HER"],
    ],
}


TEXT = {
    "en": {
        "intro": (
            "SERIAL RECALL: CHUNKING\n\n"
            "You will see three groups of three letters.\n"
            "Remember all nine letters in the SAME ORDER.\n\n"
            "Press SPACE to continue."
        ),
        "trial_ready": "Remember the letters in exact order.\n\nPress SPACE when ready.",
        "response": "Type all nine letters in the SAME ORDER.",
    },
    "da": {
        "intro": (
            "SERIEL GENKALDELSE: GRUPPERING\n\n"
            "Du vil se tre grupper med tre bogstaver.\n"
            "Husk alle ni bogstaver i SAMME RÆKKEFØLGE.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at fortsætte."
        ),
        "trial_ready": (
            "Husk bogstaverne i præcis rækkefølge.\n\n"
            "Tryk på MELLEMRUMSTASTEN, når du er klar."
        ),
        "response": "Indtast alle ni bogstaver i SAMME RÆKKEFØLGE.",
    },
}
