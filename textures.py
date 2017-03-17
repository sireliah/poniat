# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from OpenGL.GL import *
from utils import *


class Font(object):

    def __init__(self, fil):
        self.fil = fil
        self.img = pygame.image.load(self.fil)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img_to_str = pygame.image.tostring(self.img, "RGBA", 0)
        self.tex_obj = glGenTextures(1)
        self.w = 18
        self.h = 33
        self.letters_num = float(349.0)
        self.lists = []
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_to_str)
        self.prepare()

    def prepare(self):
        x = 0
        for a in range(ord(u' '), ord(u'Ž')):
            z = 1
            listgl = glGenLists(1)
            glNewList(listgl, GL_COMPILE)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex_obj)

            glBegin(GL_QUADS)
            glTexCoord2f(float(x)/self.letters_num, 1)
            glVertex2i(-int(self.w), int(self.h))

            glTexCoord2f(float(x+z)/self.letters_num, 1)
            glVertex2i(0, int(self.h)) 

            glTexCoord2f(float(x+z)/self.letters_num, 0)
            glVertex2i(0, 0) 

            glTexCoord2f(float(x)/self.letters_num, 0)            
            glVertex2i(-int(self.w), 0)
            glEnd()
            glDisable(GL_TEXTURE_2D)
            glEndList()
            self.lists.append(listgl)
            x = x + 1

    def show(self, text, color, xx, yy, scx, scy):
        c = 0
        glLoadIdentity()
        #glColor3f(*color)
        #glColor4f(1.0, 1.0, 1.0, 0.5)        
        glTranslatef(xx, yy, 0)
        glScalef(scx, scy, 1)
        while c < len(text):
            glTranslatef(18, 0, 0)
            lis = self.lists[ord(text[c])-ord(u' ')]
            glCallList(lis)
            c += 1


class Tex(Convert):

    def __init__(self, coord_dict, fil, l=False, rect=()):
        self.c = Convert()
        self.cd = coord_dict
        self.fil = fil
        self.l = l
        self.lists = []
        self.dic = {}
        self.img = pygame.image.load(self.fil)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img_to_str = pygame.image.tostring(self.img, "RGBA", 0)
        self.tex_obj = glGenTextures(1)
        self.r = self.img.get_rect()
        self.rect = rect
        self.howfar = 300 #viewing distance

        self.identify_objects()        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_to_str)

    def identify_objects(self):

        if "barierka" in self.fil:

            for obj in self.cd.values():
                if self.l:
                    self.barl(obj)
                else:
                    self.bar(obj)
        elif "nasyp" in self.fil:
            self.foundation(self.cd[1])
        elif "rozjazd" in self.fil:
            if self.l:
                coords = [self.cd, (self.cd[0], self.height//2), (self.cd[0]-self.width//2, 0), \
                           (self.cd[0]-self.width//2, self.height//2)]
            else:
                coords = [self.cd, (self.cd[0], -self.height//2), (self.cd[0]-self.width//2, 0), \
                           (self.cd[0]-self.width//2, -self.height//2)]

            self.quad(coords)
        elif "arkad" in self.fil:
            for obj in self.cd.values():
                i = 1
                pyl_list = []
                #Iterate every other object in the dictionary.
                for obj2 in list(self.cd.values())[1::2]:
                    #After the first turn add 4 coordinates.
                    if i == 1:
                        del pyl_list[:]
                        pyl_list.append(obj2[0])
                    #After the second turn, add only last coordinate.
                    if i == 2:
                        pyl_list.append((obj2[-1][0]-2, obj[-1][1]))
                        self.pylons(pyl_list)
                        i = 0
                    i = i + 1
        else:
            for obj in self.cd.values():
                if "pas" in self.fil:
                    self.quad(obj)
                else:
                    self.simple_obj(obj)


    def quad(self, o):
        listgl = glGenLists(1)
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)    
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)

        glRotatef(70, 1, 0, 0)
        glRotatef(45, 0, 0, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2i(o[3][0], o[3][1]) 

        glTexCoord2f(0, 1)
        glVertex2i(o[2][0], o[2][1]) 

        glTexCoord2f(1, 1)
        glVertex2i(o[0][0], o[0][1]) 
        
        glTexCoord2f(1, 0)
        glVertex2i(o[1][0], o[1][1])
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.dic[o[0][0]] = listgl



    def bar(self, o):
        coord = self.c
        listgl = glGenLists(1)
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)        
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2i( coord(-o[3][0], -o[3][1])[0], coord(-o[3][0], -o[3][1])[1]-2 )

        glTexCoord2f(0, 1)
        glVertex2i( coord(-o[2][0], 107)[0], coord(-o[2][0], 107)[1] ) 

        glTexCoord2f(1, 1)
        glVertex2i( coord(-o[0][0], 107)[0], coord(-o[0][0], 107)[1] ) 

        glTexCoord2f(1, 0)
        glVertex2i( coord(-o[1][0], -o[1][1])[0], coord(-o[1][0], -o[1][1])[1]-2 )
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.dic[o[0][0]] = listgl



    def barl(self, o):
        listgl = glGenLists(1)
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)    
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        
        glRotatef(20, 1, 0, 0)
        glRotatef(45, 0, 1, 0)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2i(o[3][0], -2) 

        glTexCoord2f(0, 1)
        glVertex2i(o[2][0], o[2][1]) 

        glTexCoord2f(1, 1)
        glVertex2i(o[0][0], o[0][1]) 

        glTexCoord2f(1, 0)
        glVertex2i(o[1][0], -2)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.dic[o[0][0]] = listgl


    def pylons(self, o, length=0.85):
        listgl = glGenLists(1)
        
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)        
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glRotatef(31.8, 1, 0, 0)
        glRotatef(33, 0, 1, 0)

        glBegin(GL_QUADS)
        glTexCoord2f(1, 1)
        glVertex2i(int(o[0][0]*length), 200)

        glTexCoord2f(0, 0)
        glVertex2i(int(o[1][0]*length), 0) 

        glTexCoord2f(0, 1)
        glVertex2i(int(o[1][0]*length), 200)

        glTexCoord2f(1, 0)
        glVertex2i(int(o[0][0]*length), 0) 
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.dic[o[0][0]] = listgl

    def foundation(self, o):
        listgl = glGenLists(1)
        
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)        
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glRotatef(31.8, 1, 0, 0)
        glRotatef(33, 0, 1, 0)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2i(o[3][0], 0)

        glTexCoord2f(0, 1)
        glVertex2i(o[2][0], 140)

        glTexCoord2f(1, 1)
        glVertex2i(o[0][0], 140) 

        glTexCoord2f(1, 0)
        glVertex2i(o[1][0], 0) 
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.dic[o[0][0]] = listgl

    def simple_obj(self, o):
        x, y = self.rect
        listgl = glGenLists(1)
        glNewList(listgl, GL_COMPILE)    
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2i(-x, y)

        glTexCoord2f(1, 1)
        glVertex2i(x, y)

        glTexCoord2f(1, 0)
        glVertex2i(x, -y)

        glTexCoord2f(0, 0)
        glVertex2i(-x, -y)
        
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.lists.append(listgl)

    def show_quad(self, xx, yy, bikex):
        for num, lis in self.dic.items():
            dist = abs(num)- abs(bikex)
            if dist < self.howfar:
                glLoadIdentity()
                glTranslatef(xx, yy, 0)
                glCallList(lis)
        
    def show_static(self, xx, yy):
        glLoadIdentity()
        glTranslatef(xx, yy, 0)    
        glCallList(self.lists[0])
    
    def show_moving(self, cx, cy, xx, yy, bikex):
        dist = abs(cx  - bikex)
        if dist < self.howfar:
            cx, cy = self.c.to_screen_float(cx, cy)
            glLoadIdentity()
            glTranslatef(xx+cx, yy+cy, 0)
            glCallList(self.lists[0])


class TexSimple(object):

    def __init__(self, coord_list, fil, static=False, shift=False):
        self.c = Convert()
        self.coord_list = coord_list
        self.fil = fil
        self.lists = {}
        self.static = static
        self.shift = shift
        self.img = pygame.image.load(self.fil)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img_to_str = pygame.image.tostring(self.img, "RGBA", 0)
        self.tex_obj = glGenTextures(1)
        self.r = self.img.get_rect()
        self.howfar = 300

        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_to_str)

        if not self.shift:
            self.shift = (int(self.width/4), -int(self.height/4), \
                           -int(self.width/4), -int(self.height/4), \
                           -int(self.width/4), int(self.height/4), \
                            int(self.width/4), int(self.height/4))
        # Try to iterate an object that stores coordinates. 
        # If you encounter an exception, the object is probably a tuple, not a list.
        if self.static:
            self.flat(self.coord_list)
        else:
            try:
                for obj in self.coord_list:
                    self.perspective(obj)
            except (TypeError):
                self.perspective(self.coord_list)

    def perspective(self, o):
        coords = self.c.to_screen_int(*o)
        listgl = glGenLists(1)
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)

        glBegin(GL_QUADS)
        glTexCoord2f(1, 0)
        glVertex2i( coords[0]+self.shift[0], coords[1]+self.shift[1] )

        glTexCoord2f(0, 0)
        glVertex2i( coords[0]+self.shift[2], coords[1]+self.shift[3] )

        glTexCoord2f(0, 1)
        glVertex2i( coords[0]+self.shift[4], coords[1]+self.shift[5] )
        
        glTexCoord2f(1, 1)
        glVertex2i( coords[0]+self.shift[6], coords[1]+self.shift[7] )
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.lists[o[0]] = listgl

    def flat(self, o):
        listgl = glGenLists(1)
        glNewList(listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2i(int(o[0]), int(o[1]))

        glTexCoord2f(0, 1)
        glVertex2i(int(o[2]), int(o[3]))

        glTexCoord2f(1, 1)
        glVertex2i(int(o[4]), int(o[5]))
        
        glTexCoord2f(1, 0)
        glVertex2i(int(o[6]), int(o[7]))
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        self.lists = []
        self.lists.append(listgl)

    def show(self, xx, yy, bikex):
        for num, lis in self.lists.items():
            dist = abs(num) - abs(bikex)
            if dist < self.howfar:
                glLoadIdentity()
                glTranslatef(xx, yy, 0)
                glCallList(lis)

    def show_button(self, hover=False):
        glLoadIdentity()
        if hover:
            glTranslatef(1, 1, 0)
        glCallList(self.lists[0])


class BikeTex(object):

    def __init__(self, img, row_num, turn):
        self.row_num = row_num
        self.turn = turn
        self.img = img
        self.img_to_str = pygame.image.tostring(self.img, "RGBA", 0)
        self.tex_obj = glGenTextures(1)
        self.r = self.img.get_rect()
        self.width = self.img.get_width()
        self.height = self.img.get_height()

        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_to_str)
        self.prepare()

    def prepare(self):
        i = 4
        self.listgl = glGenLists(1)
        glNewList(self.listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glBegin(GL_QUADS)

        glTexCoord2f(0, 1)
        glVertex2i(-i, i)

        glTexCoord2f(1, 1)
        glVertex2i(i, i)

        glTexCoord2f(1, 0)
        glVertex2i(i, -i)

        glTexCoord2f(0, 0)
        glVertex2i(-i, -i)

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
        
    def show(self, xx, yy):
        glLoadIdentity()
        glTranslatef(xx, yy, 0)
        glCallList(self.listgl)


class Background(object):

    def __init__(self, fil, w, h, static=False):
        self.fil = fil
        self.w = w
        self.h = h
        self.static = static
        self.img = pygame.image.load(self.fil)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.img_to_str = pygame.image.tostring(self.img, "RGBA", 0)
        self.tex_obj = glGenTextures(1, self.img)
        self.r = self.img.get_rect()
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_to_str)
        
        self.back()

    def back(self):
        self.listgl = glGenLists(1)
        glNewList(self.listgl, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)    
        glBindTexture(GL_TEXTURE_2D, self.tex_obj)    
        glColor3f(34.0, 255.0, 1.0)
        if not self.static:
            glScalef(0.25, 0.25, 0)
            self.w = self.r.w
        glBegin(GL_QUADS)

        glTexCoord2f(0, 0)
        glVertex2i(0, 0)

        glTexCoord2f(0, 1)
        glVertex2i(0, self.h)

        glTexCoord2f(1, 1)
        glVertex2i(self.w, self.h)    
    
        glTexCoord2f(1, 0)
        glVertex2i(self.w, 0)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()


    def show(self, xx, yy):
        glLoadIdentity()
        if not self.static:
            glTranslatef(xx-300, yy-50, 0)
        glCallList(self.listgl)


