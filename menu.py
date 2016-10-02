#-*- coding: utf-8 -*-

import sys
import pygame
from pygame.locals import *
from utils import *
from initial import LoadMenuTextures

class MainMenu(LoadMenuTextures):
    
    def __init__(self, modes, win_w, win_h):
        self.showmain = True
        self.submenu = False
        self.click = False
        self.modes = modes
        LoadMenuTextures.__init__(self, win_w, win_h)
        self.menuloop()

    def mousepos(self):
        self.pos = pygame.mouse.get_pos()
    
    def is_inside(self, coords):
        x, y = self.pos
        if (x > coords[0] and x < coords[4]) and (y > coords[1] and y < coords[5]):
            return True
        else:
            return False 
    
    def startbutton(self):
        if self.is_inside(self.start_coords):
            self.start.show_button(hover=True)
            if self.click:
                self.showmain = False
        else:
            self.start.show_button()

    def aboutbutton(self):
        if self.is_inside(self.about_coords):
            self.about.show_button(hover=True)
            if self.click:
                self.submenu = True
        else:
            self.about.show_button()

    def gobackbutton(self):
        if self.is_inside(self.goback_coords):
            self.goback.show_button(hover=True)
            if self.click:
                self.submenu = False
        else:
            self.goback.show_button()


    def exitbutton(self):
        if self.is_inside(self.exit_coords):
            self.exit.show_button(hover=True)
            if self.click:
                sys.exit()
        else:
            self.exit.show_button()

    def events(self):
        self.mousepos()
        self.click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                print("koniec")
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                if event.key == K_SPACE:
                    pass
                if event.key == K_RETURN:
                    self.showmain = False
                if event.key == K_LCTRL:
                    pass
            elif event.type == MOUSEBUTTONDOWN:
                self.click = True
    
    def menuloop(self):
        while self.showmain:
            clear()
            self.events()
            self.mainback.show(0, 0)
            if self.submenu:
                self.aboutback.show(0, 0)
                self.gobackbutton()
            else:
                self.startbutton()
                self.aboutbutton()
                self.exitbutton()
            self.font.show(u"X: %s, Y: %s" % (self.pos), DARKRED, 10, 30, 1, 1)
            pygame.display.flip()
        clear()
        self.mainback.show(0, 0)
        self.frame.show(13, 14, 1.0, 1.0)
        self.font.show(u"Ładuję...", DARKRED, 10, 30, 2, 2)
        pygame.display.flip()



