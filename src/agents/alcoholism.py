
import os, random
import pygame
from pygame.image import load
from pygame.transform import scale


class Alcoholism(pygame.sprite.Sprite):

    def __init__(self, map, felix, size=200):
        pygame.sprite.Sprite.__init__(self)
        self.map = map
        self.felix = felix
        
        # beer
        self.image = scale(load(os.path.join("src","sprites","beer.png")), (size, size))
        self.image_bed = scale(load(os.path.join("src","sprites","bed.png")), (size, size))
        self.image_health = load(os.path.join("src","sprites","health_bar.png"))
        self.rect = self.image.get_rect()
        self.x, self.y = None, None
        self._position_beer()
        
        # gamestate
        self.max_beers = 10
        self.beers_intus = 9
        self.sleeping = False

        self.font = pygame.font.SysFont("Monaco", 36)        
        self.font_big = pygame.font.SysFont("Monaco", 120)        

        pygame.mixer.music.load(os.path.join("src","music","intro.mp3"))
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(0.2)


    def _position_beer(self):
        x = random.randint(0, self.map.num_tiles_x-1)
        y = random.randint(0, self.map.num_tiles_y-1)
        while not self.map.tile_free(x,y):
            x = random.randint(0, self.map.num_tiles_x-1)
            y = random.randint(0, self.map.num_tiles_y-1)
        self.x, self.y = x * self.map.tile_size, y * self.map.tile_size
        print(f"new beer at {self.x}x{self.y}")
    
    def get_beer_pos(self):
        return (self.x, self.y)
    
    def drink_beer(self):
        self.beers_intus += 1
        if self.beers_intus < self.max_beers:
            self._position_beer()
            pygame.mixer.music.set_volume(max(0.3, self.beers_intus * 0.1))
        else:
            self._position_beer()
            self.image = self.image_bed
            self.rect = self.image.get_rect()
            pygame.mixer.music.load(os.path.join("src","music","song.mp3"))
            pygame.mixer.music.play(-1,0.0)
            pygame.mixer.music.set_volume(1)
            self.felix.make_drunk()

    def update(self):
        # check collision
        if self.felix.collision_box.colliderect(self.rect):
            if not self.felix.is_drunk:
                self.drink_beer()
            else:
                self.sleeping = True

    def draw(self, display):
        x_global, y_global = self.felix.get_pos() 
        self.rect.center = self.x - x_global + self.map.offset_w, self.y - y_global + self.map.offset_h 
        display.blit(self.image, self.rect)

        # render text
        if not self.felix.is_drunk:
            prct = self.font.render(f"time to go home in {self.max_beers - self.beers_intus}", True, (255, 217, 0))
            if self.felix.walking:
                prct = self.font.render(f"you might better just walk home bro...", True, (0, 0, 0))
        else:
            prct = self.font.render(f"your are drunk felix, go home!", True, (0, 0, 0))
        prct_rect = prct.get_rect()
        prct_rect.center = (self.map.offset_w, 200)
        display.blit(prct, prct_rect)

        # render health
        if self.felix.is_drunk:
            pygame.draw.rect(display, (255,0,0), pygame.Rect(self.map.offset_w - 145, 250, int(350 * (self.felix.health / self.felix.health_max)), 100))

            # health bar
            rect = self.image_health.get_rect()
            rect.center = (self.map.offset_w, 300)
            display.blit(self.image_health, rect)

        # render finish
        if self.sleeping:
            prct = self.font_big.render(f"you win", True, (255, 217, 0))
            prct_rect = prct.get_rect()
            prct_rect.center = (self.map.offset_w, self.map.offset_h)
            display.blit(prct, prct_rect)

            prct = self.font.render(f"you made it home save! don't drink and drive!", True, (255, 217, 0))
            prct_rect = prct.get_rect()
            prct_rect.center = (self.map.offset_w, self.map.offset_h + 100)
            display.blit(prct, prct_rect)      
