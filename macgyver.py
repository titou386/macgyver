import random
import os

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

    @property
    def cap_short_name(self):
        return self.name[0].capitalize()

class Road(Position):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

class Items(Position):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

class Guardian(Position):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)


class Hero(Position):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.collected_items = []
        self.dead = False

    def pick_item(self, item):
        self.items.append(item.name)

    def died(self):
        self.dead = True

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

    def is_free(self, x, y):
        return[road.compare(x, y) and not
               self.hero.compare(x, y) and not
               self.guardian.compare(x, y) for road in self.road]

    def load_items(self):
        road = [r for r in self.road if r.is_free(r.x, r.y)]
        free_spaces = random.sample(road, len(ITEMS_LIST))
        for i, item in enumerate(ITEMS_LIST):   # create instance for each item
            self.list_items.append(
                Items(item, free_spaces[i].x, free_spaces[i].y))

    def load_map(self):
        with open(MAP_FILE, "r") as file:   # loading MAP
            for i, file_line in enumerate(file):
                for j, character in enumerate(file_line):
                    if character == 'S':
                        obj = Hero("MacGyver", j, i)
                        self.road.append(obj)
                    if character == 'E':
                        obj = Guardian("Guardian", j, i)
                        self.road.append(obj)
                    if character == 'O':
                        obj = Road("Road", j, i)
                        self.road.append(obj)

def find_space(objects):
    for obj in objects:
        while True:
            x = random.randint(0, (MAP_SIZE - 1))
            y = random.randint(0, (MAP_SIZE - 1))
            if is_free(objects, x, y):
                return(x, y)

def check_move(objects, player, direction):
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
    for obj in objects:
        if player.x + x == obj.x and player.y + y == obj.y \
            and "None" != obj.name \
            and "Start" != obj.name \
                and "Exit" != obj.name:
            return False
    return True

def is_pickable(objects, player):
    for obj in objects:
        if player.x == obj.x and player.y == obj.y :
            for elt in ITEMS_LIST:
                if elt == obj.name:
                    return True
    return False

def is_exit(objects, player):
    for obj in objects:
        if obj.name == "Exit":
            if player.x == obj.x and player.y == obj.y:
                    return True
    return False

def is_guardian(objects, player):
    for obj in objects:
        if obj.name == "Guardian":
            if player.x == obj.x and player.y == obj.y:
                    return True
    return False


def pick_item(objects, player):
    for i, obj in enumerate(objects):
        if player.x == obj.x and player.y == obj.y:
            if player != obj:
                player.pick_item(objects.pop(i))
    

def display_console(size, list_elt_map, list_obj_map):
    os.system("clear")
    area = []
    line = []
    i = 0
    j = 0
        
    while i != (size):
        while j != (size):
            line.append('')
            j += 1
        area.append(line)
        line = []
        j = 0
        i += 1
    
    for obj in list_elt_map:
        if obj.get_name == "Wall":
            rep = '#'
        if obj.get_name == "None":
            rep = ' '
        if 'rep' in locals():
            area[obj.y][obj.x] = rep
            del(rep)
        else:
            area[obj.y][obj.x] = obj.get_short_name # erreur
            
    for obj in list_obj_map:
        area[obj.y][obj.x] = obj.get_short_name
    
    i = 0
    output_extremity = ''
    while i != (size + 2):
        output_extremity += '#'
        i += 1
    output_extremity += '\n'
    
    output = output_extremity
    
    # Create body
    for line in area:
        output = output + '#' + ''.join(line) + '#' + '\n'
    output += output_extremity
    print(output)


# Main

list_elt_map = init_game()
list_obj_map = []


x, y = find_space(list_elt_map)
gardian = Object("Guardian", x, y)
macgyver = Hero("MacGyver", 0, 0)  # TODO find the Object "Start"
list_obj_map.append(gardian)
list_obj_map.append(macgyver)

display_console(MAP_SIZE, list_elt_map, list_obj_map)

loop_continue = True
while loop_continue:
    command = input("Direction ? (q for quit): ")
    if command == 'q':
        loop_continue = False
    else:
        if check_move(list_elt_map, macgyver, command):
            macgyver.move(command)
            if is_pickable(list_obj_map, macgyver):
                pick_item(list_obj_map, macgyver)
            if is_guardian(list_obj_map, macgyver):
                if len(ITEMS_LIST) != len(macgyver.items):
                    macgyver.died()
                    loop_continue = False
            if is_exit(list_elt_map, macgyver) \
                and len(ITEMS_LIST) == len(macgyver.items):
                loop_continue = False
        display_console(MAP_SIZE, list_elt_map, list_obj_map)
        print("MacGyver possède : ", macgyver.items)
        if macgyver.dead:
            print("Vous êtes mort !")
        if not loop_continue and len(ITEMS_LIST) == len(macgyver.items):
            print("Bravo vous avez gagné !")
