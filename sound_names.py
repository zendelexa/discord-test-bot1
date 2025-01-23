SOUND_NAMES = {}


def load_sounds(path):
    with open(path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            SOUND_NAMES[key] = value
