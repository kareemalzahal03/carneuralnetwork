import pygame
from math import cos, sin, pi
from point import Point, LineCollision

class Car:
    def __init__(self, spawn_pos, spawn_angle):
        super(Car, self).__init__()
        self.og_surf = pygame.transform.smoothscale(pygame.image.load("car.png").convert(), (104, 54))
        self.surf = self.og_surf
        self.vision_dist = 500
        self.ray_count = 11
        self.rps = [None] * self.ray_count # Ray Points
        self.hbps = [None] * 4 # Hit Box Points
        self.rect = self.surf.get_rect(center=spawn_pos.tuple())
        self.surf.set_alpha(255)

        # self.pos = spawn_pos
        # self.dir = Point(1,0).rotate(spawn_angle)
        # self.angle = spawn_angle

        self.respawn(spawn_pos, spawn_angle)
    
    def draw(self, screen, hitboxes = False):
        screen.blit(self.surf, self.rect)
        if hitboxes:
            pygame.draw.lines(screen,(255,255,0), True, self.hbps)
        
    def rotate(self, angle):
        self.angle += angle
        self.surf = pygame.transform.rotate(self.og_surf, -self.angle*180/pi)
        self.rect = self.surf.get_rect(center=self.rect.center)
        self.dir = Point(cos(self.angle), sin(self.angle))
        self.update_hitbox()

    def move(self, speed):
        self.pos += self.dir * speed
        self.rect.center = [self.pos.x, self.pos.y]
        self.update_hitbox()

    def update_hitbox(s):
        dir_right = Point(-s.dir.y, s.dir.x)

        s.hbps[0] = (s.pos + s.dir * 48 - dir_right * 24).tuple()
        s.hbps[1] = (s.pos + s.dir * 48 + dir_right * 24).tuple()
        s.hbps[2] = (s.pos - s.dir * 48 + dir_right * 24).tuple()
        s.hbps[3] = (s.pos - s.dir * 48 - dir_right * 24).tuple()

        s.rps[0] = (s.pos + s.dir.rotate(-1.5) * s.vision_dist).tuple()
        s.rps[1] = (s.pos + s.dir.rotate(-1.2) * s.vision_dist).tuple()
        s.rps[2] = (s.pos + s.dir.rotate(-0.9) * s.vision_dist).tuple()
        s.rps[3] = (s.pos + s.dir.rotate(-0.6) * s.vision_dist).tuple()
        s.rps[4]= (s.pos + s.dir.rotate(-0.3) * s.vision_dist).tuple()
        s.rps[5] = (s.pos + s.dir.rotate(0) * s.vision_dist).tuple()
        s.rps[6] = (s.pos + s.dir.rotate(0.3) * s.vision_dist).tuple()
        s.rps[7]= (s.pos + s.dir.rotate(0.6) * s.vision_dist).tuple()
        s.rps[8] = (s.pos + s.dir.rotate(0.9) * s.vision_dist).tuple()
        s.rps[9]= (s.pos + s.dir.rotate(1.2) * s.vision_dist).tuple()
        s.rps[10]= (s.pos + s.dir.rotate(1.5) * s.vision_dist).tuple()

    def respawn(self, pos, angle):
        self.dir = Point(1,0).rotate(angle)
        self.pos = pos
        self.angle = angle
        self.rotate(0)

    def collision(self, p0, p1):
        return (LineCollision(self.hbps[0], self.hbps[1], p0, p1) != None
                or LineCollision(self.hbps[1], self.hbps[2], p0, p1) != None
                or LineCollision(self.hbps[2], self.hbps[3], p0, p1) != None
                or LineCollision(self.hbps[3], self.hbps[0], p0, p1) != None)
