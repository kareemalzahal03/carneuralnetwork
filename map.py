import pygame
from point import Point
from math import floor, pi

class NewMap:
    def __init__(map, info):
        map.road_width = 200

        map.info = info

        map.dir = Point(1,0).rotate(map.info.start_angle)
        map.lp = map.info.start_pos - Point(-map.dir.y, map.dir.x) * (map.road_width/2)
        map.rp = map.info.start_pos + Point(-map.dir.y, map.dir.x) * (map.road_width/2)
        map.lps = [map.lp.tuple()]
        map.rps = [map.rp.tuple()]
        map.cps = []

        map.load(map.info.draw_path)
        map.reset_cp()

    def draw(map, screen, hitboxes = False):

        if map.info.clockwise:
            pygame.draw.polygon(screen, (0,0,0), map.lps)
            pygame.draw.polygon(screen, (0,150,0), map.rps)
        else:
            pygame.draw.polygon(screen, (0,0,0), map.rps)
            pygame.draw.polygon(screen, (0,150,0), map.lps)

        pygame.draw.lines(screen, (0,100,0), False, map.rps, 5)
        pygame.draw.lines(screen, (0,100,0), False, map.lps, 5)

        if hitboxes:
            pygame.draw.lines(screen, (255,255,0), False, map.rps)
            pygame.draw.lines(screen, (255,255,0), False, map.lps)
            for p0, p1 in map.cps:
                pygame.draw.line(screen, (255,200,200), p0, p1)
            pygame.draw.line(screen, (255,0,0), map.cp[0], map.cp[1])

    def reset_cp(map):
        map.cp_index = map.info.start_cp_index
        map.cp = map.cps[map.cp_index]

    def inc_cp(map):
        map.cp_index = map.cp_index + 1 if map.cp_index < len(map.cps) - 1 else 0
        map.cp = map.cps[map.cp_index]

    def load(map, info):
        for info in info:
            if info == 'L':
                map.turn_left()
            elif info == 'R':
                map.turn_right()
            elif info == 'l':
                map.turn_slight_left()
            elif info == 'r':
                map.turn_slight_right()
            elif type(info) == int:
                map.move_forward(info)

    def move_forward(map, distance):
        additional_cps = floor((distance-25)/85)+1

        for x in range(additional_cps):
            map.cps.append(((map.lp + map.dir * ((x+0.5) * distance / (additional_cps))).tuple(),
                                      (map.rp + map.dir * ((x+0.5) * distance / (additional_cps))).tuple()))

        map.lp += Point(map.dir.x * distance, map.dir.y * distance)
        map.lps.append(map.lp.tuple())
        map.rp += Point(map.dir.x * distance, map.dir.y * distance)
        map.rps.append(map.rp.tuple())

    def turn_slight_left(map):
        dir = Point(map.dir.y, -map.dir.x)

        map.cps.append(((map.rp + map.dir * 80 + dir * 16).tuple(), (map.lp + map.dir * 0 + dir * 0).tuple()))
        # map.cps.append(((map.rp + map.dir * 148 + dir * 62).tuple(), (map.lp + map.dir * 5 + dir * 5).tuple()))
        
        map.rps.append((map.rp + map.dir * 80 + dir * 16).tuple())
        map.rps.append((map.rp + map.dir * 148 + dir * 62).tuple())
        map.rp += map.dir * 148 + dir * 62

        map.lps.append((map.rp + dir.rotate(-pi/4) * 200).tuple())
        map.lp = map.rp + dir.rotate(-pi/4) * 200

        map.dir = map.dir.rotate(-pi/4)

    def turn_slight_right(map):
        dir = Point(-map.dir.y, map.dir.x)

        map.cps.append(((map.lp + map.dir * 80 + dir * 16).tuple(), (map.rp + map.dir * 0 + dir * 0).tuple()))
        # map.cps.append(((map.rp + map.dir * 148 + dir * 62).tuple(), (map.lp + map.dir * 5 + dir * 5).tuple()))
        
        map.lps.append((map.lp + map.dir * 80 + dir * 16).tuple())
        map.lps.append((map.lp + map.dir * 148 + dir * 62).tuple())
        map.lp += map.dir * 148 + dir * 62

        map.rps.append((map.lp + dir.rotate(pi/4) * 200).tuple())
        map.rp = map.lp + dir.rotate(pi/4) * 200

        map.dir = map.dir.rotate(pi/4)

    def turn_left(map):
        dir = Point(map.dir.y, -map.dir.x)

        map.cps.append(((map.rp + map.dir * 80 + dir * 16).tuple(), (map.lp + map.dir * 0 + dir * 0).tuple()))
        # map.cps.append(((map.rp + map.dir * 148 + dir * 62).tuple(), (map.lp + map.dir * 5 + dir * 5).tuple()))
        map.cps.append(((map.rp + map.dir * 194 + dir * 130).tuple(), (map.lp + map.dir * 10 + dir * 10).tuple()))

        map.rps.append((map.rp + map.dir * 80 + dir * 16).tuple())
        map.rps.append((map.rp + map.dir * 148 + dir * 62).tuple())
        map.rps.append((map.rp + map.dir * 194 + dir * 130).tuple())
        map.rps.append((map.rp + map.dir * 210 + dir * 210).tuple())
        map.rp += map.dir * 210 + dir * 210

        map.lps.append((map.lp + map.dir * 10 + dir * 10).tuple())
        map.lp += map.dir * 10 + dir * 10

        map.dir = dir
        
    def turn_right(map):
        dir = Point(-map.dir.y, map.dir.x)

        map.cps.append(((map.lp + map.dir * 80 + dir * 16).tuple(), (map.rp + map.dir * 0 + dir * 0).tuple()))
        # map.cps.append(((map.lp + map.dir * 148 + dir * 62).tuple(), (map.rp + map.dir * 5 + dir * 5).tuple()))
        map.cps.append(((map.lp + map.dir * 194 + dir * 130).tuple(), (map.rp + map.dir * 10 + dir * 10).tuple()))

        map.lps.append((map.lp + map.dir * 80 + dir * 16).tuple())
        map.lps.append((map.lp + map.dir * 148 + dir * 62).tuple())
        map.lps.append((map.lp + map.dir * 194 + dir * 130).tuple())
        map.lps.append((map.lp + map.dir * 210 + dir * 210).tuple())
        map.lp += map.dir * 210 + dir * 210

        map.rps.append((map.rp + map.dir * 10 + dir * 10).tuple())
        map.rp += map.dir * 10 + dir * 10

        map.dir = dir

class MAP0_info:
    start_pos = Point(230, 580)
    start_angle = 0
    spawn_pos = Point(530, 590)
    spawn_angle = 0
    draw_path = [590, 'L', 10,'R', 130,'L', 10,'L', 370,'L', 10,'R', 10,'R', 10,'L', 120,'L', 240,'L']
    start_cp_index = 5
    clockwise = False

class MAP1_info:
    start_pos = Point(1185, 590)
    start_angle = pi
    spawn_pos = Point(960, 595)
    spawn_angle = pi
    draw_path = [750,'R','L','R',40,'R',250,'R',40,'L',240,'L',40,'R',40,'R',260,'R']
    start_cp_index = 4
    clockwise = True

class MAP2_info:
    start_pos = Point(220, 530)
    start_angle = 0
    spawn_pos = Point(280, 530)
    spawn_angle = 0
    draw_path = [180,'l','R','l',80,'r','L','r',80,'L',200,'L',80,'l',100,'r',100,'r',100,'L',80,'r',118,'L',80,'L']
    start_cp_index = 2
    clockwise = False

class MAP3_info:
    start_pos = Point(1170, 590)
    start_angle = pi
    spawn_pos = Point(1170, 590)
    spawn_angle = pi
    draw_path = [260,'R',50,'L',80,'L',50,'R',40,'r',180,'R',185,'r',450,'r',80,'L','R','r',200,'R']
    start_cp_index = 1
    clockwise = True

MAPS = [NewMap(MAP0_info),
              NewMap(MAP1_info),
              NewMap(MAP2_info),
              NewMap(MAP3_info)]




# import pygame
# from point import Point
# from math import floor, pi

# class NewMap:
#     def __init__(self, x, y, angle):
#         self.road_width = 200
#         self.dir = Point(1,0).rotate(angle)

#         right = Point(-self.dir.y, self.dir.x)

#         self.lp = Point(x, y) - right * (self.road_width/2)
#         self.rp = Point(x, y) + right * (self.road_width/2)

#         self.lps = [self.lp.tuple()]
#         self.rps = [self.rp.tuple()]
#         self.cps = []

#     def move_forward(self, distance):
#         additional_cps = floor((distance-25)/85)+1

#         for x in range(additional_cps):
#             self.cps.append(((self.lp + self.dir * ((x+0.5) * distance / (additional_cps))).tuple(),
#                                       (self.rp + self.dir * ((x+0.5) * distance / (additional_cps))).tuple()))

#         self.lp += Point(self.dir.x * distance, self.dir.y * distance)
#         self.lps.append(self.lp.tuple())
#         self.rp += Point(self.dir.x * distance, self.dir.y * distance)
#         self.rps.append(self.rp.tuple())

#     def turn_slight_left(self):
#         dir = Point(self.dir.y, -self.dir.x)

#         self.cps.append(((self.rp + self.dir * 80 + dir * 16).tuple(), (self.lp + self.dir * 0 + dir * 0).tuple()))
#         # self.cps.append(((self.rp + self.dir * 148 + dir * 62).tuple(), (self.lp + self.dir * 5 + dir * 5).tuple()))
        
#         self.rps.append((self.rp + self.dir * 80 + dir * 16).tuple())
#         self.rps.append((self.rp + self.dir * 148 + dir * 62).tuple())
#         self.rp += self.dir * 148 + dir * 62

#         self.lps.append((self.rp + dir.rotate(-pi/4) * 200).tuple())
#         self.lp = self.rp + dir.rotate(-pi/4) * 200

#         self.dir = self.dir.rotate(-pi/4)

#     def turn_slight_right(self):
#         dir = Point(-self.dir.y, self.dir.x)

#         self.cps.append(((self.lp + self.dir * 80 + dir * 16).tuple(), (self.rp + self.dir * 0 + dir * 0).tuple()))
#         # self.cps.append(((self.rp + self.dir * 148 + dir * 62).tuple(), (self.lp + self.dir * 5 + dir * 5).tuple()))
        
#         self.lps.append((self.lp + self.dir * 80 + dir * 16).tuple())
#         self.lps.append((self.lp + self.dir * 148 + dir * 62).tuple())
#         self.lp += self.dir * 148 + dir * 62

#         self.rps.append((self.lp + dir.rotate(pi/4) * 200).tuple())
#         self.rp = self.lp + dir.rotate(pi/4) * 200

#         self.dir = self.dir.rotate(pi/4)

#     def turn_left(self):
#         dir = Point(self.dir.y, -self.dir.x)

#         self.cps.append(((self.rp + self.dir * 80 + dir * 16).tuple(), (self.lp + self.dir * 0 + dir * 0).tuple()))
#         # self.cps.append(((self.rp + self.dir * 148 + dir * 62).tuple(), (self.lp + self.dir * 5 + dir * 5).tuple()))
#         self.cps.append(((self.rp + self.dir * 194 + dir * 130).tuple(), (self.lp + self.dir * 10 + dir * 10).tuple()))

#         self.rps.append((self.rp + self.dir * 80 + dir * 16).tuple())
#         self.rps.append((self.rp + self.dir * 148 + dir * 62).tuple())
#         self.rps.append((self.rp + self.dir * 194 + dir * 130).tuple())
#         self.rps.append((self.rp + self.dir * 210 + dir * 210).tuple())
#         self.rp += self.dir * 210 + dir * 210

#         self.lps.append((self.lp + self.dir * 10 + dir * 10).tuple())
#         self.lp += self.dir * 10 + dir * 10

#         self.dir = dir
        
#     def turn_right(self):
#         dir = Point(-self.dir.y, self.dir.x)

#         self.cps.append(((self.lp + self.dir * 80 + dir * 16).tuple(), (self.rp + self.dir * 0 + dir * 0).tuple()))
#         # self.cps.append(((self.lp + self.dir * 148 + dir * 62).tuple(), (self.rp + self.dir * 5 + dir * 5).tuple()))
#         self.cps.append(((self.lp + self.dir * 194 + dir * 130).tuple(), (self.rp + self.dir * 10 + dir * 10).tuple()))

#         self.lps.append((self.lp + self.dir * 80 + dir * 16).tuple())
#         self.lps.append((self.lp + self.dir * 148 + dir * 62).tuple())
#         self.lps.append((self.lp + self.dir * 194 + dir * 130).tuple())
#         self.lps.append((self.lp + self.dir * 210 + dir * 210).tuple())
#         self.lp += self.dir * 210 + dir * 210

#         self.rps.append((self.rp + self.dir * 10 + dir * 10).tuple())
#         self.rp += self.dir * 10 + dir * 10

#         self.dir = dir
        
# class MAP0(NewMap):
#     def __init__(self):
#         super().__init__(230, 580, 0)

#         self.spawn_pos = Point(530, 590)
#         self.spawn_angle = 0
        
#         self.data = [590, 'L', 10,'R', 130,'L', 10,'L', 370,'L', 10,'R', 10,'R', 10,'L', 120,'L', 240,'L']
#         self.first_cp = 5

#         self.load()

#     def load(map):
#         for data in map.data:
#             if data == 'L':
#                 map.turn_left()
#             elif data == 'R':
#                 map.turn_right()
#             elif type(data) == int:
#                 map.move_forward(data)
#         map.reset_cp()

#     def draw(self, screen, hitboxes = False):
#         pygame.draw.polygon(screen, (0,0,0), self.rps)
#         pygame.draw.polygon(screen, (0,150,0), self.lps)
#         pygame.draw.lines(screen, (0,100,0), False, self.rps, 5)
#         pygame.draw.lines(screen, (0,100,0), False, self.lps, 5)
#         if hitboxes:
#             pygame.draw.lines(screen, (255,255,0), False, self.rps)
#             pygame.draw.lines(screen, (255,255,0), False, self.lps)
#             for p0, p1 in self.cps:
#                 pygame.draw.line(screen, (255,200,200), p0, p1)
#             pygame.draw.line(screen, (255,0,0), self.cp[0], self.cp[1])

#     def inc_cp(s):
#         s.cp_id = s.cp_id + 1 if s.cp_id < len(s.cps) - 1 else 0
#         s.cp = s.cps[s.cp_id]

#     def reset_cp(s):
#         s.cp_id = s.first_cp
#         s.cp = s.cps[s.cp_id]

# class MAP1(NewMap):
#     def __init__(self):
#         super().__init__(1185, 590, pi)

#         self.spawn_pos = Point(960, 595)
#         self.spawn_angle = pi
        
#         self.data = [750,'R','L','R',40,'R',250,'R',40,'L',240,'L',40,'R',40,'R',260,'R']
#         self.first_cp = 4

#         self.load()

#     def load(map):
#         for data in map.data:
#             if data == 'L':
#                 map.turn_left()
#             elif data == 'R':
#                 map.turn_right()
#             elif type(data) == int:
#                 map.move_forward(data)
#         map.reset_cp()

#     def draw(self, screen, hitboxes = False):
#         pygame.draw.polygon(screen, (0,0,0), self.lps)
#         pygame.draw.polygon(screen, (0,150,0), self.rps)
#         pygame.draw.lines(screen, (0,100,0), False, self.rps, 5)
#         pygame.draw.lines(screen, (0,100,0), False, self.lps, 5)
#         if hitboxes:
#             pygame.draw.lines(screen, (255,255,0), False, self.rps)
#             pygame.draw.lines(screen, (255,255,0), False, self.lps)
#             for p0, p1 in self.cps:
#                 pygame.draw.line(screen, (255,200,200), p0, p1)
#             pygame.draw.line(screen, (255,0,0), self.cp[0], self.cp[1])

#     def inc_cp(s):
#         s.cp_id = s.cp_id + 1 if s.cp_id < len(s.cps) - 1 else 0
#         s.cp = s.cps[s.cp_id]

#     def reset_cp(s):
#         s.cp_id = s.first_cp
#         s.cp = s.cps[s.cp_id]

# class MAP2(NewMap):
#     def __init__(self):
#         super().__init__(220, 530, 0)

#         self.spawn_pos = Point(280, 530)
#         self.spawn_angle = 0
        
#         self.data = [180,'l','R','l',80,'r','L','r',80,'L',200,'L',80,'l',100,'r',100,'r',100,'L',80,'r',118,'L',80,'L']
#         self.first_cp = 2

#         self.load()

#     def load(map):
#         for data in map.data:
#             if data == 'L':
#                 map.turn_left()
#             elif data == 'R':
#                 map.turn_right()
#             elif data == 'l':
#                 map.turn_slight_left()
#             elif data == 'r':
#                 map.turn_slight_right()
#             elif type(data) == int:
#                 map.move_forward(data)
#         map.reset_cp()

#     def draw(self, screen, hitboxes = False):
#         pygame.draw.polygon(screen, (0,0,0), self.rps)
#         pygame.draw.polygon(screen, (0,150,0), self.lps)
#         pygame.draw.lines(screen, (0,100,0), False, self.rps, 5)
#         pygame.draw.lines(screen, (0,100,0), False, self.lps, 5)
#         if hitboxes:
#             pygame.draw.lines(screen, (255,255,0), False, self.rps)
#             pygame.draw.lines(screen, (255,255,0), False, self.lps)
#             for p0, p1 in self.cps:
#                 pygame.draw.line(screen, (255,200,200), p0, p1)
#             pygame.draw.line(screen, (255,0,0), self.cp[0], self.cp[1])

#     def inc_cp(s):
#         s.cp_id = s.cp_id + 1 if s.cp_id < len(s.cps) - 1 else 0
#         s.cp = s.cps[s.cp_id]

#     def reset_cp(s):
#         s.cp_id = s.first_cp
#         s.cp = s.cps[s.cp_id]

# MAPS = [MAP0(),MAP1(),MAP2()]