import pygame, time, sys
import macgyver
from constant import ITEMS_LIST
from constant import IMG_PATH
from constant import ITEMS_IMG

from constant import UP
from constant import DOWN
from constant import RIGHT
from constant import LEFT

size = width, height = 300, 300
elt_size = elt_width, elt_height = 20, 20



def init_xgame(game):
    pygame.init()

    screen = pygame.display.set_mode((300, 320))

    tiles = pygame.image.load(IMG_PATH + "floor-tiles-20x20.png")
    guardian = pygame.image.load(IMG_PATH + "Gardien.png")
    guardian = pygame.transform.scale(guardian, elt_size)

    wall = pygame.Surface(elt_size)
    road = pygame.Surface(elt_size)
    start = pygame.Surface(elt_size)

    background = pygame.Surface(size)

    wall.blit(tiles, (0, 0), (300, 0, 20, 20))
    road.blit(tiles, (0, 0), (0, 240, 20, 20))
    start.blit(tiles, (0, 0), (160, 20, 20, 20))

    for y in range(0, height, elt_height):
        for x in range(0, width, elt_width):
            background.blit(wall, (x, y))
            for obj in game.road:
                if obj.x == (x / elt_width) and obj.y == (y / elt_height):
                    if obj.name == "Road":
                        background.blit(road, (x, y))
                    elif obj.name == "Start":
                        background.blit(start, (x, y))
                    elif obj.name == "Guardian":
                        background.blit(guardian, (x, y))

    return screen, background

game = macgyver.Game()
screen, background = init_xgame(game)
small_font = pygame.font.SysFont("Comic Sans MS", 25)
hero_have = small_font.render("MacGyver possède :", False, (255, 255, 255))

big_font = pygame.font.SysFont("Comic Sans MS", 60)
big_font.set_bold(True)
game_over = big_font.render("GAME OVER !", False, (255, 0, 0), (0, 0, 0))

py_img = {}
py_img[game.hero.name] = pygame.image.load(IMG_PATH + "MacGyver.png")
py_img[game.hero.name] = pygame.transform.scale(
    py_img[game.hero.name], elt_size)
for i, item in enumerate(ITEMS_LIST):
    py_img[ITEMS_LIST[i]] = pygame.image.load(IMG_PATH + ITEMS_IMG[i])
    py_img[ITEMS_LIST[i]] = pygame.transform.scale(
        py_img[ITEMS_LIST[i]], elt_size)

loop_continue = True
while loop_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.pre_move(LEFT)
            if event.key == pygame.K_RIGHT:
                game.pre_move(RIGHT)
            if event.key == pygame.K_UP:
                game.pre_move(UP)
            if event.key == pygame.K_DOWN:
                game.pre_move(DOWN)
            if event.key == pygame.K_q:
                sys.exit()
    if game.hero.compare(game.guardian.x, game.guardian.y):
        if len(ITEMS_LIST) != len(game.hero.collected_items):
            loop_continue = False
            end_mesg = "Vous avez perdu !!!"
        else:
            loop_continue = False
            end_mesg = "Vous avez gagné !!!"

    screen.blit(background, (0, 0))

    screen.blit(py_img[game.hero.name], (
        game.hero.x * elt_width, game.hero.y * elt_height))

    for item in game.list_items:
        screen.blit(py_img[item.name],
                    (item.x * elt_width, item.y * elt_height))

    screen.blit(hero_have, (0, 300))
    for i, item in enumerate(game.hero.collected_items):
        screen.blit(py_img[item.name],
                    (i * elt_width + 180, 300))
    pygame.display.flip()

screen.blit(game_over, (0, 140))
mesg = small_font.render(end_mesg, False, (255, 0, 0), (0, 0, 0))
screen.blit(mesg, (60, 200))
pygame.display.flip()

time.sleep(10)
