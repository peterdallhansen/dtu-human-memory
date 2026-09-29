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


LISTS = {
    "en": {
        "L1": [
            "candle", "river", "jacket", "lemon", "garden",
            "piano", "window", "bottle", "rabbit", "hammer",
            "cloud", "basket", "mirror", "pepper", "ladder",
        ],
        "L2": [
            "ticket", "island", "pencil", "orange", "helmet",
            "camera", "blanket", "flower", "silver", "bridge",
            "cookie", "pocket", "thunder", "magnet", "castle",
        ],
        "L3": [
            "anchor", "banana", "circle", "dragon", "engine",
            "finger", "gravel", "hotel", "insect", "jungle",
            "kitten", "marble", "needle", "ocean", "paper",
        ],
        "L4": [
            "apple", "beach", "chair", "diamond", "eagle",
            "fence", "guitar", "horse", "igloo", "knife",
            "lantern", "monkey", "napkin", "olive", "pillow",
        ],
    },
    "da": {
        "L1": [
            "lys", "flod", "jakke", "citron", "have",
            "klaver", "vindue", "flaske", "kanin", "hammer",
            "sky", "kurv", "spejl", "peber", "stige",
        ],
        "L2": [
            "billet", "oase", "blyant", "appelsin", "hjelm",
            "kamera", "dyne", "blomst", "guld", "bro",
            "kage", "lomme", "torden", "magnet", "slot",
        ],
        "L3": [
            "anker", "banan", "cirkel", "drage", "motor",
            "finger", "grus", "hotel", "insekt", "jungle",
            "killing", "kugle", "snor", "hav", "papir",
        ],
        "L4": [
            "frugt", "strand", "stol", "diamant", "falk",
            "hegn", "guitar", "hest", "iglo", "kniv",
            "lanterne", "abe", "serviet", "oliven", "pude",
        ],
    },
}


FINAL_LISTS = {
    "en": {
        **LISTS["en"],
        "L5": [
            "acorn", "beacon", "cabin", "daisy", "envelope",
            "fountain", "glove", "harbor", "jelly", "kitchen",
            "laptop", "meadow", "puzzle", "suitcase", "willow",
        ],
        "L6": [
            "airport", "cactus", "drawer", "elbow", "flame",
            "grape", "hallway", "journal", "lighthouse", "orchard",
            "quilt", "sandal", "thermos", "umbrella", "wagon",
        ],
        "L7": [
            "attic", "branch", "chimney", "desert", "garlic",
            "honey", "inlet", "jigsaw", "knot", "mug",
            "oyster", "parade", "quarry", "ribbon", "shelter",
        ],
        "L8": [
            "apron", "barber", "compass", "dolphin", "elevator",
            "fabric", "glacier", "handle", "ladle", "museum",
            "oar", "pebble", "quiver", "syrup", "velvet",
        ],
        "L9": [
            "blossom", "canyon", "drum", "fossil", "harvest",
            "ink", "jewel", "market", "napkin", "raven",
            "shovel", "trumpet", "valley", "walnut", "zipper",
        ],
        "L10": [
            "beetle", "button", "coral", "cradle", "feather",
            "kettle", "locker", "melon", "pocket", "sailboat",
            "statue", "thimble", "toaster", "yarn", "cushion",
        ],
        "L11": [
            "bakery", "cherry", "closet", "comet", "curtain",
            "doorknob", "firefly", "hammock", "incense", "mailbox",
            "telescope", "towel", "village", "sunrise", "teapot",
        ],
        "L12": [
            "boulder", "doorstep", "fireplace", "flashlight", "popcorn",
            "raccoon", "sandwich", "seashell", "sidewalk", "snowman",
            "windmill", "coconut", "doormat", "raincoat", "shoelace",
        ],
        "L13": [
            "chalk", "clover", "crown", "domino", "eyelash",
            "flag", "frosting", "icicle", "jacket", "locket",
            "mushroom", "subway", "thunder", "toothbrush", "whistle",
        ],
        "L14": [
            "cannon", "cedar", "cupcake", "dictionary", "firewood",
            "grasshopper", "lighthouse", "mirror", "pumpkin", "sail",
            "teapot", "trophy", "underpass", "waterfall", "windshield",
        ],
        "L15": [
            "bicycle", "blanket", "chicken", "cotton", "hamburger",
            "mattress", "notebook", "pancake", "postcard", "volcano",
            "backpack", "baseball", "broccoli", "cabinet", "chocolate",
        ],
        "L16": [
            "avocado", "cabinet", "fireplace", "football", "lantern",
            "newspaper", "pancake", "postcard", "sandwich", "toothpaste",
            "volcano", "windmill", "cushion", "doorknob", "sweater",
        ],
    },
    "da": {
        **LISTS["da"],
        "L5": [
            "akvarium", "bager", "bamse", "batteri", "billede",
            "blad", "bluse", "bord", "brise", "busk",
            "flamme", "gade", "gummi", "hytte", "kort",
        ],
        "L6": [
            "avis", "bakke", "boks", "fabrik", "farve",
            "film", "glas", "havn", "hjul", "kasse",
            "klokke", "kyst", "lampe", "metal", "mur",
        ],
        "L7": [
            "album", "ananas", "arm", "asfalt", "bagage",
            "ballon", "barnevogn", "benzin", "blok", "bold",
            "brev", "briller", "bygning", "dam", "dyr",
        ],
        "L8": [
            "butik", "cykel", "elev", "fisk", "garn",
            "gave", "himmel", "honning", "kande", "kiste",
            "knogle", "kokken", "krukke", "loft", "pisk",
        ],
        "L9": [
            "kaede", "kamel", "klippe", "krone", "kvist",
            "lastbil", "lygte", "madras", "marked", "melon",
            "mont", "nabo", "palme", "panda", "perle",
        ],
        "L10": [
            "net", "nummer", "pakke", "pasta", "pind",
            "plade", "plante", "plaster", "pose", "ramme",
            "reol", "rose", "rude", "sandal", "skuffe",
        ],
        "L11": [
            "skib", "skilt", "skjorte", "skovl", "skrivebord",
            "slange", "smed", "sne", "sok", "sommer",
            "sovepose", "spand", "stempel", "sten", "stjerne",
        ],
        "L12": [
            "sukker", "suppe", "tablet", "tallerken", "tand",
            "taske", "tavle", "telefon", "termometer", "trappe",
            "trae", "tromme", "tunge", "ur", "vase",
        ],
        "L13": [
            "vask", "vand", "vifte", "vogn", "vulkan",
            "baer", "bevis", "bogstav", "by", "dag",
            "drik", "drom", "fane", "fjer", "flise",
        ],
        "L14": [
            "frakke", "gaffel", "gulv", "havre", "hjelm",
            "jord", "kage", "kanal", "kartoffel", "kirke",
            "kompas", "mark", "maling", "motor", "navn",
        ],
        "L15": [
            "bibel", "brand", "bro", "dreng", "familie",
            "hage", "harpiks", "indgang", "jordbar", "klap",
            "krus", "laks", "leg", "legetoj", "morgen",
        ],
        "L16": [
            "nat", "nisse", "papir", "perron", "plet",
            "radio", "reb", "ring", "saebe", "skrivebog",
            "tablet", "telt", "tog", "torn", "vinter",
        ],
    },
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
