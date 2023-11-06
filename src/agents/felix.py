

import math
import os
import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.image import load
from pygame.transform import scale
from pygame import draw

from agents.utils import rotate_around_center

class Felix(Sprite):
    def __init__(self, x_screen: int, y_screen: int,
                 x_gobal: int, y_global: int,
                 size: int = 100):
        super().__init__()

        self.x_gobal = x_gobal
        self.y_gobal = y_global

        # visual
        self.base_image = scale(load(os.path.join("src","sprites","agent_felix.png")), (size, size))
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.center = (x_screen, y_screen)

        # collision box
        box_size = size/3
        self.collision_box = Rect(x_screen - (box_size / 2), y_screen - (box_size / 2), box_size, box_size)

        # movement
        self.angle = 0
        self.v = 0.0
        self.v_max = 30
        self.v_min = -5
        self.v_steering = 3
        self.a_acceleration = 1
        self.a_break = 2
        self.a_roll = 0.3

        # map
        self.map = None

    def set_map(self, map):
        self.map = map

    def get_pos(self) -> [int, int]:
        """return global position"""
        return self.x_gobal, self.y_gobal

    def gas(self):
        """accelerate felix schumacher"""
        if self.v < self.v_max:
            #print("gas!!!!!")
            self.v = self.v + self.a_acceleration
            if self.v < self.v_max / 3:
                self.emit_tracks()

    def brake(self):
        """break felix schumacher"""
        if self.v > 0:
            #print("brake...")
            self.v = max(0, self.v - self.a_break)
            self.emit_tracks() 

    def roll(self):
        """natural deacceleration if not on gas, nor break"""
        if self.v > 0:
            self.v = max(0, self.v - self.a_roll)
            self.emit_tracks() 
        if self.v < 0:
            self.v = max(self.v_min, self.v + self.a_roll)


    def steer(self, left: bool = False):
        """rotate felix"""
        steering = self.v_steering if left else -self.v_steering
        self.angle += steering
        self.angle %= 360
        if (self.v > self.v_max / 2):
            self.emit_tracks()

    def collision(self):
        if self.v <= 0:
            self.v = -self.v_min / 4
        elif self.v < -self.v_min:
            self.v = -self.v
        else:
            self.v = self.v_min
  

    def emit_tracks(self):
        pass

    def update(self, pressed_keys):
        # update velocity
        if pressed_keys[pygame.K_DOWN]:
            self.brake()
        elif pressed_keys[pygame.K_UP]:
            self.gas()
        else:
            self.roll()

        # update angle
        if pressed_keys[pygame.K_LEFT]:
            self.steer(left=True)
        if pressed_keys[pygame.K_RIGHT]:
            self.steer(left=False)

        # update position
        x_curr = self.x_gobal
        y_curr = self.y_gobal
        self.x_gobal += self.v * math.cos(math.radians(270-self.angle))
        self.y_gobal += self.v * math.sin(math.radians(270-self.angle))
        
        # check for collision, reset to non-collision and change velocity as reaction
        if self.map.check_collision(self.x_gobal, self.y_gobal):
            self.x_gobal = x_curr
            self.y_gobal = y_curr
            # change v to opposite direction
            self.collision() 

        # update rotation
        self.image, self.rect = rotate_around_center(self.base_image, self.rect, self.angle)

        


    def draw(self, display):
        display.blit(self.image, self.rect)
        draw.rect(display, "red", self.collision_box)

 