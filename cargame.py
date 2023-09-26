import pygame
from pygame.locals import *
from controller import Controller
from map import MAPS
from car import Car
import point
from math import sqrt

pygame.init()
FPS = 240

class CarGameAI:
    def __init__(self, w=1400, h=700):

        # 1 # Window
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption('Car Game')
        self.clock = pygame.time.Clock()

        # 2 # Game Content
        self.controller = Controller()
        self.map_id = 0
        self.map = MAPS[0]
        self.plr = Car(self.map.info.spawn_pos, self.map.info.spawn_angle)
        self.hitboxes = False
        self.ray_dists = [None] * self.plr.ray_count
        self.ray_pts = [None] * self.plr.ray_count

        # 3 # Agent Info
        self.current_score = 0
        self.score = 0
        self.game_over = False
        self.running = True

        # 4 # Init Game
        self.reset()
        self.update_rays()

    def update_score(self):
        self.score = self.current_score if self.map_id == 0 else min(self.score, self.current_score)
        self.current_score = 0

    def load_new_map(self):
        self.map_id += 1
        self.map = MAPS[self.map_id]
        self.plr.respawn(self.map.info.spawn_pos, self.map.info.spawn_angle)
        self.map.reset_cp()
        self.controller.throttle = 0
        self.controller.steer = 0

    def reset(self):
        self.game_over = False
        self.current_score = 0
        self.score = 0
        self.map_id = 0
        self.map = MAPS[self.map_id]
        self.plr.respawn(self.map.info.spawn_pos, self.map.info.spawn_angle)
        self.map.reset_cp()
        self.controller.throttle = 0
        self.controller.steer = 0

    def play_step(self, action):
        # Update Agent Info

        # 1 # Collect User Input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == K_h:
                    self.hitboxes = not self.hitboxes

        # 2 # Move Player

        self.move(action)

        # 3 # Check if Game Over

        if self.is_game_over() or self.current_score >= 1000:
            self.update_score()
            if self.map_id < len(MAPS) - 1:
                self.load_new_map()
            else:
                self.game_over = True

        # 4 # Update Model Input Data

        if self.plr.collision(self.map.cp[0], self.map.cp[1]):
            self.current_score += 1
            self.map.inc_cp()

        self.update_rays()

        # Update UI and Clock

        self.draw_game()
        self.clock.tick(FPS)
    
    def getModelInput(self):
        return self.ray_dists

    def move(self, action):
        self.controller.getAction(action)
        
        if (self.controller.throttle != 0):
            self.plr.rotate(0.04/10 * self.controller.steer)

        self.plr.move(self.controller.throttle*0.4)

    def draw_game(self):
        self.screen.fill((0,150,0))
        self.map.draw(self.screen, self.hitboxes)

        if self.hitboxes:
            for p in self.ray_pts:
                pygame.draw.line(self.screen, (0,255,255), self.plr.pos.tuple(), p)

        self.plr.draw(self.screen, self.hitboxes)
        pygame.display.update()

    def is_game_over(self):
        for x in range(len(self.map.lps)-1):
            if self.plr.collision(self.map.lps[x], self.map.lps[x+1]):
                return True
        for x in range(len(self.map.rps)-1):
            if self.plr.collision(self.map.rps[x], self.map.rps[x+1]):
                return True
        return False

    def update_rays(self):
        for x in range(len(self.plr.rps)):
            closest_point = self.plr.rps[x]
            closest_dist = self.plr.vision_dist
            for y in range(len(self.map.lps)-1):
                col = point.LineCollision(self.plr.pos.tuple(), self.plr.rps[x], self.map.lps[y], self.map.lps[y+1])
                if col != None:
                    dist = sqrt((self.plr.pos.x - col[0])**2 + (self.plr.pos.y - col[1])**2)
                    if dist < closest_dist:
                        closest_point = col
                        closest_dist = dist
            for y in range(len(self.map.rps)-1):
                col = point.LineCollision(self.plr.pos.tuple(), self.plr.rps[x], self.map.rps[y], self.map.rps[y+1])            
                if col != None:
                    dist = sqrt((self.plr.pos.x - col[0])**2 + (self.plr.pos.y - col[1])**2)
                    if dist < closest_dist:
                        closest_point = col
                        closest_dist = dist

            self.ray_pts[x] = closest_point
            self.ray_dists[x] = 1 - closest_dist/self.plr.vision_dist

# if __name__ == '__main__':
#     game = CarGameAI()
    
#     # game loop
#     while True:
#         game_over, score = game.play_step()
        
#         if game_over == True:
#             print('Score:', game.score)
#             game.reset()