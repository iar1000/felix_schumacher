
import pygame
from agents.alcoholism import Alcoholism
from agents.arrow import Arrow
from agents.felix import Felix
from camera import Camera
from map import Map


SCREEN_W = 2000
SCREEN_H = 1000
FPS = 60

TILE_SIZE=100
SPRITE_SIZE=120
FELIX_SIZE = 80
ARROW_SIZE = 100

map_path = "src/sprites/maps/map_small.png"


pygame.init()

display = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption('Felix Schumacher')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
pygame.display.update()

# create agents
felix = Felix(SCREEN_W/2, SCREEN_H/2, 
              x_gobal=1000, y_global=1000, 
              size=FELIX_SIZE)
map = Map(felix, display,
          SCREEN_W, SCREEN_H, 
          map_path=map_path,
          tile_size=TILE_SIZE, sprite_size=SPRITE_SIZE)
felix.set_map(map=map)
pointer = Arrow(SCREEN_W/2, SCREEN_H/2 + 350, size=ARROW_SIZE)
gamestate = Alcoholism(map, felix)

# main loop
running = True
while running:
    for event in pygame.event.get():
            # exit game
            if event.type == pygame.QUIT:
                running = False

    # handle input
    felix.update(pygame.key.get_pressed())
    pointer.update(felix.get_pos(), gamestate.get_beer_pos())
    gamestate.update()
    map.draw(display)
    pointer.draw(display)
    gamestate.draw(display)
    felix.draw(display)
    pygame.display.update()

    clock.tick(FPS)

    #print("update:")
    #print(f"\tfps: {clock.get_fps()}")
    #print(f"\tpos: {felix.get_pos()}")
