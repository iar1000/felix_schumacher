
import os
import pygame
import argparse
from map import Map
from agents.alcoholism import Alcoholism
from agents.arrow import Arrow
from agents.felix import Felix


SCREEN_W = 1100
SCREEN_H = 800
FPS = 60

TILE_SIZE = 100
SPRITE_SIZE = 120
TREE_VAR = 0.15
HOUSE_VAR = 0.08
FELIX_SIZE = 80
ARROW_SIZE = 100
BEER_SIZE = 150

FELIX_MAX_SPEED = 25

FELIX_START_X = 10000
FELIX_START_Y = 10000
MAP_PATH = os.path.join("src", "sprites", "maps", "map_1.png")

def run():
    print("===========================")
    print("==== FELIX SCHUMACHER =====")
    print("===========================")
    print("starting the game...")
    print("\twindow size:", SCREEN_W, SCREEN_H)
    print("\tmap: ", MAP_PATH)
    pygame.init()

    display = pygame.display.set_mode((SCREEN_W,SCREEN_H))

    pygame.display.set_caption('Felix Schumacher')
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    pygame.display.update()

    font = pygame.font.SysFont("Courier", 180)
    text_felix = font.render(f"FELIX", True, (255, 255, 255))
    text_felix_rect = text_felix.get_rect()
    text_felix_rect.center = (SCREEN_W/2, SCREEN_H/2 - SCREEN_H/4)
    display.blit(text_felix, text_felix_rect)
    text_schumi = font.render(f"SCHUMACHER", True, (255, 255, 255))
    text_schumi_rect = text_schumi.get_rect()
    text_schumi_rect.center = (SCREEN_W/2, SCREEN_H/2 + SCREEN_H/4)
    display.blit(text_schumi, text_schumi_rect)


    # create agents
    felix = Felix(SCREEN_W/2, SCREEN_H/2, 
                x_gobal=FELIX_START_X, y_global=FELIX_START_Y, 
                size=FELIX_SIZE,
                max_speed=FELIX_MAX_SPEED)
    map = Map(felix, display,
            SCREEN_W, SCREEN_H, 
            map_path=MAP_PATH,
            tile_size=TILE_SIZE, sprite_size=SPRITE_SIZE,
            sprite_size_variance_tree=TREE_VAR,
            sprite_size_variance_house=HOUSE_VAR)
    felix.set_map(map=map)
    pointer = Arrow(SCREEN_W/2, 7 * SCREEN_H/8, size=ARROW_SIZE)
    gamestate = Alcoholism(map, felix, size=BEER_SIZE)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="change width of window (in pixels)", type=int)
    parser.add_argument("--height", help="change height of window (in pixels)", type=int)
    parser.add_argument("--small", action="store_true", help="play on small map (reduced loading time)")
    parser.add_argument("--funny", action="store_true", help="play in funny mode (very hard)")
    args = parser.parse_args()

    if args.width:
        SCREEN_W = args.width
    if args.height:
        SCREEN_H = args.height

    if args.small:
        FELIX_START_X = 5000
        FELIX_START_Y = 5000
        MAP_PATH = os.path.join("src", "sprites", "maps", "map_2.png")

    if args.funny:
        TREE_VAR = 0.5
        HOUSE_VAR = 0.3
        ARROW_SIZE = 250
        FELIX_SIZE = 40
        FELIX_MAX_SPEED = 40
        BEER_SIZE = 250


    run()

