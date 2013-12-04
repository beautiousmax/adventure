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

    def discovery(self):
        #For purposes of 'looking at a map' and seeing where you have traveled to
        #with a vague idea of what's in the neighboring places
        self.discovered_yet = True
        self.saw_in_the_distance = False


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


def change_direction(direction):
    dir_shift = {"north": -10, "south": 10, "east": 1, "west": -1}
    new_loc = (current.location + dir_shift[direction])
    for place in map_squares:
        if place.location == new_loc:
            return place
    print "Can't go further %s! \n" % direction
    return current


#functionality of this will need to be expanded some
def find_neighbors():
    n = int(current.location) - 10
    e = int(current.location) + 1
    s = int(current.location) + 10
    w = int(current.location) - 1
    neighbors = [
        (n, "north"),
        (e, "east"),
        (s, "south"),
        (w, "west")]
    not_on_map = []
    on_map = []

    for i in neighbors:
        if i[0] in grid:
            on_map.append(i)
        elif i not in grid:
            not_on_map.append("nothing further %s" % i[1])

#DOESN'T WORK. editing the list it is looking at, bad idea.
    for i in on_map:
        for square in map_squares:
            if i == square.location:
                if square.discovered_yet is False:
                    square.saw_in_the_distance = True

    print ', '.join(not_on_map)


def commands(words):
    global current

    if words.lower() == "help":
        print "Available commands are 'look around', 'go north', 'go east', 'go south', and 'go west'"

    if words.lower() == "go north":
        current = change_direction("north")

    if words.lower() == "go east":
        current = change_direction("east")

    if words.lower() == "go south":
        current = change_direction("south")

    if words.lower() == "go west":
        current = change_direction("west")

    if words.lower() == "look around":
        print "This place is %s." % current.land.description

    print "You are at %s, which is %s. \n" % (current.location, current.land.name)
    current.discovery()
    find_neighbors()


def start_game():
    global current
    #place player
    current = map_squares[4]
    current.discovery()
    find_neighbors()
    commands("help")

#generate map
grid = [00, 01, 02, 10, 11, 12, 20, 21, 22]
#grid to be generated by function, eventually. Maybe with individual arrays for each row?? crazy talk
#I am thinking *HUGE grids, 1000 + squares
#will want a way to create mountain chains across different parts of the map
#*relatively huge

land_type = [Forest(drops(master_mobs), random.choice(forest_description), drops(master_items)),
             Farmland(drops(master_mobs), random.choice(farmland_description), drops(master_items)),
             Mountains(drops(master_mobs), random.choice(mountains_description))]

#Not to be limited to forest and farmland:
#castles, small towns, swamps, mountains, the like

map_squares = []

for loc in grid:
    map_squares.append(Map(loc, (random.choice(land_type))))

start_game()
if __name__ == "__main__":
    while True:
        commands(raw_input("What would you like to do? \n"))