"""Design settings for the full memory experiment."""

FREE_RECALL_REPETITIONS = 4
CAPACITY_REPETITIONS = 4
PHONOLOGICAL_REPETITIONS = 4
CHUNKING_REPETITIONS = 4

BREAK_EVERY_TRIALS = 12

# Each repetition contains four free-recall, three capacity,
# six phonological, and four chunking trials.
TRIALS_PER_REPETITION = {
    "free_recall": 4,
    "capacity": 3,
    "phonological": 6,
    "chunking": 4,
}

TOTAL_TRIALS = (
    FREE_RECALL_REPETITIONS * TRIALS_PER_REPETITION["free_recall"]
    + CAPACITY_REPETITIONS * TRIALS_PER_REPETITION["capacity"]
    + PHONOLOGICAL_REPETITIONS * TRIALS_PER_REPETITION["phonological"]
    + CHUNKING_REPETITIONS * TRIALS_PER_REPETITION["chunking"]
)

EXPERIMENT_VERSION = "final_v1"
