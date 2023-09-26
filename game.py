import pygame
from pygame.locals import *
from controller import Controller
from new_map import MAP1
from car import Car
import point
from math import sqrt
# from network import NeuralNetwork

pygame.init()
FPS = 60

class CarGameAI:
    def __init__(self, w=1400, h=700):

        # 1 # Make Window
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption('Car Game')
        self.clock = pygame.time.Clock()

        # 2 # Make Content
        self.controller = Controller()
        self.map = MAP1()
        # self.bestBrain = NeuralNetwork((11, 7, 3))
        # self.brain = NeuralNetwork((11, 7, 3))
        self.plr = Car(self.map.spawn_pos, self.map.spawn_angle)
        self.hitboxes = False
        self.ray_dists = [0.0] * self.plr.ray_count
        self.ray_pts = [None] * self.plr.ray_count
        self.reset()

    def reset(self):
        # self.brain = NeuralNetwork((11, 7, 3))
        self.score = 0
        self.plr.respawn()
        self.map.reset_cp()

    def play_step(self):

        # 1 # Collect User Input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_h:
                    self.hitboxes = not self.hitboxes
                # self.controller.getKeyEvent(event)

            # if event.type == pygame.KEYUP:      
            #     self.controller.getKeyEvent(event)

        self.controller.getAction(self.brain.feedForward(self.ray_dists))

        # self.controller.update()

        # 2 # Move Player

        if (self.controller.throttle != 0):
            self.plr.rotate(0.04/10 * self.controller.steer)

        self.plr.move(self.controller.throttle*0.4)

        # 3 # Check if Game Over

        game_over = self.car_collision()

        # 4 # Update Ray Data

        if self.plr.collision(self.map.cp[0], self.map.cp[1]):
            self.score += 1
            self.map.inc_cp()

        self.update_rays()

        # Update UI and Clock

        self.draw_game(self.hitboxes)
        self.clock.tick(FPS)

        # Return Game Over and Score

        return game_over, self.score
    
    def draw_game(self, hitboxes = False):
        self.screen.fill((0,150,0))
        self.map.draw(self.screen, hitboxes)

        if hitboxes:
            for p in self.ray_pts:
                pygame.draw.line(self.screen, (0,255,255), self.plr.pos.tuple(), p)

        self.plr.draw(self.screen, hitboxes)
        pygame.display.update()

    def car_collision(self):
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

if __name__ == '__main__':
    game = CarGameAI()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            print('Score:', game.score)
            game.reset()