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
        self.inventory = {"BlueGem": 0, "GreenGem": 0, "OrangeGem": 0, "Key": 0}

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
        player.inventory["BlueGem"] += 1
        GAME_BOARD.draw_msg("You just acquired a blue gem! Press i to see your inventory.")

class GreenGem(Gem):
    IMAGE = "GreenGem"

    def interact(self, player):
        player.inventory["GreenGem"] += 1
        GAME_BOARD.draw_msg("You just acquired a green gem! Press i to see your inventory.")

class OrangeGem(Gem):
    IMAGE = "OrangeGem"

    def interact(self, player):
        player.inventory["OrangeGem"] += 1
        GAME_BOARD.draw_msg("You just acquired a orange gem! Press i to see your inventory.")


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
        missing_gems = []
        if player.inventory['BlueGem'] >= 1 and player.inventory['OrangeGem'] >= 1 and player.inventory['GreenGem'] >= 1:
            player.inventory['BlueGem'] -= 1
            player.inventory['OrangeGem'] -= 1
            player.inventory['GreenGem'] -= 1
            GAME_BOARD.draw_msg("You got all 3 gems! Here's a key.")
            player.inventory['Key'] = 1

        if player.inventory['BlueGem'] == 0:
            missing_gems.append('blue')
        if player.inventory['GreenGem'] == 0:
            missing_gems.append('green')
        if player.inventory['OrangeGem'] == 0:
            missing_gems.append('orange')

        if len(missing_gems) == 3:
            GAME_BOARD.draw_msg("I'll give you a key in exchange for a gem of each color!")
        elif missing_gems != []:
            missing_gems_string = "You still need to get: "
            for gem in missing_gems:
                missing_gems_string += " " + gem
            missing_gems_string += " gems."
            GAME_BOARD.draw_msg(missing_gems_string)
    
        # if player.inventory == []:
        #     
        # elif len(player.inventory):
        #     # Actually give them a key. Take the gems.
        #     # Replacing inventory with an inventory that contains a key. 
        #     # TODO: Remove the gems and add a key.
        #     player.inventory = [key]
        # else:
        #     GAME_BOARD.draw_msg("You don't have 3 gems yet.")
        # # here put the interaction for giving the Bystander stuff for the key
        # pass

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
    if KEYBOARD[key.I]:
        inventory_string = "You have: "
        for item, number in PLAYER.inventory.iteritems():
            inventory_string += "%d %s " % (number, item)

        GAME_BOARD.draw_msg(inventory_string)

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

    rock_positions = [(2, 1), (1, 4), (3, 2)]
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

    bgem = BlueGem()
    GAME_BOARD.register(bgem)
    GAME_BOARD.set_el(1, 6, bgem)

    ogem = OrangeGem()
    GAME_BOARD.register(ogem)
    GAME_BOARD.set_el(6, 5, ogem)

    ggem = GreenGem()
    GAME_BOARD.register(ggem)
    GAME_BOARD.set_el(3, 0, ggem)

    bystander = Bystander()
    GAME_BOARD.register(bystander)
    GAME_BOARD.set_el(0, 0, bystander)

    GAME_BOARD.draw_msg("You need to save Prince Apricot from the castle!")

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

