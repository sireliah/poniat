#-*- coding: utf-8 -*-

from math import pi, sqrt, radians
from random import randint

class Bike(object):

    def __init__(self, px, py, vx, vy, map_w, map_h, lamps_r):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.map_w = map_w
        self.map_h = map_h
        self.angle = radians(pi/2)
        self.acc = 0
        self.frame = 1
        self.turn = 0
        self.health = 100
        self.win = False
        self.lamps_r = lamps_r
        #self.manholes = manholes

    def borders(self):
        if self.px > 3900:
            self.px = self.map_w
            self.game_over_win()
        elif self.px < 0:
            self.px = 0
        if self.py > self.map_h:
            self.py = self.map_h
        elif self.py < 0:
            self.py = 0

        if self.py > 97 and self.py < 98:
            if self.hop == 0:
                self.py = 97
        elif self.py < 11 and self.py > 10:
            if self.hop == 0:
                self.py = 11

        for x, y in self.lamps_r:
            dist = sqrt((self.px - x)**2 + (self.py - y)**2)
            if dist < 2:
                self.vx, self.vy = 0, 0

        #for tup in self.manholes.values():
        #    dist = sqrt((self.px + tup[0][0])**2 + (self.py + tup[0][1])**2)
        #    if dist < 3:
        #        #self.vx, self.vy = randint(-1, 1), randint(-1, 1)
        #        self.angle += radians(randint(-3, 3))
        #        #self.acc = 0

    def game_over_win(self):
        self.win = True

    
    def physics(self, hop):
        self.hop = hop

        self.borders()

        if self.hop > 0:
            self.offset = 1
            self.hop -= 1
        else:
            self.offset = 0

        
        if abs(self.acc) > 0.0001:
            self.acc = self.acc*0.9

        if abs(self.vx) > 0.0001:
            self.vx = self.vx*0.9

        if abs(self.vy) > 0.0001:
            self.vy = self.vy*0.9

        if self.angle > radians(360):
            self.angle = radians(0)
        elif self.angle < radians(0):
            self.angle = radians(360)
        
        if self.angle > radians(72) and self.angle < radians(90):
            self.frame = 0
        if self.angle > radians(90) and self.angle < radians(108):
            self.frame = 1
        if self.angle > radians(108) and self.angle < radians(126):
            self.frame = 2
        if self.angle > radians(126) and self.angle < radians(144):
            self.frame = 3
        if self.angle > radians(144) and self.angle < radians(162):
            self.frame = 4
        if self.angle > radians(162) and self.angle < radians(180):
            self.frame = 5
        if self.angle > radians(180) and self.angle < radians(198):
            self.frame = 6
        if self.angle > radians(198) and self.angle < radians(216):
            self.frame = 7
        if self.angle > radians(216) and self.angle < radians(234):
            self.frame = 8
        if self.angle > radians(234) and self.angle < radians(252):
            self.frame = 9
        if self.angle > radians(252) and self.angle < radians(270):
            self.frame = 10
        if self.angle > radians(270) and self.angle < radians(288):
            self.frame = 11
        if self.angle > radians(288) and self.angle < radians(306):
            self.frame = 12
        if self.angle > radians(306) and self.angle < radians(324):
            self.frame = 13
        if self.angle > radians(324) and self.angle < radians(342):
            self.frame = 14
        if self.angle > radians(342) and self.angle < radians(360):
            self.frame = 15
        if self.angle > radians(0) and self.angle < radians(18):
            self.frame = 16
        if self.angle > radians(18) and self.angle < radians(36):
            self.frame = 17
        if self.angle > radians(36) and self.angle < radians(54):
            self.frame = 18
        if self.angle > radians(54) and self.angle < radians(72):
            self.frame = 19

        return self.hop

