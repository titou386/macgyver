import random
import os
import platform

from constant import MAP_FILE
from constant import MAP_SIZE
from constant import ITEMS_LIST

from constant import UP
from constant import DOWN
from constant import RIGHT
from constant import LEFT


class Position:
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name

    def move_up(self):
        if self.y > 0:
            self.y -= 1

    def move_down(self):
        if self.y < MAP_SIZE - 1:
            self.y += 1

    def move_left(self):
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        if self.x < MAP_SIZE - 1:
            self.x += 1

    def compare(self, x, y):
        return self.x == x and self.y == y

    def is_free(self, road):
        return[self.compare(r.x, r.y) and
               r.name != "MacGyver" and
               r.name != "Guardian" and
               r.name != "Start" for r in road]


class Object(Position):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)


class Hero(Position):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.collected_items = []
        self.dead = False

    def pick_item(self, item):
        self.items.append(item.name)

    def move(self, direction):
        if direction == UP:
            self.move_up()
        if direction == DOWN:
            self.move_down()
        if direction == LEFT:
            self.move_left()
        if direction == RIGHT:
            self.move_right()


class Game:
    def __init__(self):
        self.hero = None
        self.guardian = None
        self.list_items = []
        self.road = []
        self.load_map()
        self.load_items()

    def load_items(self):
        road = [r for r in self.road if r.is_free(self.road)]
        free_spaces = random.sample(road, len(ITEMS_LIST))
        for i, item in enumerate(ITEMS_LIST):
            self.list_items.append(
                Object(item, free_spaces[i].x, free_spaces[i].y))

    def load_map(self):
        with open(MAP_FILE, "r") as file:
            for i, file_line in enumerate(file):
                for j, character in enumerate(file_line):
                    if character == 'S':
                        self.road.append(Object("Start", j, i))
                        self.hero = Hero("MacGyver", j, i)
                    if character == 'E':
                        self.guardian = Object("Guardian", j, i)
                        self.road.append(self.guardian)
                    if character == 'O':
                        self.road.append(Object("Road", j, i))
        self.road.append(self.hero)

    def pre_move(self, direction):
        x = 0
        y = 0
        if direction == UP:
            y = -1
        if direction == DOWN:
            y = 1
        if direction == LEFT:
            x = -1
        if direction == RIGHT:
            x = 1
        for obj in self.road:
            if obj.compare(self.hero.x + x, self.hero.y + y):
                self.hero.move(direction)
                if self.is_item():
                    self.pick_item()
                break

    def is_item(self):
        for obj in self.list_items:
            if obj.compare(self.hero.x, self.hero.y):
                return True
        return False

    def pick_item(self):
        for i, obj in enumerate(self.list_items):
            if obj.compare(self.hero.x, self.hero.y):
                self.hero.collected_items.append(self.list_items.pop(i))


def display_console(game):
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    area = []
    line = []
    i = 0
    j = 0

    while i != (MAP_SIZE):
        while j != (MAP_SIZE):
            line.append('#')
            j += 1
        area.append(line)
        line = []
        j = 0
        i += 1

    for obj in game.road:
        if obj.name == "Road":
            area[obj.y][obj.x] = ' '
        else:
            area[obj.y][obj.x] = obj.name[0]

    for obj in game.list_items:
        area[obj.y][obj.x] = obj.name[0]

    i = 0
    output_extremity = ''
    while i != (MAP_SIZE + 2):
        output_extremity += '#'
        i += 1
    output_extremity += '\n'

    output = output_extremity

    # Create body
    for line in area:
        output = output + '#' + ''.join(line) + '#' + '\n'
    output += output_extremity
    print(output)
    print("\nMac Gyver possède : ", end='')
    for item in level1.hero.collected_items:
        print(item.name, end=' ')
    print()


# Main

level1 = Game()

loop_continue = True
while loop_continue:
    display_console(level1)
    command = input("Direction ? (q for quit): ")
    if command == 'q':
        loop_continue = False
    else:
        level1.pre_move(command)
        if level1.hero.compare(level1.guardian.x, level1.guardian.y):
            if len(ITEMS_LIST) != len(level1.hero.collected_items):
                loop_continue = False
                display_console(level1)
                print("Vous avez rencontré le guardain sans\
 avoir tout recupéré les objets.")
            else:
                loop_continue = False
                display_console(level1)
                print("Bravo vous avez gagné.")
            print("GAME OVER !")
            if platform.system() == "Windows":
                os.system("pause")
