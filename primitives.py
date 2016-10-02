#-*- coding: utf-8 -*-

from OpenGL.GL import *

class Quad(object):
    
    def __init__(self, w, h, color, transparency):
        self.w = w
        self.h = h
        self.c = color
        self.transparency = transparency
        self.listgl = glGenLists(1)
        glNewList(self.listgl, GL_COMPILE)
        self.prepare()
    
    def prepare(self):
        i = self.w
        glColor4f(self.c[0], self.c[1], self.c[2],  self.transparency)
        glBegin(GL_QUADS)
        glVertex2i(0, 0)
        glVertex2i(0, self.h)
        glVertex2i(self.w, self.h)
        glVertex2i(self.w, 0)
        glEnd()
        glEndList()
        

    def show(self, xx, yy, scalex, scaley):
        glLoadIdentity()
        glTranslatef(xx, yy, 0)
        glScalef(scalex, scaley, 1.0)
        glCallList(self.listgl)
