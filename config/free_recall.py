"""Free-recall conditions, stimuli, and participant-facing text."""

from . import common


LIST_LENGTH = 15


CONDITIONS = [
    {
        "condition": "slow_immediate",
        "word_duration": common.SLOW_WORD_DURATION,
        "post_task": "immediate",
    },
    {
        "condition": "fast_immediate",
        "word_duration": common.FAST_WORD_DURATION,
        "post_task": "immediate",
    },
    {
        "condition": "slow_wm",
        "word_duration": common.SLOW_WORD_DURATION,
        "post_task": "working_memory",
    },
    {
        "condition": "slow_pause",
        "word_duration": common.SLOW_WORD_DURATION,
        "post_task": "pause",
    },
]


VOCABULARY = {
    "en": [
        "candle", "river", "jacket", "lemon", "garden",
        "piano", "window", "bottle", "rabbit", "hammer",
        "cloud", "basket", "mirror", "pepper", "ladder",
        "ticket", "island", "pencil", "orange", "helmet",
        "camera", "blanket", "flower", "silver", "bridge",
        "cookie", "pocket", "thunder", "magnet", "castle",
        "anchor", "banana", "circle", "dragon", "engine",
        "finger", "gravel", "hotel", "insect", "jungle",
        "kitten", "marble", "needle", "ocean", "paper",
        "apple", "beach", "chair", "diamond", "eagle",
        "fence", "guitar", "horse", "igloo", "knife",
        "lantern", "monkey", "napkin", "olive", "pillow",
        "acorn", "beacon", "cabin", "daisy", "envelope",
        "fountain", "glove", "harbor", "jelly", "kitchen",
        "laptop", "meadow", "puzzle", "suitcase", "willow",
        "airport", "cactus", "drawer", "elbow", "flame",
        "grape", "hallway", "journal", "lighthouse", "orchard",
        "quilt", "sandal", "thermos", "umbrella", "wagon",
        "attic", "branch", "chimney", "desert", "garlic",
        "honey", "inlet", "jigsaw", "knot", "mug",
        "oyster", "parade", "quarry", "ribbon", "shelter",
        "apron", "barber", "compass", "dolphin", "elevator",
        "fabric", "glacier", "handle", "ladle", "museum",
        "oar", "pebble", "quiver", "syrup", "velvet",
        "blossom", "canyon", "drum", "fossil", "harvest",
        "ink", "jewel", "market", "raven", "shovel",
        "trumpet", "valley", "walnut", "zipper", "beetle",
        "button", "coral", "cradle", "feather", "kettle",
        "locker", "melon", "sailboat", "statue", "thimble",
        "toaster", "yarn", "cushion", "bakery", "cherry",
        "closet", "comet", "curtain", "doorknob", "firefly",
        "hammock", "incense", "mailbox", "telescope", "towel",
        "village", "sunrise", "teapot", "boulder", "doorstep",
        "fireplace", "flashlight", "popcorn", "raccoon", "sandwich",
        "seashell", "sidewalk", "snowman", "windmill", "coconut",
        "doormat", "raincoat", "shoelace", "chalk", "clover",
        "crown", "domino", "eyelash", "flag", "frosting",
        "icicle", "locket", "mushroom", "subway", "toothbrush",
        "whistle", "cannon", "cedar", "cupcake", "dictionary",
        "firewood", "grasshopper", "pumpkin", "sail", "trophy",
        "underpass", "waterfall", "windshield", "bicycle", "chicken",
        "cotton", "hamburger", "mattress", "notebook", "pancake",
        "postcard", "volcano", "backpack", "baseball", "broccoli",
        "cabinet", "chocolate", "avocado", "football", "newspaper",
        "toothpaste", "sweater",
    ],
    "da": [
        "lys", "flod", "jakke", "citron", "have",
        "klaver", "vindue", "flaske", "kanin", "hammer",
        "sky", "kurv", "spejl", "peber", "stige",
        "billet", "oase", "blyant", "appelsin", "hjelm",
        "kamera", "dyne", "blomst", "guld", "bro",
        "kage", "lomme", "torden", "magnet", "slot",
        "anker", "banan", "cirkel", "drage", "motor",
        "finger", "grus", "hotel", "insekt", "jungle",
        "killing", "kugle", "snor", "hav", "papir",
        "frugt", "strand", "stol", "diamant", "falk",
        "hegn", "guitar", "hest", "iglo", "kniv",
        "lanterne", "abe", "serviet", "oliven", "pude",
        "akvarium", "bager", "bamse", "batteri", "billede",
        "blad", "bluse", "bord", "brise", "busk",
        "flamme", "gade", "gummi", "hytte", "kort",
        "avis", "bakke", "boks", "fabrik", "farve",
        "film", "glas", "havn", "hjul", "kasse",
        "klokke", "kyst", "lampe", "metal", "mur",
        "album", "ananas", "arm", "asfalt", "bagage",
        "ballon", "barnevogn", "benzin", "blok", "bold",
        "brev", "briller", "bygning", "dam", "dyr",
        "butik", "cykel", "elev", "fisk", "garn",
        "gave", "himmel", "honning", "kande", "kiste",
        "knogle", "kokken", "krukke", "loft", "pisk",
        "kaede", "kamel", "klippe", "krone", "kvist",
        "lastbil", "lygte", "madras", "marked", "melon",
        "mont", "nabo", "palme", "panda", "perle",
        "net", "nummer", "pakke", "pasta", "pind",
        "plade", "plante", "plaster", "pose", "ramme",
        "reol", "rose", "rude", "sandal", "skuffe",
        "skib", "skilt", "skjorte", "skovl", "skrivebord",
        "slange", "smed", "sne", "sok", "sommer",
        "sovepose", "spand", "stempel", "sten", "stjerne",
        "sukker", "suppe", "tablet", "tallerken", "tand",
        "taske", "tavle", "telefon", "termometer", "trappe",
        "trae", "tromme", "tunge", "ur", "vase",
        "vask", "vand", "vifte", "vogn", "vulkan",
        "baer", "bevis", "bogstav", "by", "dag",
        "drik", "drom", "fane", "fjer", "flise",
        "frakke", "gaffel", "gulv", "havre", "jord",
        "kanal", "kartoffel", "kirke", "kompas", "mark",
        "maling", "navn", "bibel", "brand", "dreng",
        "familie", "hage", "harpiks", "indgang", "jordbar",
        "klap", "krus", "laks", "leg", "legetoj",
        "morgen", "nat", "nisse", "perron", "plet",
        "radio", "reb", "ring", "saebe", "skrivebog",
        "telt", "tog", "torn", "vinter",
    ],
}


TEXT = {
    "en": {
        "intro": (
            "FREE RECALL PILOT\n\n"
            "You will see a list of words, one at a time.\n"
            "After the list, recall as many words as you can in ANY order.\n\n"
            "Type recalled words separated by spaces.\n\n"
            "Press SPACE to begin."
        ),
        "trial": (
            "Free recall trial {trial} of {total}.\n\n"
            "Keep your eyes on the centre of the screen.\n\n"
            "Press SPACE when ready."
        ),
        "response": (
            "Recall as many words as possible, in any order.\n"
            "Separate words with spaces."
        ),
        "working_memory": (
            "Count backwards by 3 from {start}.\n\n"
            "Type each answer separated by a SPACE.\n"
            "Keep going until the timer ends.\n\n"
            "{response}_\n\n"
            "{remaining:0.0f} s"
        ),
        "pause": "Please wait.",
    },
    "da": {
        "intro": (
            "FRI GENKALDELSE - PILOT\n\n"
            "Du vil se en liste med ord, ét ad gangen.\n"
            "Efter listen skal du genkalde så mange ord som muligt i\n"
            "VILKÅRLIG RÆKKEFØLGE.\n\n"
            "Skriv de ord, du kan huske, adskilt af mellemrum.\n\n"
            "Tryk på MELLEMRUMSTASTEN for at begynde."
        ),
        "trial": (
            "Forsøg med fri genkaldelse {trial} af {total}.\n\n"
            "Hold blikket rettet mod midten af skærmen.\n\n"
            "Tryk på MELLEMRUMSTASTEN, når du er klar."
        ),
        "response": (
            "Genkald så mange ord som muligt i vilkårlig rækkefølge.\n"
            "Adskil ordene med mellemrum."
        ),
        "working_memory": (
            "Tæl baglæns med 3 fra {start}.\n\n"
            "Skriv hvert svar adskilt af et MELLEMRUM.\n"
            "Fortsæt, indtil tiden er gået.\n\n"
            "{response}_\n\n"
            "{remaining:0.0f} sek."
        ),
        "pause": "Vent venligst.",
    },
}
