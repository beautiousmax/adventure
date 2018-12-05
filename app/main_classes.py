import random

import colorama
from reusables.string_manipulation import int_to_words

from app.common_functions import comma_separated, add_dicts_together, remove_little_words, odds
from data.text import items, buildings, wild_mobs, names, adjectives


colorama.init()


def find_a_name(name_list):
    n = name_list[random.randint(0, len(name_list)-1)]
    if len(the_map[p.location].unique_names) <= len(names) + len(adjectives):
        if n not in the_map[p.location].unique_names:
            the_map[p.location].unique_names.append(n)
            return n
        else:
            return find_a_name(name_list)
    else:
        the_map[p.location].unique_names = []
        return find_a_name(name_list)


def drops(dictionary, object_in_question):
    """ Randomly generates objects based on rarity """
    drops_i = []

    results = {'super rare': 100,
               'rare': 50,
               'uncommon': 25,
               'common': 5,
               'super common': 2}

    for k, v in dictionary.items():
        quantity = 0
        countdown = random.randint(0, 10)
        while countdown > 0:
            if random.randint(0, results[v["rarity"]]) == 1:
                quantity += 1
            countdown -= 1
        if quantity:
            if object_in_question == Item:
                drops_i.append(object_in_question(name=k, quantity=quantity, **v))
            elif object_in_question == Mob:
                if quantity > 1:
                    for m in range(0, quantity):
                        drops_i.append(Mob(name=f"{k} named {find_a_name(names)}", **v))
                else:
                    drops_i.append(Mob(name=k, **v))
            elif object_in_question == Building:
                if quantity > 1 and v['category'] != 'residence':
                    for m in range(0, quantity):
                        if odds(2):
                            drops_i.append(Building(name=f"The {find_a_name(adjectives)} "
                                                         f"{remove_little_words(k).capitalize()}", **v))
                        else:
                            drops_i.append(Building(name=f"{find_a_name(names)}'s "
                                                         f"{remove_little_words(k).capitalize()}", **v))
                elif quantity > 1 and v['category'] == 'residence':
                    for m in range(0, quantity):
                        drops_i.append(Building(name=f"{find_a_name(names)}'s {remove_little_words(k)}", **v))
                else:
                    drops_i.append(Building(name=k, **v))

    return drops_i


class MapSquare(object):
    def __init__(self, name=""):
        square_types = ["forest", "mountains", "desert", "city", "swamp", "ocean"]
        self.square_type = square_types[random.randint(0, len(square_types) - 1)]
        self.name = name
        self.unique_names = []

    mobs = []
    items = []
    buildings = []

    def generate_items(self):
        self.items = drops(add_dicts_together(items["master"], items[self.square_type]), Item)

    def generate_buildings(self):
        self.buildings = drops(add_dicts_together(buildings["master"], buildings[self.square_type]), Building)

    def generate_mobs(self):
        self.mobs = drops(add_dicts_together(wild_mobs["master"], wild_mobs[self.square_type]), Mob)

    def clean_up_map(self):
        """ Remove items with quantity of zero from the map inventory"""
        self.items = [i for i in self.items if i.quantity != 0]


the_map = {(0, 0): MapSquare(name="spawn")}


class Player(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.money = 0
        self.quest = None
        self.job = None
        self.phase = "day"

    equipped_weapon = None
    building_local = None
    inventory = []
    skills = {}
    health = 100

    def phase_change(self):
        self.phase = 'day' if self.phase == 'night' else 'night'
        for k, square in the_map.items():
            square.generate_items()
            for b in square.buildings:
                if b.ware_list:
                    b.wares = drops(b.ware_list, Item)

    def formatted_inventory(self):
        formatted = []
        for item in self.inventory:

            if item.quantity > 1:
                formatted.append(f"{int_to_words(item.quantity)} {item.plural}")
            else:
                formatted.append(item.name)
        if formatted:
            return comma_separated(formatted)
        else:
            return "nothing"

    def pretty_inventory(self):
        print(f"You have {self.formatted_inventory()} in your inventory.")
        if self.equipped_weapon is not None:
            # TODO show weapon rating ?
            w = self.equipped_weapon
            print(f"You are wielding {int_to_words(w.quantity)} "
                  f"{remove_little_words(w.name) if w.quantity == 1 else w.plural}.")

    def status(self):
        print(f"Currently, you have {self.health} health. \nYou are located on map coordinates "
              f"{self.location}, which is {the_map[self.location].square_type}.")
        if p.building_local:
            print(f"You are inside {p.building_local.name}.")

        if self.skills:
            for k, v in self.skills.items():
                if v >= 100:
                    print(f"You have mastered {k}.")
                else:
                    print(f"You have learned {v}% of {k}.")
        else:
            print("You don't have any skills.")

        self.pretty_inventory()
        print(f"You have ${self.money} in your wallet.")

        if self.job:
            print(f"You have a job as a {self.job.name}.")
        if self.quest:
            print(f"You have a quest.")
        elif self.job is None and self.quest is None:
            print("You do not have a job, and you are not contributing to society.")


p = Player(name='', location=(0, 0))


class Item(object):
    def __init__(self, name, quantity, plural, category=None, perishable=None,
                 flammable=None, rarity=None, price=None, weapon_rating=None):
        self.name = name
        self.quantity = quantity
        self.plural = plural
        self.category = category or None
        self.perishable = perishable or None
        self.flammable = flammable or None
        self.rarity = rarity or None
        self.price = price or None
        self.weapon_rating = weapon_rating or None

    def copy(self):
        return Item(name=self.name, quantity=self.quantity, plural=self.plural, category=self.category,
                    perishable=self.perishable, flammable=self.flammable, rarity=self.rarity,
                    weapon_rating=self.weapon_rating)


class Building(object):
    def __init__(self, name, plural, category=None, rarity=None, ware_list=None, mobs=None, jobs=None):
        self.name = name
        self.quantity = 1
        self.plural = plural
        self.category = category or None
        self.rarity = rarity or None
        self.ware_list = ware_list
        self.wares = drops(ware_list, Item) if self.ware_list else None
        self.mobs = drops(mobs, Mob) if mobs else None
        self.jobs = self.drop_job(jobs) if jobs else None

    @staticmethod
    def drop_job(jobs):
        drops_i = []
        for k, v in jobs.items():
            if odds(2):
                drops_i.append(Job(name=k, **v))
        return drops_i


class Job(object):
    def __init__(self, name, skills_needed=None, salary=0, skills_learned=None, inventory_needed=None):
        self.name = name
        self.location = p.location
        self.skills_needed = skills_needed or None
        self.salary = salary or 0
        self.skills_learned = skills_learned or None
        self.inventory_needed = inventory_needed or None


class Mob(object):
    def __init__(self, name, plural, rarity):
        self.name = name
        self.plural = plural
        self.location = the_map[p.location]
        self.quantity = 1
        self.rarity = rarity

        self.skills = self.skills()
        self.quest = None

        self.inventory = drops(add_dicts_together(items['master'], items[self.location.square_type]), Item)
        self.health = 100
        self.equipped_weapon = self.equip()

    def equip(self):
        nice_weapons = []
        for i in self.inventory:
            try:
                if i.weapon_rating:
                    nice_weapons.append(i)
            except AttributeError:
                pass
        nice_weapons.sort(key=lambda x: x.weapon_rating, reverse=True)
        if nice_weapons:
            self.inventory.remove(nice_weapons[0])
            return nice_weapons[0]
        else:
            return None

    @staticmethod
    def skills():
        """ Pick the skills for a mob, these determine what a player can get from completing a quest """
        all_skills = ["strength", "patience", "cleanliness", "leadership", "communication", "self loathing",
                      "science", "math", "engineering", "intelligence", "driving"]

        random.shuffle(all_skills)
        return all_skills[0:2]

    def generate_quest(self):
        """
        inventory based
        bring me 100 of super common object to learn patience
        bring me a super rare object to learn patience
        bring me 10 uncommon object to earn 20 dollars

        or

        win a game of go fish with random mob type to learn intelligence
        say hello to 50 mobs to learn communication
        murder a jellyfish to earn money
        """

        if odds(3):

            quest_items = add_dicts_together(items["master"], items[the_map[p.location].square_type])
            quest_item = random.choice(list(quest_items.keys()))

            i = Item(quest_item, 0, **quest_items[quest_item])
            self.inventory.append(i)

            quantity = {'super rare': '1',
                        'rare': '2',
                        'uncommon': '3',
                        'common': '6',
                        'super common': '15'}
            q = quantity[i.rarity]

            self.quest = i, int(q), f"{p.name}, if you bring " \
                                    f"me {q} {i.plural if int(q) > 1 else remove_little_words(i.name)}, " \
                                    f"I will teach you a valuable skill."
        else:
            return None


the_map[(0, 0)].generate_items()
the_map[(0, 0)].generate_buildings()
the_map[(0, 0)].generate_mobs()
