import pygame
import numpy as np

MAX = 10
MIN = -10
INC = 0.5

class Controller:

    def __init__(self):
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = True
        self.down_pressed = False
        self.steer = 0
        self.throttle = 0

    def update(self):
        if (self.left_pressed == self.right_pressed):
            if self.steer != 0:
                self.steer += INC if self.steer <= 0 else -INC
        elif (self.left_pressed and self.steer > MIN):
            self.steer -= INC
        elif (self.right_pressed and self.steer < MAX):
            self.steer += INC

        if (self.down_pressed == self.up_pressed):
            if self.throttle != 0:
                self.throttle += INC if self.throttle <= 0 else -INC
        elif (self.down_pressed and self.throttle > MIN):
            self.throttle -= INC
        elif (self.up_pressed and self.throttle < MAX):
            self.throttle += INC

    def getKeyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.left_pressed = True
            elif event.key == pygame.K_RIGHT:
                self.right_pressed = True
            elif event.key == pygame.K_UP:
                self.up_pressed = True
            elif event.key == pygame.K_DOWN:
                self.down_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_pressed = False
            elif event.key == pygame.K_RIGHT:
                self.right_pressed = False
            elif event.key == pygame.K_UP:
                self.up_pressed = False
            elif event.key == pygame.K_DOWN:
                self.down_pressed = False
        
    def getAction(self, action):
        # # [left, straight, right]
        # if np.array_equal(action, [1, 0, 0]):
        #     self.left_pressed = True
        #     self.right_pressed = False
        # elif np.array_equal(action, [0, 1, 0]):
        #     self.left_pressed = False
        #     self.right_pressed = False
        # else: # [0, 0, 1]
        #     self.left_pressed = False
        #     self.right_pressed = True

        self.left_pressed = action[0] == True
        self.right_pressed = action[1] == True
        
        self.update()