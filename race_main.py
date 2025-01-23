import physics
import random
import os
import sound_names


def start(names):
    os.system("del /Q images")

    #names = input().split()

    physics.clear()

    physics.create_track()
    for (index, name) in enumerate(names):
        physics.create_player(name, index)

    physics.start_race()

    random_song = random.choice(sound_names.SONGS)
    
    #os.system(f"ffmpeg -y -framerate 15 -i images/img_%d.png -i {random_song} -c:a copy -shortest -c:v libx264 -r 30 output.mp4")
    os.system(f"ffmpeg -y -i outputtest.mp4 -i {random_song} -c:a copy -shortest -c:v libx264 -r 30 output.mp4")
    os.system("del /Q player_icons")
