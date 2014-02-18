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

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Character(GameElement):
    IMAGE = "Princess"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

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

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class BlueGem(Gem):
    IMAGE = "BlueGem"

    # def interact(self, player):
    #     pass

class GreenGem(Gem):
    IMAGE = "GreenGem"

class OrangeGem(Gem):
    IMAGE = "OrangeGem"

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
    def interact(self, player):
        GAME_BOARD.draw_msg("This is a person!")

class Prince(NPC):
    IMAGE = "Boy"
    def interact(self, player):
        GAME_BOARD.draw_msg("This is the text you see when you win!")

class Bystander(NPC):
    IMAGE = "Horns"
    def interact(self, player):
        # here put the interaction for giving the Bystander stuff for the key
        pass

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class Door(GameElement):
    pass

class OpenDoor(Door):
    IMAGE = "DoorOpen"
    SOLID = False

class ClosedDoor(Door):
    IMAGE = "DoorClosed"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    def interact(self, player):
        # TODO: Add the key to the inventory. Print something to the screen.
        pass


####   End class definitions    ####

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

def initialize():
    """Put game initialization code here"""
    wall_position = [(4, 0), (4, 1), (4, 2), (6, 2)]
    walls = []
    for pos in wall_position:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        walls.append(wall)
    
    door =  ClosedDoor()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(5, 2, door)

    prince = Prince()
    GAME_BOARD.register(prince)
    GAME_BOARD.set_el(6, 0, prince)

    tree_position = [(3,1), (2, 3), (3, 4), (5, 5)]
    trees = []
    for pos in tree_position:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree)

    rock_positions = [(2, 1), (1, 2), (3, 2)]
    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    # rocks[-1].SOLID = False

    global PLAYER # global???
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    # GAME_BOARD.draw_msg("This game is wicked awesome!")

    # gem_pos = [(3, 1), (4, 0), (1, 4)]
    # gems = []
    # for pos in gem_pos:
    #     gem = Gem()
    #     GAME_BOARD.register(gem)
    #     GAME_BOARD.set_el(pos[0], pos[1], gem)
    #     gems.append(gem)

    # tree = Tree()
    # GAME_BOARD.register(tree)
    # GAME_BOARD.set_el(4,4, tree)

    # chest = Chest()
    # GAME_BOARD.register(chest)
    # GAME_BOARD.set_el(5, 4, chest)

