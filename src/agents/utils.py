import pygame
from pygame.transform import rotate

def rotate_around_center(image, rect, angle):
        """rotate an image while keeping its center"""
        new_image = rotate(image, angle)
        new_rect = new_image.get_rect(center=rect.center)
        return new_image, new_rect
