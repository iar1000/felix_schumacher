
import pygame
from agents.felix import Felix
from camera import Camera
from map import Map


SCREEN_W = 2000
SCREEN_H = 1000
FPS = 60

TILE_SIZE=80
SPRITE_SIZE=100
FELIX_SIZE = 80

map_path = "src/sprites/maps/map_0.png"


pygame.init()

display = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption('Felix Schumacher')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
pygame.display.update()


felix = Felix(SCREEN_W/2, SCREEN_H/2, 
              x_gobal=19900, y_global=11000, 
              size=FELIX_SIZE)
map = Map(felix, SCREEN_W, SCREEN_H, 
          map_path=map_path,
          tile_size=TILE_SIZE, sprite_size=SPRITE_SIZE)
felix.set_map(map=map)

running = True
while running:
    for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT:
                running = False

    # handle input
    felix.update(pygame.key.get_pressed())
    map.draw(display)
    felix.draw(display)
    pygame.display.update()

    clock.tick(FPS)

    print("update:")
    print(f"\tfps: {clock.get_fps()}")
    print(f"\tpos: {felix.get_pos()}")
