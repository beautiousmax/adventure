__author__ = 'Clara'

"""
This is Adventure. It is a text based adventure full of adventures.
"""

import random
from collections import Counter


class Map(object):
    def __init__(self, location, land, discovered_yet=False):
        self.location = location
        self.land = land
        self.discovered_yet = discovered_yet

#makes a list of a weighted, randomly selected, list of stuff.
#to be used for inventory items.
#maybe even for mobs
#or adventure stuff

results = {'super rare': 100,
           'rare': 50,
           'uncommon': 25,
           'common': 5,
           'super common': 2}

dropper = lambda rareness: random.randint(0, results[rareness]) == 1


class Forest(object):
    def __init__(self, mobs, description, items, name="forest"):
        self.name = name
        self.mobs = mobs
        self.items = items
        self.description = description

forest_description = ["laced with dark magic",
                      "the home of the Tin Woodsman",
                      "filled with happy woodland animals",
                      "covered in shadow"]
forest_mobs = {"old witch": "rare",
               "wolves": "uncommon",
               "squirrels": "common",
               "wood nymphs": "super rare"}


class Farmland(object):
    def __init__(self, mobs, description, items, name="farmland"):
        self.name = name
        self.mobs = mobs
        self.items = items
        self.description = description

farmland_description = ["just barren fields",
                        "rows and rows of beans and squash",
                        "protected from evil by an ancient spell"]
farmland_mobs = {"cows": "common",
                 "farmer": "rare"}


class Mountains(object):
    def __init__(self, mobs, description, name="mountains"):
        self.mobs = mobs
        self.description = description
        self.name = name

mountains_description = ["a very high place",
                         "lots of cliffs and stuff",
                         "home to Tim the Enchanter"]


def drops(set):
    """ Gives each item a few chances to drop, makes a list of dropped items.
    """
    countdown = random.randint(0, 10)
    drops_i = []
    while countdown > 0:
        for k, x in set.items():
            if dropper(x) is True:
                drops_i.append(k)
        countdown -= 1
        return drops_i

#For super awesome chests or loot drops, set countdown to 50 and only include rare or super rare.


#for now, all the things are in one dict.
#To accommodate slicing for the weird things that would appear only in special map types,
#I will make separate dictionaries and just zip them together when I want them all together.
#At least, that's the plan for now.
#Same goes for mobs.
master_items = {"rock": "super common",
                "stick": "common",
                "pinecone": "super common",
                "hunting knife": "uncommon",
                "emerald necklace": "super rare",
                "red lamborghini": "super rare",
                "pixie dust": "rare",
                "broken glass": "uncommon",
                "shovel": "uncommon",
                "mushrooms": "uncommon"}

master_mobs = {"are squirrels": "common",
               "an old witch": "rare",
               "a pack of wolves": "uncommon",
               "some wood nymphs": "super rare"}


def commands(words):
    """ Command handler.
    Anything needing more than one line of code gets its own function.
    """
    if words.lower() == "help":
        print "Available commands are 'look around', 'go north', 'go east', 'go south', and 'go west'"

    if words.lower().startswith("go"):
        change_direction(words.split("go "[-1]))

    if words.lower() == "look around":
        look_around()

    if words.lower() == "inventory":
        print Counter(inventory)

    if words.lower()[0:5] == "throw":
        throw(words[6:])


def look_around():
    """ Tells player a description of current square.
    Sets square to 'discovered', and neighbor squares to seen in the distance.
    For the time being, puts all items into inventory.
    """
    global first_glance
    if current.land.name != "mountains":
        if len(str(current.land.items)) > 0:
            print "This place is %s. Items you found are: " % current.land.description
            print current.land.items
            for i in current.land.items:
                inventory.append(i)
            if first_glance == False:
                print "Time to learn new commands! 'inventory' will tell you what you are carrying." \
                      "You can throw items by using the 'throw [item]' command."
                first_glance = True
        else:
            print "This place is %s. There is nothing here." % current.land.description
    else:
        print "This place is %s. There is nothing here." % current.land.description
    current.discovered_yet = True
    #need a way to not have the stuff be picked up again on a second pass over


def change_direction(direction):
    """ Changes the square to be one square over in the desired direction after checking to see if is on the map
    and if it wouldn't be wrapping the edges pac man style
    """
    global map_squares
    global current
    dir_shift = {"north": -100, "south": 100, "east": 1, "west": -1}
    new_loc = (int(current.location) + int(dir_shift[direction]))
    if new_loc < 0 or new_loc > 10000:
        print "Can't go further %s!" % direction
    elif direction == "east" and new_loc % 100 == 0:
        print "Can't go further east!"
    elif direction == "west" and int(current.location) % 100 == 0:
        print "Can't go further west!"
    else:
        current = map_squares[new_loc]
        print "You are now in %s." % current.land.name
        meet_monster(current.land.mobs)


mob_size = 0
chase_crew = []


#this sucks: the monsters sneak up on you (or not) super predictably, always upon arrival.
#try putting this on a random timer of some kind, rather than movement triggered?
#or randomly every 5 - 9 commands or so.
def meet_monster(mob):
    """ Determine if a mob is hostile or not.
    Decide how many there are.
    """
    global mob_size
    global chase_crew
    hungry = random.randint(0, 5)
    mob_size = random.randint(1, 5)
    if hungry == 1:
        chase_crew.append(mob * mob_size)
        print "%s %s have caught your scent and are about to attack!" % (mob_size, mob)
    else:
        print "%s %s are nearby, peacefully singing and dancing together." % (mob_size, mob)
#gotta make the hostile mobs chase you! otherwise, where's the fun?
#no health for mobs per se, because, let's face it: squirrels and old witches both have the same amount of defence.

throwing_accuracy = 0


def throw(thing):
    """ Player chooses item in inventory, throws it.
    The throw removes the item from inventory.
    There is the chance of it landing back into the area's item cache, so the player may pick it up again for re-use.
    Each throw makes accuracy better, for potential hits on aggressive mobs.
    """
    global inventory
    global throwing_accuracy
    global mob_size
    if thing in inventory:
        inventory.remove(thing)
        if current.land.name != "mountains":
            if random.randint(0, 10) == 1:
                current.land.items.append(thing)
        print "You tossed out a %s!" % thing
        if random.randint(0, 50) <= throwing_accuracy:
            print "You hit one!"
            mob_size -= 1
        throwing_accuracy += 1
    else:
        print "Your throwing is rotten. Nothing happened."
#specify which mob you killed perhaps.

#tackle next: reusable weapons. You don't want to 'throw' your really rare bow, for example.
#mobs cause damage - you should kill them or scare them off.
#player death - always a good goal
#ways to regen health.
#player needs to win the game eventually. Add in the magic castle that is locked.

inventory = []
first_glance = False


def start_game():
    """ Places player in the center of the map.
    Gives help for command options.
    """
    global current
    global health
    current = map_squares[5555]
    health = 100
    commands("help")
    print "You are in %s." % current.land.name


land_type = [Forest(drops(forest_mobs), random.choice(forest_description), drops(master_items)),
             Farmland(random.choice(farmland_mobs.keys()), random.choice(farmland_description), drops(master_items)),
             Mountains(random.choice(master_mobs.keys()), random.choice(mountains_description))]

map_squares = {}


def map_generator():
    """ Makes a grid 100 x 100. Each square is assigned a land type - forest, farmland, mountains, etc.
    """
    global map_squares
    rows = 100
    columns = 100
    name_guy = 0
    while rows > 0:
        while columns > 0:
            map_squares[name_guy] = Map(str(name_guy), (random.choice(land_type)))
            columns -= 1
            name_guy += 1
        rows -= 1
        columns = 100


map_generator()
start_game()
if __name__ == "__main__":
    while health > 0:
        commands(raw_input())