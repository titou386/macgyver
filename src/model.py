"""MacGyver labyrinth game for OpenClassRooms."""
import random
import os
import platform

from src.constant import MAP_FILE
from src.constant import ITEMS_LIST

from src.constant import UP
from src.constant import DOWN
from src.constant import RIGHT
from src.constant import LEFT


class Position:
    """Parent class for positioning."""

    def __init__(self, name, x, y):
        """Require a name and a position.

        Attributes:
            name (str): name of the object
            x (int): for abscissa representation
            y (int): for ordinate representation
        """
        self.x = x
        self.y = y
        self.name = name

    def move_up(self):
        """Move up, decrease y by 1."""
        if self.y > 0:
            self.y -= 1

    def move_down(self, map_size):
        """Move down, increase y by 1."""
        if self.y < map_size - 1:
            self.y += 1

    def move_left(self):
        """Move left, decrease x by 1."""
        if self.x > 0:
            self.x -= 1

    def move_right(self, map_size):
        """Move right, increase x by 1."""
        if self.x < map_size - 1:
            self.x += 1

    def compare(self, x, y):
        """Comparison test between the object and the position."""
        return(self.x == x and self.y == y)


class Item(Position):
    """Used for alls items on this labyrinth MacGyver needs to pick up."""

    def __init__(self, name, x, y):
        """Same attributes as Position class."""
        super().__init__(name, x, y)


class Road(Position):
    """Used for the road path."""

    def __init__(self, name, x, y):
        """Same attributes as Position class."""
        super().__init__(name, x, y)


class Guardian(Position):
    """Used for the guardian."""

    def __init__(self, name, x, y):
        """Same attributes as Position class."""
        super().__init__(name, x, y)


class Hero(Position):
    """Used for the player MacGyver."""

    def __init__(self, name, x, y):
        """Same attributes as position with a list of collected object."""
        super().__init__(name, x, y)
        self.collected_items = []

    def pick_item(self, item):
        """Add an item on collected itmes list."""
        self.collected_items.append(item)

    def move(self, direction, map_size):
        """Check what direction is asked."""
        if direction == UP:
            self.move_up()
        elif direction == DOWN:
            self.move_down(map_size)
        elif direction == LEFT:
            self.move_left()
        elif direction == RIGHT:
            self.move_right(map_size)
        else:
            raise DirectionInputError()


class DirectionInputError(Exception):
    """Exception raised for errors in the input."""

    def __init__(self):
        """Exception raised for errors in the input."""


class Game:
    """Create each objects and manage them in a play area."""

    def __init__(self):
        """No args required.

        Attributes:
                    hero (Object) Represent the hero object
                    guardian (Object) Represent the guardain object
                    list_items (list of Object)
                    road (list of Object)
        """
        self.hero = None
        self.guardian = None
        self.exit = None
        self.map_size = 0
        self.list_items = []
        self.road = []
        self.load_map()
        self.load_items()

    def is_free(self, x, y):
        """Return True if this object is on an empty space on road list."""
        return(not self.hero.compare(x, y) and
               not self.guardian.compare(x, y) and
               not self.exit.compare(x, y) and
               any([True for r in self.road if r.compare(x, y)]))

    def load_items(self):
        """Create an instance of each item."""
        road = [r for r in self.road if self.is_free(r.x, r.y)]
        free_spaces = random.sample(road, len(ITEMS_LIST))
        for i, item in enumerate(ITEMS_LIST):
            self.list_items.append(
                Item(item, free_spaces[i].x, free_spaces[i].y))

    def load_map(self):
        """Create an instance of each portion of the road."""
        with open(MAP_FILE, "r") as file:
            for i, file_line in enumerate(file):
                if (i + 1) > self.map_size:
                    self.map_size = i + 1
                for j, character in enumerate(file_line):
                    if j > self.map_size:
                        self.map_size = j
                    if character == 'S':
                        self.hero = Hero("MacGyver", j, i)
                        self.road.append(Road("Start", j, i))
                    if character == 'G':
                        self.guardian = Guardian("Guardian", j, i)
                        self.road.append(Road("Road", j, i))
                    if character == 'O':
                        self.road.append(Road("Road", j, i))
                    if character == 'E':
                        self.exit = Road("Exit", j, i)
                        self.road.append(self.exit)

    def check_move(self, direction):
        """Do some checks before and after move the hero."""
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
                self.hero.move(direction, self.map_size)
                self.check_pick_item()
                break

    def check_pick_item(self):
        """Verify if there is a pickable item."""
        for i, obj in enumerate(self.list_items):
            if obj.compare(self.hero.x, self.hero.y):
                self.hero.pick_item(self.list_items.pop(i))


def display_console(game):
    """Display the play area."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    area = []
    line = []

    for i in range(0, game.map_size, 1):
        for i in range(0, game.map_size, 1):
            line.append('#')
        area.append(line)
        line = []

    for obj in game.road:
        if obj.name == "Road":
            area[obj.y][obj.x] = ' '
        else:
            area[obj.y][obj.x] = obj.name[0]

    for obj in game.list_items:
        area[obj.y][obj.x] = obj.name[0]

    area[game.hero.y][game.hero.x] = game.hero.name[0]
    area[game.guardian.y][game.guardian.x] = game.guardian.name[0]

    output_extremity = ''
    for i in range(0, game.map_size + 2, 1):
        output_extremity += '#'
    output_extremity += '\n'

    output = output_extremity

    # Create body
    for line in area:
        output = output + '#' + ''.join(line) + '#' + '\n'
    output += output_extremity
    print(output)
    print("\nMac Gyver possède : ", end='')
    for item in game.hero.collected_items:
        print(item.name, end=' ')
    print()


def main():
    """Main."""
    game = Game()

    loop_continue = True
    while loop_continue:
        display_console(game)
        command = input("Direction ? (q for quit): ")
        try:
            if command == 'q':
                loop_continue = False
            else:
                game.check_move(command)
                if (game.hero.compare(game.guardian.x, game.guardian.y) and
                   len(ITEMS_LIST) != len(game.hero.collected_items)):
                    loop_continue = False
                    display_console(game)
                    print("Vous avez rencontré le gardien sans\
 avoir tout recupéré les objets.")
                if (game.hero.compare(game.exit.x, game.exit.y) and
                   len(ITEMS_LIST) == len(game.hero.collected_items)):
                    loop_continue = False
                    display_console(game)
                    print("Bravo vous avez gagné.")
                print("GAME OVER !")
        except DirectionInputError:
            pass

    if platform.system() == "Windows":
        os.system("pause")
