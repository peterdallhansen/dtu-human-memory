"""Serial-recall capacity configuration and participant-facing text."""

LENGTHS = [4, 6, 8]


TEXT = {
    "en": {
        "intro": (
            "SERIAL RECALL: CAPACITY\n\n"
            "You will see digits one at a time.\n"
            "Afterwards, type them in the SAME ORDER.\n\n"
            "Press SPACE to continue."
        ),
        "trial": (
            "Capacity trial: {length} digits.\n\n"
            "Press SPACE when ready."
        ),
        "response": "Type the digits in the SAME ORDER.",
    },
    "da": {
        "intro": (
            "SERIEL GENKALDELSE: KAPACITET\n\n"
            "Du vil se cifre ét ad gangen.\n"
            "Bagefter skal du skrive dem i SAMME RÆKKEFØLGE.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at fortsætte."
        ),
        "trial": (
            "Kapacitetsforsøg: {length} cifre.\n\n"
            "Tryk på MELLEMRUMSTASTEN, når du er klar."
        ),
        "response": "Indtast cifrene i SAMME RÆKKEFØLGE.",
    },
}
