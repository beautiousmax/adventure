import random
import colorama
from app.common_functions import comma_separated, add_dicts_together, remove_little_words, odds
from data.text import items, buildings, wild_mobs, names, adjectives
from reusables.string_manipulation import int_to_words

colorama.init()


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
    def __init__(self, name, plural, category=None, rarity=None, wares=None, mobs=None, jobs=None):
        self.name = name
        self.quantity = 1
        self.plural = plural
        self.category = category or None
        self.rarity = rarity or None
        self.wares = drops(wares, Item) if wares else None
        self.mobs = drops(mobs, Mob) if mobs else None
        self.jobs = jobs

    # TODO add job interviews


class Mob(object):
    def __init__(self, name, plural, rarity):
        self.name = name
        self.plural = plural
        self.quantity = 1
        self.rarity = rarity

        self.skills = self.skills()
        self.quest = None

    inventory = []
    health = 100

    def skills(self):
        """Pick the skills for a mob, these determine what a player can get from completing a quest"""
        all_skills = ["strength", "patience", "cleanliness", "leadership", "communication", "self loathing",
                      "science", "math", "engineering", "intelligence"]

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
        """

        if odds(3):

            quest_items = add_dicts_together(items["master"], items[the_map[p.location].square_type])
            quest_item = random.choice(list(quest_items.keys()))

            i = Item(quest_item, 0, **quest_items[quest_item])
            self.inventory.append(i)

            quantity = {'super rare': '1',
                        'rare': '2',
                        'uncommon': '5',
                        'common': '10',
                        'super common': '20'}
            q = quantity[i.rarity]

            self.quest = i, int(q), f"{p.name}, if you bring " \
                                    f"me {q} {i.plural if int(q) > 1 else remove_little_words(i.name)}, " \
                                    f"I will teach you a valuable skill."
        else:
            return None


class Player(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.money = 0
        self.quest = None
        self.job = None

    building_local = None
    inventory = []
    skills = {}
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
            print(f"You are inside {p.building_local.name}.")

        if self.skills:
            for k, v in self.skills.items():
                if v >= 100:
                    print(f"You have mastered {k}.")
                else:
                    print(f"You have learned {v}% of {k}.")
        else:
            print("You don't have any skills.")

        print(f"You have {self.formatted_inventory()} in your inventory.")
        print(f"You have ${self.money} in your wallet.")

        if self.job:
            print(f"You have a job as a {self.job}.")
        if self.quest:
            print(f"You have a quest.")
        elif self.job is None and self.quest is None:
            print("You do not have a job, and you are not contributing to society.")


class MapSquare(object):
    def __init__(self, name=""):
        square_types = ["forest", "mountains", "desert", "city", "swamp", "ocean"]
        self.square_type = square_types[random.randint(0, len(square_types) - 1)]
        self.name = name
    mobs = []
    items = []
    buildings = []

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
        used_names = []
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
                        n = ''
                        while n not in used_names:
                            n = names[random.randint(0, len(names)-1)]
                            if n not in used_names:
                                used_names.append(n)
                        drops_i.append(Mob(name=f"{k} named {n}", **v))
                else:
                    drops_i.append(Mob(name=k, **v))
            elif object_in_question == Building:
                if quantity > 1 and v['category'] != 'residence':
                    for m in range(0, quantity):
                        if odds(2):
                            n = ''
                            while n not in used_names:
                                n = adjectives[random.randint(0, len(adjectives) - 1)]
                                if n not in used_names:
                                    used_names.append(n)
                            drops_i.append(Building(name=f"The {n} {remove_little_words(k).capitalize()}", **v))
                        else:
                            n = ''
                            while n not in used_names:
                                n = names[random.randint(0, len(names) - 1)]
                                if n not in used_names:
                                    used_names.append(n)
                            drops_i.append(Building(name=f"{n}'s {remove_little_words(k).capitalize()}", **v))
                elif quantity > 1 and v['category'] == 'residence':
                    for m in range(0, quantity):
                        n = ''
                        while n not in used_names:
                            n = names[random.randint(0, len(names) - 1)]
                            if n not in used_names:
                                used_names.append(n)

                        drops_i.append(Building(name=f"{n}'s {remove_little_words(k)}", **v))
                else:
                    drops_i.append(Building(name=k, **v))

    return drops_i


the_map = {(0, 0): MapSquare(name="spawn")}
the_map[(0, 0)].generate_items()
the_map[(0, 0)].generate_buildings()
the_map[(0, 0)].generate_mobs()

p = Player(name='', location=(0, 0))
