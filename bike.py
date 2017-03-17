# -*- coding: utf-8 -*-

from math import pi, sqrt, radians


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

    def game_over_win(self):
        self.win = True

    @staticmethod
    def get_frame(angle):
        # Subtract 3, because texture template doesn't start on 0 angle.
        return int(angle / radians(18) - 3) % 20

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

        self.frame = self.get_frame(self.angle)

        return self.hop
