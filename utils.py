#-*- coding: utf-8 -*-

from OpenGL.GL import *
from pygame import mixer

WHITE     = (255, 255, 255)
YELLOW    = (255, 255,   0)
BLACK     = (  0,   0,   0)
GRAY      = ( 60,  60,  60)
DARKGRAY  = ( 30,  30,  30)
RED       = (255,   0,   0)
DARKRED   = (120,   0,   0)
GREEN     = ( 71, 107,   8)
ORANGE    = (255,  36,   0)
BLUE      = (  0,   0, 244)


def clear():
    glClearColor(0.0, 0.0, 0.0, 0.1)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

class Convert(object):        
        
    #This is the class that handles perspective transformation.

    #From map to screen
    def __call__(self, x, y):
        tx = ((-x+y)/1.4)
        ty = ((-x-y)/1.4*0.342)
        return (int(tx), int(ty))

    def to_screen_float(self, x, y):
        tx = ((-x+y)/1.4)
        ty = ((-x-y)/1.4*0.342)
        return tx, ty

    def to_screen_int(self, x, y):
        tx = ((-x+y)/1.4)
        ty = ((-x-y)/1.4*0.342)
        return int(tx), int(ty)

    #From screen to map
    def to_map(self, win_w, win_h, mx, my):
        xx = win_w/10 + ((mx-my)/1.4 )
        yy = win_h/10 + ((mx+my)/1.4 * 0.342)
        return (xx, yy)

class Sounds(object):
    
    def __init__(self):
        mixer.set_num_channels(8)
        self.a = mixer.Channel(1)
        self.b = mixer.Channel(2)
        self.c = mixer.Channel(3)
        self.d = mixer.Channel(4)
        self.f = mixer.Channel(5)
        self.ambient = mixer.Sound('data/tlo.ogg')
        self.music = mixer.Sound('data/cory_gray_someone_kill_jt.ogg')
        self.passing_sound = mixer.Sound('data/mijanie.ogg')
        self.crash_sound = mixer.Sound('data/uderzenie.ogg')
        self.car_honk = mixer.Sound('data/klakson2.ogg')
        self.tram_bell = mixer.Sound('data/dzwonek_tramwajowy.ogg')

    def background_sounds(self):
        if not self.a.get_busy():
            self.a.set_volume(0.5)
            self.a.play(self.ambient)

        if not self.c.get_busy():
            self.c.set_volume(0.5)
            self.c.play(self.music)

    def passing(self, dist):
        dist = dist/10
        if not self.b.get_busy():
            self.b.play(self.passing_sound)
            self.b.set_volume(1/dist)
        else:
            self.b.set_volume(1/dist)

    def honk(self, car_type):
        if not self.d.get_busy():
            self.d.set_volume(0.3)
            if car_type == 'tram':
                self.d.play(self.tram_bell)
            else:
                self.d.play(self.car_honk)

    def crash(self):
        self.f.set_volume(0.7)
        self.f.play(self.crash_sound)


