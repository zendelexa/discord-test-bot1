SOUND_NAMES = {}

SOUNDS_NAMES_DIR_PATH = "."
SOUNDS_NAMES_FILE = "sounds.txt"

SONGS = [
    SOUNDS_NAMES_DIR_PATH + "/" + "pedro.mp3",
    SOUNDS_NAMES_DIR_PATH + "/" + "mrbeast.mp4",
    SOUNDS_NAMES_DIR_PATH + "/" + "crazyfrog.mp3"
]


def load_sounds(path):
    with open(path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            SOUND_NAMES[key] = value
