#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
    Poniat 0.7
    for more info, please visit http://sourceforge.net/projects/poniat/
 
    Copyright (C) 2015 Piotr Gołąb

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


    In this piece of software I used music by Cory Gray 
    on Creative Commons Attribution-NonCommercial 3.0 license
    for more information, please visit:
    http://freemusicarchive.org/music/Cory_Gray/
"""

import pygame
import math
import datetime
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from utils import *
from menu import MainMenu
from initial import *
from textures import *
from game_objects import *
from bike import Bike


class Play(LoadTextures, Surf, Populate):

    def __init__(self):
        self.startx, self.starty = 250, 102
        self.elapsed = 0
        self.lives = 3
        self.hop = 0
        Surf.__init__(self)
        self.cursor(True)
        self.opengl(menu=True)
        menu = MainMenu(self.modes, self.win_w, self.win_h)
        menu.menuloop()
        self.cursor(False)
        self.opengl()
        self.s = Sounds()
        self.mm = MapModel()
        self.clock = pygame.time.Clock()
        self.c = Convert()
        LoadTextures.__init__(self, self.mm)        
        self.b = Bike(self.startx, self.starty, 0, 0, self.mm.w, self.mm.h, self.mm.lampr_dic)
        Populate.__init__(self, self.mm.w, self.mm.h, self.s)




    
    def show_bike(self):
        for frame in self.bike_textures:
            if (self.b.frame == frame.row_num) and (round(self.b.turn) == frame.turn):
                if self.flickering == 0:
                    frame.show(self.win_w/10, self.win_h/10-self.b.offset)
                else:
                    if (self.flickering % 2 == 0):                   #Check if number is even or odd
                        frame.show(self.win_w/10, self.win_h/10-self.b.offset)
                        self.flickering -= 1
                    else:
                        self.flickering -= 1
        if self.b.turn < 3:
            if self.b.acc > 0.01:
                self.b.turn += 0.1
        else:
            self.b.turn = 0

    def print_time(self):
        t = datetime.timedelta(milliseconds=self.elapsed)
        try:
            f = datetime.datetime.strptime(str(t), '%H:%M:%S.%f')
        except ValueError:
            f = datetime.datetime.strptime(str(t), '%H:%M:%S')
        return "%s:%s" % (f.minute, f.second)

    def game_logic(self):

        def win():
            self.hang = True
            while self.hang:
                clear()
                self.opengl(menu=True)
                self.winback.show(0, 0)
                self.frame_endgame.show(int(self.win_w/3), 10, 1.0, 1.0)                
                self.font.show(u"Twój czas to: %s" % self.print_time(), RED, int(self.win_w/4), int(self.win_h*0.46), 1.5, 1.5)
                self.frame.show(int(self.win_w/15), int(self.win_w/10), 2.5, 1.0)
                self.points = int(900-(self.elapsed/1000)+self.b.health)
                self.font.show(u"Punkty: %s" % str(self.points), RED, int(self.win_w/4), int(self.win_h*0.53), 1.5, 1.5)
                self.events()
                if self.enter:
                    self.font.show(u"Naciśnij [ENTER], żeby zakończyć.", RED, int(self.win_w/4), int(self.win_h*0.66), 1.5, 1.5)
                else:
                    self.font.show(u"Naciśnij [ENTER], żeby zakończyć.", BLUE, int(self.win_w/4), int(self.win_h*0.66), 1.5, 1.5)
                pygame.display.flip()
            sys.exit()

        def end():
            clear()
            self.endgame.show_static(int(self.win_w/12), int(self.win_h/12))
            pygame.display.flip()
            pygame.time.wait(3000)
            self.b.px = self.startx
            self.b.py = self.starty
            self.b.vx, self.b.vy = 0, 0    
            self.b.health = 100
            self.lives -= 1
            self.flickering = 100
            self.show_auaa = 0
            
        if self.b.health <= 0:
            end()
        if self.lives == 0:
            end()
            print("koniec")
            sys.exit()

        if self.b.win:
            win()
            

    #@profile
    def mainloop(self):
        counter = 0
        while True:
            clear()
            self.events()
            self.s.background_sounds()
            self.hop = self.b.physics(self.hop)
            self.game_logic()
            
            self.b.vx += math.sin(self.b.angle) * self.b.acc
            self.b.vy += math.cos(self.b.angle) * self.b.acc

            self.b.px = self.b.px + self.b.vx
            self.b.py = self.b.py + self.b.vy
    
            self.back.show(self.b.px/10, self.b.py/5)
            xx, yy = self.c.to_map(self.win_w, self.win_h, self.b.px, self.b.py)

            self.junctionr.show_quad(xx, yy, self.b.px)
            self.railingr.show_quad(xx, yy, self.b.px)
            self.benchr.show(xx, yy, self.b.px)
            self.lampr.show(xx, yy, self.b.px)
            self.pavement.show_quad(xx, yy, self.b.px)
            self.llaner.show_quad(xx, yy, self.b.px)
            self.llane2r.show_quad(xx, yy, self.b.px)
            self.tram_obj.show_quad(xx, yy, self.b.px)
            self.llane2l.show_quad(xx, yy, self.b.px)
            self.llane1l.show_quad(xx, yy, self.b.px)
            #self.manhole.show_quad(xx, yy, self.b.px)
            self.pavementl.show_quad(xx, yy, self.b.px)
            self.tower_powisle_r.show(xx, yy, self.b.px) 
            self.tower_praga_r.show(xx, yy, self.b.px) 
    
            self.show_bike()

            self.generate_people()
            self.crowd_dynamics(xx, yy, self.b.px)
            counter = self.generate_cars(counter=counter)
            counter -= 1

            self.car_dynamics(xx, yy, self.b.px)
            self.railingl.show_quad(xx, yy, self.b.px)
            self.lampl.show(xx, yy, self.b.px)
            self.foundation.show_quad(xx, yy, self.b.px)
            self.pylons.show_quad(xx, yy, self.b.px)
            self.benchl.show(xx, yy, self.b.px)
            self.junctionl.show_quad(xx, yy, self.b.px)
            self.tower_powisle_l.show(xx, yy, self.b.px)
            self.tower_praga_l.show(xx, yy, self.b.px)
            
            self.b.acc = self.collisions(self.b)
            if self.show_auaa > 0:
                self.ouch.show_static(self.win_w/9, self.win_h/14)
                self.show_auaa -= 1            
            fps = self.clock.get_fps()
            self.frame.show(9, 9, 1.1, 1.5)
            self.health_bar.show(10, 20, self.b.health/100.0, 1.0)
            self.font.show(u"fps: %s" % round(fps, 1), BLUE, 10, 10, 0.2, 0.2)
            self.font.show(u"Zdrowie: %s" % self.b.health, RED, 10, 20, 0.2, 0.2)
            self.font.show(u"Życia: ", DARKRED, 10, 30, 0.2, 0.2)
            for life in range(self.lives):
                self.lives_bar.show(35+(life*10), 30, 1.0, 1.0)
            
            #self.clock.tick_busy_loop(100)
            self.elapsed += self.clock.tick(100)
            self.frame.show(int(self.win_w/15), 10, 0.7, 0.5)
            self.font.show(u"Czas: %s" % self.print_time(), RED, int(self.win_w/15), 10, 0.2, 0.2)
            pygame.display.flip()



    def events(self):
        self.enter = False
        for event in pygame.event.get():
            if event.type == QUIT:
                print("koniec")
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_SPACE:
                    self.hop = 5
                if event.key == K_RETURN:
                    self.hang = False
                    self.enter = True
                if event.key == K_LCTRL:
                    self.b.acc += 0.1

        keys = pygame.key.get_pressed()

        if keys[K_UP]:
            self.b.acc += 0.01
        if keys [K_LSHIFT]:
            self.b.acc += 0.1
        if keys[K_DOWN]:
            self.b.acc -= 0.01
        if keys[K_LEFT]:
            self.b.angle = self.b.angle + math.radians(2)
        elif keys[K_RIGHT]:
            self.b.angle = self.b.angle - math.radians(2)

    #Helper function
    def punkt(self, x, y, xx, yy):
        coords = self.c.to_screen_int(x, y)
        glLoadIdentity()
        glTranslatef(xx, yy, 0)
        glPointSize(10.0)
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POINTS)
        #glVertex2f(*coords)
        #print "punkt %s %s" % (coords[0], coords[1])
        glVertex2f(coords[0], coords[1]-20)
        glEnd()


if __name__ == '__main__':
    p = Play()
    p.mainloop()


