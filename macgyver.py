import random
import os
from constant import *

class Position:
	def __init__(self, x, y, name):
		self.x = x
		self.y = y
		self.name = name
	
	def move_up(self):
		if self.y > 0:
			self.y -= 1
	
	def move_down(self):
		self.y += 1				# TODO control missing !
		
	def move_left(self):
		if self.x > 0:
			self.x -= 1
	
	def move_right(self):
		self.x +=1				# TODO control missing !

	@property
	def get_position(self):
		return(self.x, self.y)

	@property
	def get_name(self):
		return(self.name)


class Hero(Position):
	def __init__(self, x, y, name):
		super().__init__(x, y, name)
		self.items = []
		
	def move(self, direction):
		if direction == UP:
			self.move_up()
		if direction == DOWN:
			self.move_down()
		if direction == LEFT:
			self.move_left()
		if direction == RIGHT:
			self.move_right()

		
class Items(Position):
	def __init__(self,x, y, name):
		super().__init__(x, y, name)
	


class Zone(Position):
	def __init__(self):
		self.area = []
		self.start = ()
		self.exit = ()

	def load(self):			# loading MAP
		self.area = []
		with open(MAP_FILE, "r") as file: 	
			for i, file_line in enumerate(file):
				line = []
				for j, character in enumerate(file_line):
					if character != "\n":
						line.append(character)
					if character == 'S':
						self.start = (j, i)
					if character == 'E':
						self.exit = (j, i)
				self.area.append(line)		
	@property			
	def get_area(self):
		return self.area
	
	@property
	def get_start_position(self):
		return self.start
	
	def is_free(self, x, y):
		if self.area[y][x] == 'O':
			return True
		else:
			return False
			
	@property
	def get_area_len(self):
		return(len(self.area))


		#display function in the console
def console_display(zone, objects_list):
	os.system("clear")	
	wall = '#'
	zone.load()		#reload the map to erase the changes
	area = zone.get_area

			#place all the instance in the map
	for elt in objects_list:
		area[elt.get_position[1]][elt.get_position[0]] = elt.get_name[0]



	# created the first line and the last line for output
	i = 0
	output_extremity = ''

	while i != (len(area) + 2):
		output_extremity += wall
		i += 1
	output_extremity +='\n'
	
	output = output_extremity
	
	# Create body of the output in output
	for line in area:
		output = output + wall + ''.join(line) + wall + '\n'
	
	output += output_extremity
	
	output = output.replace('O', ' ')
	output = output.replace('X', wall)
	
	print(output)


def find_space(zone):   #find an empty space
	while True:
		x = random.randint(0, (zone.get_area_len - 1))
		y = random.randint(0, (zone.get_area_len - 1))
		if zone.is_free(x, y):
			return (x, y)
		

# main code
zone1 = Zone()
zone1.load()
instance_on_map = []

for i in ITEMS_LIST:   # create instance for each item
	x, y = find_space(zone1)
	instance_on_map.append(Items(x, y, i))

		# create player
macgyver = Hero(zone1.get_start_position[0], \
					zone1.get_start_position[1], "MacGyver")
instance_on_map.append(macgyver)

console_display(zone1, instance_on_map)

	# keystroke loop
loop_continue = True
while loop_continue:
	command = input("Direction ? (q for quit): ")
	if command == 'q':
	  	loop_continue = False
	else :
		macgyver.move(command)
		console_display(zone1, instance_on_map)
	  

