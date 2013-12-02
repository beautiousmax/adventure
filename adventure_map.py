__author__ = 'Clara'

import random


class Map(object):
    def __init__(self, location, land, discovered_yet=False, saw_in_the_distance=False):
        self.location = location
        self.land = land
        self.discovered_yet = discovered_yet
        self.saw_in_the_distance = saw_in_the_distance

    def discovery(self):
        self.discovered_yet = True
        self.saw_in_the_distance = False
        #set neighboring squares saw_in_the_distance to True if they haven't been discovered yet

#This bit is pure folly.
#Don't look at it, unless with loving care.
#It may be salvageable.
#The idea is to add items that may be pocketed in an inventory to each map square
#as well as cute descriptions of each place on the map (not all farmland was created equal, ya know)

"""
class Items(object):
    def __init__(self, name, rarity, use):
        self.name = name
        #with this, the idea is to somehow say 'yes, make this item accessable, this time around'
        self.rarity = rarity
        self.use = use


#calculate the odds of an item dropping -
def rare_maybe(x):
    if x == "super rare":
        if random.randint(0, 100) == 1:
            return True
        else:
            return False

    if x == "rare":
        if random.randint(0, 50) == 1:
            return True
        else:
            return False

    if x == "uncommon":
        if random.randint(0, 25) == 1:
            return True
        else:
            return False

    if x == "common":
        if random.randint(0, 5) == 1:
            return True
        else:
            return False

    if x == "super common":
        if random.randint(0, 2) == 1:
            return True
        else:
            return False


class Forest(object):
    def __init__(self, mob, description, items, name="forest"):
        self.name = name
        self.mob = mob
        self.description = description
        self.items = items

        mobs_lst = ["are squirrels",
                    "an old witch",
                    "a pack of wolves",
                    "some wood nymphs"]
        self.mob = random.choice(mobs_lst)
        description_lst = ["laced with dark magic",
                           "the home of the Tin Woodsman",
                           "filled with happy woodland animals",
                           "covered in shadow"]
        self.description = random.choice(description_lst)

        items_lst = []
        hidden_items_lst = [Items("rock", rare_maybe("common"), "weapon"),
                            Items("stick", rare_maybe("common"), "weapon"),
                            Items("pinecone", rare_maybe("super common"), "n"),
                            Items("hunting knife", rare_maybe("uncommon"), "weapon"),
                            Items("emerald necklace", rare_maybe("super rare"), "jewelry")]
        for i in hidden_items_lst:
            if i[Items.rarity] is True:
                items_lst.append(i)


class Farmland(object):
    def __init__(self, mob, description, items, name="farmland"):
        self.name = name
        self.mob = mob
        self.description = description
        self.items = items

        mobs_lst = ["a few cows",
                    "a farmer"]
        self.mob = random.choice(mobs_lst)

        description_lst = ["just barren fields",
                           "rows and rows of beans and squash",
                           "protected from evil by an ancient spell"]
        self.description = random.choice(description_lst)

        hidden_items_lst = [Items("broken glass", rare_maybe("uncommon"), "n"),
                            Items("shovel", rare_maybe("uncommon"), "weapon"),
                            Items("mushrooms", rare_maybe("uncommon"), "n")]
        items_lst = []
        for i in hidden_items_lst:
            if i[Items.rarity] is True:
                items_lst.append(i)

"""


def change_direction(direction):
    dir_shift = {"north": -10, "south": 10, "east": 1, "west": -1}
    new_loc = (current.location + dir_shift[direction])
    for place in map_squares:
        if place.location == new_loc:
            return place
    print "Can't go further %s!" % direction
    print
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
        (w, "west")
    ]
    not_on_map = []
    on_map = []

    for i in neighbors:
        if i[0] in grid:
            on_map.append(i)
        elif i not in grid:
            not_on_map.append("nothing further %s" % i[1])

    print ', '.join(not_on_map)


def commands(words):
    global current

    if words.lower() == "help":
        print "Available commands are 'go north', 'go east', 'go south', and 'go west'"
        commands(raw_input("What would you like to do? "))

    if words.lower() == "go north":
        current = change_direction("north")
        print "You now are at %s, which is %s." % (current.location, current.land)
        find_neighbors()

    if words.lower() == "go east":
        current = change_direction("east")
        print "You now are at %s, which is %s." % (current.location, current.land)
        find_neighbors()

    if words.lower() == "go south":
        current = change_direction("south")
        print "You now are at %s, which is %s." % (current.location, current.land)
        find_neighbors()

    if words.lower() == "go west":
        current = change_direction("west")
        print "You now are at %s, which is %s." % (current.location, current.land)
        find_neighbors()
    current.discovery()


def start_game():
    global current
    #place player
    current = map_squares[4]
    current.discovery()
    print "You are at square %s, which is %s." % (current.location, current.land)
    find_neighbors()
    print
    print "Available commands are 'go north', 'go east', 'go south', and 'go west'"
    return current

#generate map
grid = [00, 01, 02, 10, 11, 12, 20, 21, 22]
#grid to be generated by function, eventually. Maybe with individual arrays for each row?? crazy talk

land_type = ["forest", "farmland"]
#to be replaced with classes that have attributes and items in them.. see failures above
#and not to be limited to forest and farmland:
#castles, small towns, swamps, mountains, the like

map_squares = []

for loc in grid:
    map_squares.append(Map(loc, (random.choice(land_type))))

start_game()
if __name__ == "__main__":
    while True:
        print
        commands(raw_input("What would you like to do? "))