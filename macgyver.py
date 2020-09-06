"""MacGyver labyrinth game for OpenClassRooms."""
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

    def move_down(self):
        """Move down, increase y by 1."""
        if self.y < MAP_SIZE - 1:
            self.y += 1

    def move_left(self):
        """Move left, decrease x by 1."""
        if self.x > 0:
            self.x -= 1

    def move_right(self):
        """Move right, increase x by 1."""
        if self.x < MAP_SIZE - 1:
            self.x += 1

    def compare(self, x, y):
        """Comparison test between the object and the position."""
        return self.x == x and self.y == y

    def is_free(self, road):
        """Return True if this object is on an empty space on road list."""
        return[self.compare(r.x, r.y) and
               r.name != "MacGyver" and
               r.name != "Guardian" and
               r.name != "Start" for r in road]


class Object(Position):
    """Used for all objects on this labyrinth except MacGyver."""

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
        self.collected_items.append(item.name)

    def move(self, direction):
        """Check what direction is asked."""
        if direction == UP:
            self.move_up()
        elif direction == DOWN:
            self.move_down()
        elif direction == LEFT:
            self.move_left()
        elif direction == RIGHT:
            self.move_right()
        else:
            raise DirectionInputError(direction, "n'est pas reconnu")


class DirectionInputError(Exception):
    """Exception raised for errors in the input."""

    def __init__(self, expression, message):
        """Arg : expression from the input and error message."""
        self.expression = expression
        self.message = message
        self.error()
        self.help()

    def error(self):
        """Print the error message."""
        print(self.expression, self.message)
        print()

    def help(self):
        """Print the help message."""
        print(UP, "pour haut")
        print(DOWN, "pour bas")
        print(LEFT, "pour gauche")
        print(RIGHT, "pour droite")


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
        self.list_items = []
        self.road = []
        self.load_map()
        self.load_items()

    def load_items(self):
        """Create an instance of each item."""
        road = [r for r in self.road if r.is_free(self.road)]
        free_spaces = random.sample(road, len(ITEMS_LIST))
        for i, item in enumerate(ITEMS_LIST):
            self.list_items.append(
                Object(item, free_spaces[i].x, free_spaces[i].y))

    def load_map(self):
        """Create an instance of each portion of the road."""
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
        """Do some checks before move the hero."""
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
                self.pre_pick_item()
                break

    def pre_pick_item(self):
        """Verify if there is a pickable item."""
        for i, obj in enumerate(self.list_items):
            if obj.compare(self.hero.x, self.hero.y):
                self.pick_item(self.list_items.pop(i))


def display_console(game):
    """Display the play area."""
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
    try:
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
    except DirectionInputError as e:
        input("Appuyer une touche pour continuer ...")
