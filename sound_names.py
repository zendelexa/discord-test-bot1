SOUND_NAMES = {}


def init(path):
    for line in open(path, 'r'):
        key, value = line.strip().split()
        SOUND_NAMES[key] = value
