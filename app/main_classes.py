import random
from app.common_functions import comma_separated, add_dicts_together
from data.text import items, buildings, wild_mobs
from reusables.string_manipulation import int_to_words


class Item(object):
    def __init__(self, name, quantity, plural, category=None, perishable=None,
                 flammable=None, rarity=None, price=None):
        self.name = name
        self.quantity = quantity
        self.plural = plural
        self.category = category or None
        self.perishable = perishable or None
        self.flammable = flammable or None
        self.rarity = rarity or None
        self.price = price or None

    def copy(self):
        return Item(name=self.name, quantity=self.quantity, plural=self.plural, category=self.category,
                    perishable=self.perishable, flammable=self.flammable, rarity=self.rarity)


class Building(object):
    def __init__(self, name, quantity, plural, category=None, rarity=None, wares=None, mobs=None, jobs=None):
        self.name = name
        self.quantity = quantity
        self.plural = plural
        self.category = category or None
        self.rarity = rarity or None
        self.wares = drops(wares, Item) if wares else None
        self.mobs = drops(mobs, Mob) if mobs else None
        self.jobs = jobs


class Mob(object):
    def __init__(self, name, plural, quantity, rarity):
        self.name = name
        self.plural = plural
        self.quantity = quantity
        self.rarity = rarity

    skills = {}
    health = 100
    # TODO add conversation flows, job interviews, quests

    # quests
    # bring me 100 of super common object to learn patience
    # bring me a super rare object to learn patience
    # bring me 10 uncommon object to earn 20 dollars

    # say hello to 50 mobs to learn communication


class Player(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.money = 0

    building_local = None
    inventory = []
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
                    formatted.append(f"{int_to_words(self.money)} dollars")

            elif item.quantity > 1:
                formatted.append(f"{int_to_words(item.quantity)} {item.plural}")
            else:
                formatted.append(item.name)
        if formatted != []:
            return comma_separated(formatted)
        else:
            return "nothing"

    def status(self):
        print(f"Currently, you have {self.health}% health. \nYou are located on map coordinates "
              f"{self.location}, which is {the_map[self.location].square_type}.")
        if p.building_local:
            print(f"You are inside {p.building_local}.")

        if self.skills:
            for k, v in self.skills.items():
                if v >= 100:
                    print(f"You have mastered {k}.")
                else:
                    print(f"You have learned {v}% of {k}.")
        else:
            print("You don't have any skills.")

        print(f"You have {self.formatted_inventory()} in your inventory.")

        if self.job:
            print(f"You have a job as a {self.job}.")
        else:
            print("You do not have a job, and you are not contributing to society.")


class MapSquare(object):
    def __init__(self, name=""):
        self.name = name
    square_type = ''
    mobs = []
    items = []
    buildings = []

    def new(self):
        square_types = ["forest", "mountains", "desert", "city", "swamp", "ocean"]
        self.square_type = square_types[random.randint(0, len(square_types) - 1)]
        return self

    def generate_items(self):
        self.items = drops(add_dicts_together(items["master"], items[self.square_type]), Item)

    def generate_buildings(self):
        self.buildings = drops(add_dicts_together(buildings["master"], buildings[self.square_type]), Building)

    def generate_mobs(self):
        self.mobs = drops(add_dicts_together(wild_mobs["master"], wild_mobs[self.square_type]), Mob)


def drops(dictionary, object_in_question):
    drops_i = []

    results = {'super rare': 100,
               'rare': 50,
               'uncommon': 25,
               'common': 5,
               'super common': 2}

    d = dictionary

    for k, v in d.items():
        quantity = 0
        countdown = random.randint(0, 10)
        while countdown > 0:
            if random.randint(0, results[v["rarity"]]) == 1:
                quantity += 1
            countdown -= 1
        if quantity:
            drops_i.append(object_in_question(name=k, quantity=quantity, **v))

    return drops_i


the_map = {(0, 0): MapSquare(name="spawn").new()}
the_map[(0, 0)].generate_items()
the_map[(0, 0)].generate_buildings()
the_map[(0, 0)].generate_mobs()

p = Player(name='', location=(0, 0))