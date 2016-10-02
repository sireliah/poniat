#-*- coding: utf-8 -*-

import pygame
from OpenGL.GL import *
from textures import *
from primitives import *
from utils import *

class Surf(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Poniat v0.7')
        num = 0
        self.modes = pygame.display.list_modes(32)
        
        #Let's not use too big resolution
        if self.modes[num] > (1920, 1080):
            self.win_w = 1920
            self.win_w = 1080
        else:
            self.win_w = self.modes[num][0]
            self.win_h = self.modes[num][1]

        print(self.win_w, self.win_h)
        self.surface = pygame.display.set_mode((self.win_w, self.win_h), \
                                                pygame.OPENGL \
                                              | pygame.DOUBLEBUF \
                                              | pygame.FULLSCREEN )
        self.cursor(False)

    def cursor(self, visible):
        if visible:
            pygame.mouse.set_visible(1)
        else:
            pygame.mouse.set_visible(0)

    def opengl(self, menu=False):
        glClearColor(0.2, 0.4, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)            
        glLoadIdentity()
        glViewport(0, 0, self.win_w, self.win_h)
        if menu:        
            glOrtho(0, self.win_w, self.win_h, 0, -100, 400)
        else:
            glOrtho(0, self.win_w/6, self.win_h/5, 0, -3000, 4000)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


class MapModel(object):

    def __init__(self):
        self.lane1r_dic = {}
        self.lane2r_dic = {}
        self.pavl_dic = {}
        self.pavr_dic = {}
        self.tram_dic = {}
        self.lane2l_dic = {}
        self.lane1l_dic = {}
        self.manhole_dic = {}
        self.lampr_dic = []
        self.lampl_dic = []
        self.benchr_dic, self.benchl_dic = [], []
        self.points = []
        self.map = pygame.image.load("data/mapa3.png")
        self.map.lock()
        self.w, self.h = self.map.get_size()
        self.parse_pixels()
       
    def sew_lanes(self, lane, obj, x, y):
        if len(obj) == 4 and len(lane) == 0:
            lane[1] = obj
            obj = obj[:0]
            obj.append((-x, -y))
        else:
            obj.append((-x, -y))

        ld = len(lane)
        if ld > 0 and len(obj) == 2:
            lane[ld+1] = (lane[ld][-2], lane[ld][-1], obj[-2], obj[-1])
            obj = obj[:0]
        return lane, obj
            
    def parse_pixels(self):
        obj1, obj2, obj3, obj4, obj5, obj6, obj7 = [], [], [], [], [], [], []
        for x in range(self.w):
            for y in range(self.h):
                r, g, b, a = self.map.get_at((x, y))

                if (r, g, b) == (255, 0, 0):
                    self.lane1r_dic, obj1 = self.sew_lanes(self.lane1r_dic, obj1, x, y)
                elif (r, g, b) == (0, 255, 0):
                    self.lane2r_dic, obj2 = self.sew_lanes(self.lane2r_dic, obj2, x, y)
                elif (r, g, b) == (0, 255, 255):
                    self.pavl_dic, obj3 = self.sew_lanes(self.pavl_dic, obj3, x, y)
                elif (r, g, b) == (100, 100, 254):
                    self.tram_dic, obj7 = self.sew_lanes(self.tram_dic, obj7, x, y)
                #Teraz lewe pasy    
                elif (r, g, b) == (254, 0, 0):
                    self.lane1l_dic, obj4 = self.sew_lanes(self.lane1l_dic, obj4, x, y)
                elif (r, g, b) == (0, 254, 0):                
                    self.lane2l_dic, obj5 = self.sew_lanes(self.lane2l_dic, obj5, x, y)
                elif (r, g, b) == (0, 255, 254):
                    self.pavr_dic, obj6 = self.sew_lanes(self.pavr_dic, obj6, x, y)
                #elif (r, g, b) == (150, 150, 150):
                #    self.manhole_dic[-x] = ((-x, -y), (-x, -y-4), (-x-4, -y), (-x-4, -y-4))
                elif (r, g, b) == (255, 0, 255):
                    self.lampr_dic.append((x, y))
                elif (r, g, b) == (100, 0, 255):
                    self.lampl_dic.append((x, y))
                elif (r, g, b) == (255, 180, 100):
                    self.benchl_dic.append((x, y))
                elif (r, g, b) == (0, 180, 100):
                    self.benchr_dic.append((x, y))
                elif (r, g, b) == (255, 254, 0):
                    self.tower_powisle_r = (x, y)
                elif (r, g, b) == (255, 255, 0):
                    self.tower_powisle_l = (x, y)
                elif (r, g, b) == (255, 210, 0):
                    self.tower_praga_l = (x, y)
                elif (r, g, b) == (255, 190, 0):
                    self.tower_praga_r = (x, y)
                elif (r, g, b) == (100, 50, 100):
                    self.junctionl = (-x, -y)
                elif (r, g, b) == (100, 100, 100):
                    self.junctionr = (-x, -y)
                

class LoadBikeFrames(object):

    def __init__(self, fil):
        self.fil = fil
        self.img = pygame.image.load(self.fil)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.list = []

        for y in range(0, self.height, 100):
            row = []
            for x in range(0, self.width, 100):
                rect = (x, y, 100, 100)
                frame = self.img.subsurface(rect)
                row.append(frame)
        
            self.list.append(row)

    def return_frames(self):
        return self.list


class LoadTextures(object):
        
    def __init__(self, mm):
        self.list_tex = []
        self.mm = mm
        self.bikeframes = LoadBikeFrames("data/rower2.png").return_frames()
        self.bike_textures = []
        for row_num, row in enumerate(self.bikeframes):
            for turn, frame in enumerate(row): 
                self.bike_textures.append(BikeTex(frame, row_num, turn))
        self.back = Background("data/tlo5.png", self.win_w, self.win_h)
        self.font = Font("data/unikod.png")
        self.ouch = Tex({1:1}, "data/alaaa.png", rect=(30, 30))
        self.endgame = Tex({1:1}, "data/koniecgry.png", rect=(100, 75))
        self.winback = Background("data/win.png", self.win_w, self.win_h, static=True)
        self.busr = Tex({1:1}, "data/autobus3.png", rect=(17, 8))
        self.busl = Tex({1:1}, "data/autobusl.png", rect=(17, 8))
        self.suvr = Tex({1:1}, "data/suvp.png", rect=(13, 6))
        self.minir = Tex({1:1}, "data/minip.png", rect=(10, 4))
        self.suvl = Tex({1:1}, "data/suvl.png", rect=(13, 6))
        self.sedanl = Tex({1:1}, "data/sedanl.png", rect=(13, 6))
        self.tram = Tex({1:1}, "data/tramwaj3.png", rect=(17, 8))
        self.man1 = Tex({1:1}, "data/czlowiek1.png", rect=(1, 2))
        self.woman1f = Tex({1:1}, "data/czlowiek3f.png", rect=(1, 2))
        self.man2 = Tex({1:1}, "data/czlowiek2.png", rect=(1, 2))
        self.lampr = TexSimple(self.mm.lampr_dic, "data/latarniap.png", shift=(5, -40, -5, -40, -5, 3, 5, 3))
        self.lampl = TexSimple(self.mm.lampl_dic, "data/latarnial.png", shift=(5, -40, -5, -40, -5, 3, 5, 3))
        self.benchr = TexSimple(self.mm.benchr_dic, "data/lawkap.png")
        self.benchl = TexSimple(self.mm.benchl_dic, "data/lawkal.png")
        self.tower_powisle_r = TexSimple(self.mm.tower_powisle_r, "data/wiezyca_powisle.png")
        self.tower_powisle_l = TexSimple(self.mm.tower_powisle_l, "data/wiezyca_powisle.png")    
        self.tower_praga_r = TexSimple(self.mm.tower_praga_r, "data/wiezyca_praga.png")
        self.tower_praga_l = TexSimple(self.mm.tower_praga_l, "data/wiezyca_praga.png")
        self.foundation = Tex(self.mm.pavl_dic, "data/nasyp_praga.png")
        self.pylons = Tex(self.mm.pavl_dic, "data/arkad3.png")
        self.llaner = Tex(self.mm.lane1r_dic, "data/buspas.png")
        self.llane2r = Tex(self.mm.lane2r_dic, "data/pas_ulicap.png")
        self.llane1l = Tex(self.mm.lane1l_dic, "data/buspasl.png")
        self.llane2l = Tex(self.mm.lane2l_dic, "data/pas_ulical.png")
        #self.manhole = Tex(self.mm.manhole_dic, "data/pas_studzienka.png")
        self.tram_obj = Tex(self.mm.tram_dic, "data/pas_tram.png")
        self.pavement = Tex(self.mm.pavr_dic, "data/pas_chodnik.png")
        self.pavementl = Tex(self.mm.pavl_dic, "data/pas_chodnik.png")
        self.railingr = Tex(self.mm.pavr_dic, "data/barierka.png")
        self.railingl = Tex(self.mm.pavl_dic, "data/barierka.png", l=True)
        self.junctionl = Tex(self.mm.junctionl, "data/rozjazdl.png", l=True)
        self.junctionr = Tex(self.mm.junctionr, "data/rozjazdl.png")
        self.frame = Quad(51, 20, GRAY, 0.7)
        self.frame_endgame = Quad(350, 100, GRAY, 0.7)
        self.health_bar = Quad(50, 6, RED, 0.7)
        self.lives_bar = Quad(6, 6, DARKRED, 0.7)
        
        

class LoadMenuTextures(object):

    def __init__(self, win_w, win_h):
        self.font = Font("data/unikod.png")
        self.mainback = Background("data/front.png", win_w, win_h, static=True)
        self.aboutback = Background("data/idea.png", win_w, win_h, static=True)
        w = win_w/10
        h = win_h/3
        self.start_coords = (w, h, w, h*1.2, w*3, h*1.2, w*3, h)
        self.about_coords = (w, h*1.2, w, h*1.4, w*3, h*1.4, w*3, h*1.2)
        self.exit_coords = (w, h*1.4, w, h*1.6, w*3, h*1.6, w*3, h*1.4)
        self.goback_coords = (w*6, h*2.6, w*6, h*2.8, w*8, h*2.8, w*8, h*2.6)

        self.frame = Quad(350, 100, BLACK, 1.0)
        self.start = TexSimple(self.start_coords, "data/start.png", static=True)
        self.about = TexSimple(self.about_coords, "data/oidei.png", static=True)
        self.goback = TexSimple(self.goback_coords, "data/wroc.png", static=True)
        self.exit = TexSimple(self.exit_coords, "data/wyjdz.png", static=True)


    


