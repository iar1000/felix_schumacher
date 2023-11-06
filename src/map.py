import os
import random
import time
from cv2 import transpose
import numpy as np
import pygame
from pygame.sprite import Sprite
from pygame.transform import rotate, scale
from pygame.image import load
from PIL import Image

from agents.felix import Felix

def color_to_tilespec(rgb: list) -> [str, str, str]:
    basepath = os.path.join("src", "sprites")
    
    # houses
    if rgb == [255, 100, 255] or rgb == [0, 0, 0]:
        base = None
        house = None
        if rgb == [255, 100, 255]:
            base = os.path.join(basepath, "tiles", "tile_gras.png")
        if rgb == [0, 0, 0]:
            base = os.path.join(basepath, "tiles", "tile_concrete.png")
        
        c = random.randint(0, 2)
        if c == 0:
            house = os.path.join(basepath, "houses", "house.png")
        if c == 1:
            house = os.path.join(basepath, "houses", "house_3.png")
        if c == 2:
            house = os.path.join(basepath, "houses", "house_2.png")
        if c == 3:
            house = os.path.join(basepath, "houses", "house_big.png")
        return base , house, "house"

    if rgb == [100, 100, 100]:
        return os.path.join(basepath, "tiles", "tile_concrete.png"), None, "road"

    if rgb == [255, 255, 0]:
        return os.path.join(basepath, "tiles", "tile_gras.png"), None, "gras"

    # trees
    if 155 <= rgb[1] <= 255 and rgb[0] == rgb[2] == 0:
        pr = rgb[1] - 155
        r = random.randint(0, 100)
        c = random.randint(0, 3)
        tree = None
        base = os.path.join(basepath, "tiles", "tile_gras.png")
        if pr > r:
            if c == 0:
                tree = os.path.join(basepath, "trees", "tree_apple.png")
            if c == 1:
                tree = os.path.join(basepath, "trees", "tree_tall.png")
            if c == 2 or c == 3:
                tree = os.path.join(basepath, "trees", "tree_normal.png")
        else:
            r = random.random()
            if r < 0.15:
                tree = os.path.join(basepath, "trees", "tree_normal.png")
            if r < 0.25:
                tree = os.path.join(basepath, "trees", "tree_tall.png")
            if c == 0 or c == 3:
                tree = os.path.join(basepath, "trees", "tree_autumn.png")
            if c == 1:
                tree = os.path.join(basepath, "trees", "tree_yellow.png")
            if c == 2:
                tree = os.path.join(basepath, "trees", "tree_naked.png")
            
        return base, tree, "tree"


    print(rgb)


class Map():

    def __init__(self, felix: Felix, display,
                 display_w: int, display_h: int,
                 map_path: str, 
                 tile_size = 50, sprite_size = 150) -> None:
        self.felix = felix
        self.display = display
        self.display_w, self.display_h = display_w, display_h
        self.offset_w, self.offset_h = display_w/2, display_h/2
        self.tile_size = tile_size
        self.sprite_size = sprite_size
        self.tiles, self.num_tiles_x, self.num_tiles_y = self._image_to_tile_matrix(image_path=map_path)
        print(f"tile matrix controll shape= {len(self.tiles[0])}x{len(self.tiles)}")

    def _image_to_tile_matrix(self, image_path: str):
        """reads in an image and turns color values into tiles"""
        image = Image.open(image_path).convert("RGB").transpose(5)
        height, width = image.size
        tile_matrix = [[None for _ in range(width)] for _ in range(height)]
        pixel_matrix = np.array(image)
        print(f"read map file {image_path}: ({width}x{height})")
        print(f"array shape= {pixel_matrix.shape}")
        print(f"tile matrix shape= {len(tile_matrix[0])}x{len(tile_matrix)}")
        
        total_tiles = height * width
        laoding_bar_offset = 200
        loading_bar_size = self.display_w - 2 * laoding_bar_offset
        for y in range(height):
            for x in range(width):
                background_path, sprite_path, tile_type = color_to_tilespec(pixel_matrix[x][y].tolist())
                tile_matrix[y][x] = Tile(self.tile_size * x, self.tile_size * y, 
                                            background_path=background_path, sprite_path=sprite_path, tile_type=tile_type,
                                            tile_size=self.tile_size, sprite_size=self.sprite_size)
            pygame.draw.rect(self.display, (255,0,0), pygame.Rect(laoding_bar_offset, self.offset_h, (y*width + x) / total_tiles * loading_bar_size, 50))
            if (y*width + x) / total_tiles * loading_bar_size > 65:
                font = pygame.font.SysFont("Courier", 36)
                prct = font.render(f"{int((y*width + x) / total_tiles * 100)}%", True, (255, 255, 255))
                prct_rect = prct.get_rect()
                prct_rect.topleft = ((y*width + x) / total_tiles * loading_bar_size + laoding_bar_offset - 65, self.offset_h + 5)
                self.display.blit(prct, prct_rect)
            pygame.display.update()
        
        return tile_matrix, width, height
    
    def check_collision(self, x, y) -> bool:
        x_centered, y_centered = x - self.offset_w, y - self.offset_h # add offset to make the position appear in the middle of the screen

        min_i = max(0, int((x_centered - self.tile_size) / self.tile_size))
        max_i = min(self.num_tiles_x, int((x_centered + self.display_w) / self.tile_size) + 1)
        min_j = max(0, int((y_centered - self.tile_size) / self.tile_size))
        max_j = min(self.num_tiles_y, int((y_centered + self.display_h) / self.tile_size) + 1)
        
        # detect for collision
        collides = False
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                t = self.tiles[j][i]
                if t.has_sprite:
                    t_x, t_y = self.tile_size * i, self.tile_size * j
                    rel_x, rel_y = t_x - x_centered, t_y - y_centered  
                    sprite_im, sprite_rect = t.get_sprite()
                    sprite_rect.topleft = rel_x, rel_y
                    if self.felix.collision_box.colliderect(sprite_rect):
                        collides = True
        
        return collides

    def draw(self, display):
        x_global, y_global = self.felix.get_pos() # get global position of the camera
        x_centered, y_centered = x_global - self.offset_w, y_global - self.offset_h # add offset to make the position appear in the middle of the screen

        min_i = max(0, int((x_centered - self.tile_size) / self.tile_size))
        max_i = min(self.num_tiles_x, int((x_centered + self.display_w) / self.tile_size) + 1)
        min_j = max(0, int((y_centered - self.tile_size) / self.tile_size))
        max_j = min(self.num_tiles_y, int((y_centered + self.display_h) / self.tile_size) + 1)

        # draw background
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                t_x, t_y = self.tile_size * i, self.tile_size * j
                rel_x, rel_y = t_x - x_centered, t_y - y_centered       
                
                t = self.tiles[j][i]
                bg_im, bg_rect = t.get_background()
                bg_rect.topleft = rel_x, rel_y
                display.blit(bg_im, bg_rect)

        # draw sprites
        for i in range(min_i, max_i):
            for j in range(min_j, max_j):
                t_x, t_y = self.tile_size * i, self.tile_size * j
                rel_x, rel_y = t_x - x_centered, t_y - y_centered       
                
                t = self.tiles[j][i]
                if t.has_sprite:
                    sprite_im, sprite_rect = t.get_sprite()
                    sprite_rect.topleft = rel_x, rel_y
                    display.blit(sprite_im, sprite_rect)
                        

class Tile(Sprite):
    def __init__(self, x_global, y_global, 
                 background_path: str, sprite_path: str, tile_type: str,
                 tile_size = 100, sprite_size = 100):
        Sprite.__init__(self)
        self.x = x_global
        self.y = y_global
        self.tile_type = tile_type
        self.is_visible = False

        self.bg = scale(load(background_path).convert(), (tile_size, tile_size))
        self.bg_rect = self.bg.get_rect()
        
        self.has_sprite = sprite_path is not None
        if self.has_sprite:
            self.sprite = scale(load(sprite_path), (sprite_size, sprite_size))
            self.sprite_rect = self.sprite.get_rect()

    def get_background(self):
        return self.bg, self.bg_rect
    
    def get_sprite(self):
        return self.sprite, self.sprite_rect
    
 