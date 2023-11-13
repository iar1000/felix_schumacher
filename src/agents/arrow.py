import os
import pygame, math
from pygame.image import load
from pygame.transform import scale

PI = 3.14

#rotate the arrow.
def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect

#Guide the player with a giant arrow.
class Arrow(pygame.sprite.Sprite):

    def __init__(self, x, y, size=100):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = scale(load(os.path.join("src","sprites","pointer.png")), (size, size))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect_orig = self.rect
        self.x = x
        self.y = y
        self.rect.center = self.x, self.y
        self.dir = 0

    #Update the rotation of the arrow.
    def update(self, point, target):
        point_x, point_y = point
        target_x, target_y = target
        self.dir = (math.atan2(point_y - target_y, target_x - point_x) * 180 / PI) - 90
        self.image, self.rect = rot_center(self.image_orig, self.rect_orig, self.dir)
        
    def draw(self, display):
        display.blit(self.image, self.rect)
    
