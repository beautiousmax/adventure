"""
This is Adventure. It is a text based adventure full of adventures.
"""
import random
from common_functions import comma_separated, add_dicts_together
from text import items
from reusables.numbers import int_to_words


class Item(object):
    def __init__(self, name, quantity, plural, type=None, perishable=None,
                 flammable=None, rarity=None, wares=None, jobs=None, mobs=None):
        self.name = name
        self.quantity = quantity
        self.plural = plural
        self.type = type or None
        self.perishable = perishable or None
        self.flammable = flammable or None
        self.rarity = rarity or None
        self.wares = wares or None
        self.jobs = jobs or None
        self.mobs = mobs or None

    def copy(self):
        return Item(name=self.name, quantity=self.quantity, plural=self.plural, type=self.type, perishable=self.perishable,
                    flammable=self.flammable, rarity=self.rarity, wares=self.wares, jobs=self.jobs, mobs=self.mobs)


class Building(object):
    def __init__(self, name):
        self.name = name

    def job_openings(self):
        job_openings = {}
        for k, v in items[the_map[p.location].square_type][self.name]["jobs"].items():
            job_openings[k] = {"hired": random.randint(0, 100), "open": random.randint(0, 5)}

        return job_openings

    def interactions(self):
        interactions = ["barter goods", "leave building", "apply for a job"]
        if self.name in ("bar", "starbucks", "convenience store", "a car dealership", "a food mart"):
            interactions.append("purchase items")

        return interactions


class Mob(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location

    skills = {}
    health = 100


class Player(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location

    building_local = None
    inventory = [Item(name="money", quantity=0, plural="money")]
    skills = {}
    job = {}
    health = 100

    def formatted_inventory(self):
        formatted = []
        for item in self.inventory:

            if item.name == "money":
                if item.quantity == 0:
                    formatted.append("no cash")
                else:
                    formatted.append("{} dollars".format(int_to_words(item.quantity)))

            elif item.quantity > 1:
                formatted.append("{} {}".format(int_to_words(item.quantity), item.plural))
            else:
                formatted.append(item.name)
        return formatted

    def status(self):
        print("Currently, you have {}% health. \nYou are located on map "
              "coordinates {}, which is {}.".format(self.health, self.location, the_map[self.location].square_type))

        if self.skills:
            for k, v in self.skills.items():
                if v >= 100:
                    print("You have mastered {}.".format(k))
                else:
                    print("You have learned {}% of {}.".format(v, k))
        else:
            print("You don't have any skills.")

        print("You have {} in your inventory.".format(comma_separated(self.formatted_inventory())))

        if self.job:
            print("You have a job as a {}.".format(self.job))
        else:
            print("You do not have a job, and you are not contributing to society.")


class MapSquare(object):
    def __init__(self, name=""):
        self.name = name
    square_type = ''
    mobs = {}
    items = []
    buildings = []

    def new(self):
        square_types = ["forest", "mountains", "desert", "city", "swamp", "ocean"]
        self.square_type = square_types[random.randint(0, len(square_types) - 1)]
        return self

    def generate_items(self):
        self.items = drops(add_dicts_together(items["master"], items[self.square_type]),
                           anything_buts=("building", "residence"))

    def generate_buildings(self):
        self.buildings = drops(add_dicts_together(items["master"], items[self.square_type]),
                               specific_types=("building", "residence"))


def drops(dictionary, specific_types=None, anything_buts=None):
    drops_i = []
    d = {}

    results = {'super rare': 100,
               'rare': 50,
               'uncommon': 25,
               'common': 5,
               'super common': 2}

    if specific_types or anything_buts:
        if specific_types and anything_buts is None:
            d = {k: v for (k, v) in dictionary.items() if "type" in v and v["type"] in specific_types}
        elif anything_buts and specific_types is None:
            d = {k: v for (k, v) in dictionary.items() if "type" in v and v["type"] not in anything_buts or "type" not in v}
    else:
        d = dictionary

    for k, v in d.items():
        quantity = 0
        countdown = random.randint(0, 10)
        while countdown > 0:
            if random.randint(0, results[v["rarity"]]) == 1:
                quantity += 1
            countdown -= 1
        if quantity:
            drops_i.append(Item(name=k, quantity=quantity, **v))

    return drops_i


the_map = {(0, 0): MapSquare(name="spawn").new()}
the_map[(0, 0)].generate_items()
the_map[(0, 0)].generate_buildings()

p = Player(name='', location=(0, 0))
