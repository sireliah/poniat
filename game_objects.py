#-*- coding: utf-8 -*-

from math import radians, sqrt
from random import randint
from random import uniform
from textures import Convert

class Car(object):
    
    def __init__(self, name, nr, x, y, v, w, h):
        self.name = name
        self.nr = nr
        self.x = x
        self.y = y
        self.v = v
        self.w = w/2
        self.h = h/2

class People(object):
    
    def __init__(self, name, x, y, v, w, h, side):
        self.name = name
        self.x = x
        self.y = y
        self.v = v
        self.w = w
        self.h = h
        self.side = side

class Populate(object):
        
    def __init__(self, w, h, s):
        self.people_init_nr = 50
        self.cars_init_nr = 10
        self.s = s
        self.w, self.h = w, h
        self.lane1 = []
        self.lane2 = []
        self.lane3 = []
        self.lane4 = []
        self.lane5 = []
        self.lane6 = []
        self.people = []
        self.c = Convert()    
        self.car_nr = 0
        self.density = 30.0
        self.v_range = (2.0, 4.0)
        self.show_auaa = 0
        self.flickering = 0
        self.initial()

    def generate_cars(self, counter=0, spawn_everywhere=False):
        
        def pr():
            return uniform(0.0, 100.0)
 
        velocity = uniform(*self.v_range)
        if spawn_everywhere:
            which = randint(0, 8)
            startx_r = randint(0, self.w)
            if which == 1:
                starty_r = randint(90, 92)
                self.lane1.append(Car("busr", self.car_nr, startx_r, starty_r, velocity, 50, 20))
                self.car_nr += 1
            elif which == 2:
                starty_r = randint(90, 92)
                self.lane1.append(Car("suvr", self.car_nr, startx_r, starty_r, velocity, 40, 18))
                self.car_nr += 1
            elif which == 3:
                starty_r = randint(90, 92)
                self.lane1.append(Car("minir", self.car_nr, startx_r, starty_r, velocity, 25, 16))
                self.car_nr += 1
            elif which == 4:
                starty_r = randint(32, 34)
                self.lane5.append(Car("busl", self.car_nr, startx_r, starty_r, velocity, 50, 20))
                self.car_nr += 1
            elif which == 5:
                starty_r = randint(21, 23)
                self.lane6.append(Car("suvl", self.car_nr, startx_r, starty_r, velocity, 40, 18))
                self.car_nr += 1
            elif which == 6:
                self.lane4.append(Car("tram", self.car_nr, startx_r, 50, velocity, 50, 15))
                self.car_nr += 1
            else:
                self.lane3.append(Car("tram", self.car_nr, startx_r, 60, velocity, 50, 15))
                self.car_nr += 1
        else:
            if counter < 0:
                startx_r = 0
                if pr() < self.density:
                    starty_r = randint(90, 92)
                    self.lane1.append(Car("busr", self.car_nr, startx_r, starty_r, velocity, 50, 20))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    starty_r = randint(80, 82)
                    self.lane2.append(Car("busr", self.car_nr, startx_r, starty_r, velocity, 50, 20))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    starty_r = randint(79, 81)
                    self.lane2.append(Car("suvr", self.car_nr, startx_r, starty_r, velocity, 40, 18))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    starty_r = randint(79, 81)
                    self.lane2.append(Car("minir", self.car_nr, startx_r, starty_r, velocity, 25, 16))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    starty_r = randint(21, 23)
                    self.lane6.append(Car("busl", self.car_nr, self.w, starty_r, velocity, 50, 20))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    starty_r = randint(32, 34)
                    self.lane5.append(Car("busl", self.car_nr, self.w, starty_r, velocity, 50, 20))
                    self.car_nr += 1
                if pr() < self.density:
                    starty_r = randint(32, 34)
                    self.lane5.append(Car("suvl", self.car_nr, self.w, starty_r, velocity, 40, 18))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    starty_r = randint(32, 34)
                    self.lane5.append(Car("sedanl", self.car_nr, self.w, starty_r, velocity, 40, 18))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    self.lane4.append(Car("tram", self.car_nr, self.w, 50, velocity, 50, 15))
                    self.car_nr += 1
                    counter = 100
                if pr() < self.density:
                    self.lane3.append(Car("tram", self.car_nr, startx_r, 60, velocity, 50, 15))
                    self.car_nr += 1
                    counter = 100
        return counter

    def initial(self):
        i = 0
        j = 0
        while i < self.people_init_nr:
            i += 1
            self.generate_people(spawn_everywhere=True)
        
        while j < self.cars_init_nr:
            j += 1
            self.generate_cars(spawn_everywhere=True)

    def generate_people(self, spawn_everywhere=False):
        starty_r = randint(100, 107)
        starty_l = randint(0, 7)
        velocity = uniform(-0.2, 0.2)
        w, h = 3, 3
        if spawn_everywhere:
            which = randint(0, 4)
            startx = randint(0, self.w)
            if which == 0:
                self.people.append(People(1, startx, starty_r, velocity, w, h, 'r'))
            elif which == 1:
                self.people.append(People(1, startx, starty_l, velocity, w, h, 'l'))
            elif which == 2:
                self.people.append(People(2, startx, starty_l, velocity, w, h, 'l'))
            else:
                self.people.append(People(2, startx, starty_r, velocity, w, h, 'r'))
        else:
            ri = randint(0, 1000)
            if ri == 1:
                self.people.append(People(1, 0, starty_r, velocity, w, h, 'r'))
            elif ri == 2:
                self.people.append(People(2, 0, starty_r, velocity, w, h, 'r'))
            elif ri == 3:
                self.people.append(People(1, self.w, starty_l, velocity, w, h, 'l'))
            elif ri == 4:
                self.people.append(People(2, self.w, starty_l, velocity, w, h, 'l'))
            
            
    #@profile    
    def nearest(self, lanelist, car, direction):
        if len(lanelist) > 1:
            if direction == 1:            
                difs = [abs(obj.x-car.x) for obj in lanelist
                    if obj.nr != car.nr and car.x < obj.x]
            else:
                difs = [abs(obj.x-car.x) for obj in lanelist
                    if obj.nr != car.nr and car.x > obj.x]
            if len(difs) > 0:
                minimal_dist = min(difs)
                for obj in lanelist:
                    if abs(obj.x-car.x) == minimal_dist:
                        return obj
                
        else:
            return None
    #@profile
    def car_dynamics(self, xx, yy, bikex):

        #This is the function that handles car movement.
        def simulate(lane, direction):
            for car in lane:
                nearest = self.nearest(lane, car, direction)
                if nearest:
                    if direction == 1:    
                        if car.x+50 > nearest.x:
                            car.v = nearest.v
                        elif car.x+49 > nearest.x:
                            car.x = car.x + nearest.v/2
                        else:
                            car.x = car.x + car.v 
                    else:
                        if car.x-50 < nearest.x:
                            car.v = nearest.v
                        elif car.x-49 < nearest.x:
                            car.x = car.x - nearest.v/2
                        else:
                            car.x = car.x - car.v
                        
                else:
                    car.x = car.x + (car.v * direction)    
            
                del nearest
    
                if car.x < self.w and car.x > 0:
                    bx, by = self.c.to_screen_float(car.x, car.y)
                    if car.name == 'busr':
                        self.busr.show_moving(car.x, car.y, xx, yy, bikex)
                    elif car.name == 'busl':
                        self.busl.show_moving(car.x, car.y, xx, yy, bikex)
                    elif car.name == 'tram':
                        self.tram.show_moving(car.x, car.y, xx, yy, bikex)
                    elif car.name == 'suvr':
                        self.suvr.show_moving(car.x, car.y, xx, yy, bikex)
                    elif car.name == 'minir':
                        self.minir.show_moving(car.x, car.y, xx, yy, bikex)
                    elif car.name == 'suvl':
                        self.suvl.show_moving(car.x, car.y, xx, yy, bikex)
                    elif car.name == 'sedanl':
                        self.sedanl.show_moving(car.x, car.y, xx, yy, bikex)
                else:
                    lane.remove(car)


        for lane in (self.lane1, self.lane2, self.lane3):
            simulate(lane, direction=1)

        for lane in (self.lane4, self.lane5, self.lane6):
            simulate(lane, direction=-1)
    

    #@profile
    def crowd_dynamics(self, xx, yy, bikex):
        for man in self.people:
            if man.side == 'r':
                man.x = man.x + man.v
            else:
                man.x = man.x - man.v
            
            if (man.x < self.w) and (man.x > 0):
                if man.name == 1:
                    if man.v > 0:
                        self.man1.show_moving(man.x, man.y, xx, yy, bikex)
                    else:
                        self.woman1f.show_moving(man.x, man.y, xx, yy, bikex)
                elif man.name == 2:
                    self.man2.show_moving(man.x, man.y, xx, yy, bikex)
            else:
                self.people.remove(man)

    def collisions(self, b):
        self.b = b
        for lane in (self.lane1, self.lane2, self.lane3, self.lane4, self.lane5, self.lane6):
            for car in lane:
                if (self.b.px > car.x-car.w and self.b.px < car.x+car.w) \
                 and (self.b.py > car.y-car.h and self.b.py < car.y+car.h-3):
                    pass
                    self.show_auaa = 50
                    self.flickering = 100
                    self.s.crash()
                    self.b.vx, self.b.vy = randint(-2, 2), randint(-2, 2)
                    self.b.angle += radians(randint(-10, 10))
                    self.b.acc = 0
                    self.b.health -= 3
                dist_front = self.b.px - car.x
                if (self.b.px > car.x and dist_front < 50) and ( self.b.py < car.y + 10 ):
                     self.s.honk(car.name) 

                dist = sqrt((self.b.px - car.x)**2 + (self.b.py - car.y)**2)
                if dist < 60:
                    self.s.passing(dist)
                
        for man in self.people:
            if (self.b.px > man.x-man.w and self.b.px < man.x+man.w) \
             and (self.b.py > man.y-man.h and self.b.py < man.y+man.h):
                self.b.vx, self.b.vy = 0, 0
                self.b.acc = 0

        return self.b.acc

            

