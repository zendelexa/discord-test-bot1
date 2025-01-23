import random
import screen_drawer
import imageio_ffmpeg

#import pygame as pg
from random import randrange
import pymunk.pygame_util
pymunk.pygame_util.positive_y_is_up = False

#параметры PyGame
RES = WIDTH, HEIGHT = 900, 720
FPS = 100

#pg.init()
#surface = pg.display.set_mode(RES)
#clock = pg.time.Clock()
#draw_options = pymunk.pygame_util.DrawOptions(surface)

#настройки Pymunk
space = pymunk.Space()
space.gravity = 0, 8000

#платформа


def create_segment(space, pos1, pos2):
    segment_body = pymunk.Body(1, 2, pymunk.Body.KINEMATIC)
    new_pos1 = ((pos1[0] - pos2[0]) / 2, (pos1[1] - pos2[1]) / 2)
    new_pos2 = ((pos2[0] - pos1[0]) / 2, (pos2[1] - pos1[1]) / 2)
    segment_shape = pymunk.Segment(segment_body, new_pos1, new_pos2, 20)
    segment_body.position = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)
    space.add(segment_body, segment_shape)
    segment_shape.elasticity = 0.8
    segment_shape.friction = 1.0
    segments.append(segment_shape)
    return segment_shape

def create_fan(space, pos, size):
    segments = [create_segment(space, (pos[0] - size[0], pos[1] - size[1]), (pos[0] + size[0], pos[1] + size[1])),
                create_segment(space, (pos[0] - size[1], pos[1] - size[0]), (pos[0] + size[1], pos[1] + size[0]))]
    angular_velocity = random.randint(3, 20) * (random.randint(0, 1) * 2 - 1)
    for segment in segments:
        segment.body.angular_velocity = angular_velocity
    return segments


#кружки
body = pymunk.Body()
def create_circle(space, pos, circle_size=30, body_type=pymunk.Body.DYNAMIC):
    circle_mass = 1
    circle_moment = pymunk.moment_for_circle(circle_mass, circle_size, circle_size)
    circle_body = pymunk.Body(circle_mass, circle_moment, body_type=body_type)
    circle_body.position = pos
    circle_shape = pymunk.Circle(circle_body, circle_size)
    circle_shape.elasticity = 0.8
    circle_shape.friction = 1.0
    circle_shape.color = [randrange(256) for i in range(4)] if body_type == pymunk.Body.DYNAMIC else 4*[255]
    space.add(circle_body, circle_shape)
    if body_type == pymunk.Body.DYNAMIC:
        # players.append(circle_shape)
        pass
    else:
        circles.append(circle_shape)
    return circle_shape


players: list[screen_drawer.Player] = []
circles = []
segments = []
# seg = create_segment(space, (30, 60), (400, 400))
# fan = create_fan(space, (400, 400), (200, 20))
def clear():
    global space
    space = pymunk.Space()
    space.gravity = 0, 8000
    global players, circles, segments
    players = []
    circles = []
    segments = []

def create_track():
    for i in range(10):
        create_fan(space, (400, i * 900 + 400), (200, 20))
    create_segment(space, (100, -40), (700, -40))
    create_segment(space, (100, 0), (100, 10000))
    create_segment(space, (700, 0), (700, 10000))

    for i in range(40):
        offset_x = random.randint(0, 200)
        # create_circle(space, (100, i * 200 + 300), 30, pymunk.Body.STATIC)
        # create_circle(space, (700, i * 200 + 300), 30, pymunk.Body.STATIC)
        create_segment(space, (100, i * 200 + 300), (100 + random.randint(30, 100), i * 200 + 310))
        create_segment(space, (700, i * 200 + 300), (700 - random.randint(30, 100), i * 200 + 310))

        for j in range(5):
            curr_x = offset_x + 200 * j
            if curr_x <= 250 or curr_x >= 700-150:
                continue
            create_circle(space, (curr_x, i * 200 + 400), 30, pymunk.Body.STATIC)

def create_player(name, index):
    players.append(screen_drawer.Player(name, create_circle(space, (random.randint(150, 650), random.randint(0, 50))), f"player_icons/icon{index}.png"))



#Отрисовка
def start_race():
    screen_drawer.writer = imageio_ffmpeg.write_frames("outputtest.mp4", screen_drawer.FRAME_SIZE, fps=15)
    screen_drawer.writer.send(None)
    fr = 0
    keep_going = True
    while keep_going and fr < 100_000:
        #surface.fill(pg.Color('black'))

        #for i in pg.event.get():
        #    if i.type == pg.QUIT:
        #        exit()
            # спавн кубиков
            # if i.type == pg.MOUSEBUTTONDOWN:
            #     if i.button == 1:
            #         players.append(screen_drawer.Player(f"player {len(players)}", create_circle(space, i.pos)))
            #         # print(i.pos)
        for player in players:
            keep_going = False
            if player.circle.body.position.y <= 11000:
                keep_going = True
                break


        # seg.body.angular_velocity = -1

        space.step(1 / FPS / 2)

        if fr % 5 == 0:
            screen_drawer.draw(circles, segments, players, fr // 5)
        fr += 1
        #space.debug_draw(draw_options)

        #pg.display.flip()
        #clock.tick(FPS)
    screen_drawer.writer.close()