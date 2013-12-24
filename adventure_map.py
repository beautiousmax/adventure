__author__ = 'Clara'

"""
This is Adventure. It is a text based adventure full of adventures.
"""

import random


class Map(object):
    def __init__(self, location, land, discovered_yet=False, saw_in_the_distance=False):
        self.location = location
        self.land = land
        self.discovered_yet = discovered_yet
        self.saw_in_the_distance = saw_in_the_distance


#makes a list of a weighted, randomly selected, list of awesome stuff.
#to be used for inventory items.
#maybe even for mobs
#or adventure stuff

results = {'super rare': 100,
           'rare': 50,
           'uncommon': 25,
           'common': 5,
           'super common': 2}

dropper = lambda rareness: random.randint(0, results[rareness]) == 1


def drops(lizst):
    #gives each item a few chances to drop
    countdown = random.randint(0, 10)
    drops_i = []
    while countdown > 0:
        for k, x in lizst.items():
            if dropper(x) is True:
                drops_i.append(k)
        countdown -= 1
        return drops_i


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
                "pixie dust": "rare",
                "broken glass": "uncommon",
                "shovel": "uncommon",
                "mushrooms": "uncommon"}

master_mobs = {"are squirrels": "common",
               "an old witch": "rare",
               "a pack of wolves": "uncommon",
               "some wood nymphs": "super rare",

               "a few cows": "common",
               "a farmer": "rare"}


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


class Farmland(object):
    def __init__(self, mobs, description, items, name="farmland"):
        self.name = name
        self.mobs = mobs
        self.items = items
        self.description = description

farmland_description = ["just barren fields",
                        "rows and rows of beans and squash",
                        "protected from evil by an ancient spell"]


class Mountains(object):
    def __init__(self, mobs, description, name="mountains"):
        self.mobs = mobs
        self.description = description
        self.name = name

mountains_description = ["a very high place",
                         "lots of cliffs and stuff",
                         "home to Tim the Enchanter"]


#fix this
def find_the_neighbors():
    pass

#this is going to get out of hand fast.
#commands to be separate functions.
#because, testing
#also, some really intense ones will be added later on
#future commands: dialogue stuff, attacks, localized movement
def commands(words):
    global current

    if words.lower() == "help":
        print "Available commands are 'look around', 'go north', 'go east', 'go south', and 'go west'"

    if words.lower() == "go north":
        change_direction("north")

    if words.lower() == "go east":
        change_direction("east")

    if words.lower() == "go south":
        change_direction("south")

    if words.lower() == "go west":
        change_direction("west")

    if words.lower() == "look around":
        if current.land.name != "mountains":

            if current.discovered_yet is False:
                print "This place is %s. Items you found are: " % current.land.description
                print current.land.items
                for i in current.land.items:
                    inventory.append(i)
                current.discovered_yet = True
            else:
                print "This place is %s. You have already visited here." % current.land.description
        else:
            print "This place is %s. There is nothing here." % current.land.description

    if words.lower() == "inventory":
        print inventory

    #this is really annoying.
    #print "You are at the %s.\n" % (current.land.name,)
    #find_neighbors()


def start_game():
    global current
    #place player
    current = map_squares[1000]
    #find_neighbors()
    commands("help")

inventory = []


land_type = [Forest(drops(master_mobs), random.choice(forest_description), drops(master_items)),
             Farmland(drops(master_mobs), random.choice(farmland_description), drops(master_items)),
             Mountains(drops(master_mobs), random.choice(mountains_description))]


def change_direction(direction):
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
        print "You are now in a %s." % current.land.name

#generate map
#makes a square grid
#who wouldn't want a square map anyways?

rows = 100
columns = 100
name_guy = 0

map_squares = {}

while rows > 0:
    while columns > 0:
        map_squares[name_guy] = Map(str(name_guy), (random.choice(land_type)))
        columns -= 1
        name_guy += 1
    rows -= 1
    columns = 100


start_game()
if __name__ == "__main__":
    while True:
        commands(raw_input())