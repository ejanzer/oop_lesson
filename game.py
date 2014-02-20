import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 7
GAME_HEIGHT = 7

IMAGE_KEYS = {
    's': 'Block', 
    'B': 'BlueGem', 
    'P': 'Boy', 
    'a': 'Cat', 
    'x': 'Chest', 
    'D': 'DoorClosed', 
    'd': 'DoorOpen', 
    'l': 'Girl', 
    'g': 'GrassBlock', 
    'G': 'GreenGem', 
    'h': 'Heart', 
    'H': 'Horns', 
    'K': 'Key', 
    'O': 'OrangeGem', 
    'C': 'Princess', 
    'S': 'Rock', 
    'b': 'ShortTree', 
    'n': 'StoneBlock', 
    'W': 'StoneBlockTall', 
    'T': 'TallTree', 
    'y': 'Wall', 
    'z': 'Water',
    '#': None,
    'N': 'Barrier'
}


#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = {"Blue Gem": 0, "Green Gem": 0, "Orange Gem": 0, "Key": 0}
        self.level_complete = False
        self.level_at = 1

    def next_pos(self, direction):
        if direction == 'up':
            return (self.x, self.y - 1)
        elif direction == 'down':
            return(self.x, self.y + 1)
        elif direction == 'left':
            return (self.x-1, self.y)
        elif direction == 'right':
            return (self.x + 1, self.y)
        return None

class Gem(GameElement):
    SOLID = False

class BlueGem(Gem):
    IMAGE = "BlueGem"

    def interact(self, player):
        player.inventory["Blue Gem"] += 1
        GAME_BOARD.draw_msg("You just acquired a blue gem! Press i to see your inventory.")

class GreenGem(Gem):
    IMAGE = "GreenGem"

    def interact(self, player):
        player.inventory["Green Gem"] += 1
        GAME_BOARD.draw_msg("You just acquired a green gem! Press i to see your inventory.")

class OrangeGem(Gem):
    IMAGE = "OrangeGem"

    def interact(self, player):
        player.inventory["Orange Gem"] += 1
        GAME_BOARD.draw_msg("You just acquired an orange gem! Press i to see your inventory.")


class Heart(GameElement):
    IMAGE = "Heart"
    SOLID = False
    def interact(self, player):
        # Add to inventory
        pass

class Tree(GameElement):
    IMAGE = "TallTree"
    SOLID = True

class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):
        pass

class NPC(GameElement):
    SOLID = True
    def __init__(self):
        self.met = False
    def interact(self, player):
        GAME_BOARD.draw_msg("This is a person!")
        self.met = True

class Prince(NPC):
    IMAGE = "Boy"
    def interact(self, player):
        GAME_BOARD.draw_msg("Oh no! This is an impostor prince! Your prince is in another castle.\nPress SPACE to continue.")
        player.level_complete = True

class Bystander(NPC):
    IMAGE = "Horns"
    def interact(self, player):
        if self.met:
            missing_gems = []
            if player.inventory['Key'] == 0:    
                
                if player.inventory['Blue Gem'] == 0:
                    missing_gems.append('blue')
                if player.inventory['Green Gem'] == 0:
                    missing_gems.append('green')
                if player.inventory['Orange Gem'] == 0:
                    missing_gems.append('orange')

                if missing_gems == []:
                    player.inventory['Blue Gem'] -= 1
                    player.inventory['Orange Gem'] -= 1
                    player.inventory['Green Gem'] -= 1
                    GAME_BOARD.draw_msg("You got all 3 gems! Here's a key.")
                    player.inventory['Key'] = 1
                elif len(missing_gems) == 3:
                    GAME_BOARD.draw_msg("I'll give you a key in exchange for a gem of each color!")
                elif len(missing_gems) == 2:
                    missing_gems_string = "You still need to get a %s gem and a %s gem." % (missing_gems[0], missing_gems[1])
                    GAME_BOARD.draw_msg(missing_gems_string)
                elif len(missing_gems) == 1:
                    missing_gems_string = "You still need to get a %s gem." % (missing_gems[0])
                    GAME_BOARD.draw_msg(missing_gems_string)
            else:
                GAME_BOARD.draw_msg("You need to go save Prince Pineapple!")
        else:
            GAME_BOARD.draw_msg("I'll give you a key in exchange for a gem of each color!")
            self.met = True


class Wall(GameElement):
    IMAGE = "StoneBlockTall"
    SOLID = True

class Door(GameElement):
    pass

class OpenDoor(Door):
    IMAGE = "DoorOpen"
    SOLID = False

class ClosedDoor(Door):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        if player.inventory['Key'] > 0:
            unlock_door(self.x, self.y)
            # x = self.x
            # y = self.y
            # GAME_BOARD.del_el(self.x, self.y)
            # door = OpenDoor()
            # GAME_BOARD.register(door)
            # GAME_BOARD.set_el(x, y, door)
        else:
            GAME_BOARD.draw_msg("It's locked...")

def unlock_door(x, y):
    GAME_BOARD.del_el(x, y)
    door = OpenDoor()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(x, y, door)
    PLAYER.inventory['Key'] -= 1

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):
        # TODO: Add the key to the inventory. Print something to the screen.
        pass

class Water(GameElement):
    IMAGE = "Water"
    SOLID = True

class Barrier(GameElement):
    IMAGE = 'Blank'
    SOLID = True

CLASS_KEYS = {
    'BlueGem': BlueGem,
    'Boy': Prince,
    'StoneBlockTall': Wall,
    'Princess': Character,
    'Horns': Bystander,
    'GreenGem': GreenGem,
    'OrangeGem': OrangeGem,
    'Heart': Heart,
    'TallTree': Tree,
    'Chest': Chest,
    'Key': Key,
    'DoorClosed': ClosedDoor,
    'DoorOpen': OpenDoor,
    'Rock': Rock,
    'Barrier': Barrier,
}

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    global PLAYER
    PLAYER = Character()

    set_up_level()

def keyboard_handler():
    direction = None
    if KEYBOARD[key.UP]:
        direction = 'up'
    if KEYBOARD[key.LEFT]:
        direction = 'left'
    if KEYBOARD[key.RIGHT]:
        direction = 'right'
    if KEYBOARD[key.DOWN]:
        direction = 'down'
    if KEYBOARD[key.I]:
        blue = PLAYER.inventory['Blue Gem']
        green = PLAYER.inventory['Green Gem']
        orange = PLAYER.inventory['Orange Gem']
        doorkey = PLAYER.inventory['Key']
        inventory_string = "You have %d blue gem, %d orange gem, %d green gem and %d key." % (blue, orange, green, doorkey)

        GAME_BOARD.draw_msg(inventory_string)

    if KEYBOARD[key.SPACE] and PLAYER.level_complete:
        PLAYER.level_complete = False
        PLAYER.level_at += 1
        wipe_board()
        set_up_level()

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]
        if check_pos(next_x, next_y):
            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER) 

def check_pos(x, y):
    if x >= GAME_WIDTH or x < 0:
        return False
    elif y >= GAME_HEIGHT or y < 0:
        return False
    return True

def wipe_board():
    for x in range(0, GAME_WIDTH):
        for y in range(0, GAME_HEIGHT):
            GAME_BOARD.del_el(x, y)

def set_up_level():
    d = {
        1: set_up_one,
        2: set_up_two
    }

    d[PLAYER.level_at]()

def map_setup(map_string):
    lines = map_string.split()
    game_map = []
    for i in range(len(lines)):
        row = []
        for char in lines[i]:
            row.append(IMAGE_KEYS[char])
        game_map.append(row)
    return game_map

def draw_foreground(game_map):
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            if game_map[y][x]:
                object_instance = CLASS_KEYS[game_map[y][x]]()
                GAME_BOARD.register(object_instance)
                GAME_BOARD.set_el(x, y, object_instance)

def set_up_one():

    f = open("level_one.txt")
    layout_data = f.read()
    f.close()
    layout_data = layout_data.split('*')
    background = map_setup(layout_data[0])
    foreground = map_setup(layout_data[1])

    draw_foreground(foreground)
    GAME_BOARD.set_bg_sprites(background)
    GAME_BOARD.draw()

    GAME_BOARD.draw_msg("You need to save Prince Pineapple from the castle!")

    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(6, 3, PLAYER)



def set_up_two():

    f = open("level_two.txt")
    layout_data = f.read()
    f.close()
    layout_data = layout_data.split('*')
    background = map_setup(layout_data[0])
    foreground = map_setup(layout_data[1])

    GAME_BOARD.set_bg_sprites(background)
    GAME_BOARD.draw()

    draw_foreground(foreground)

    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(0, 0, PLAYER)
    GAME_BOARD.draw_msg("You need to save Prince Pineapple from the castle!...again.")