import random

import colorama
from termcolor import colored
from reusables.string_manipulation import int_to_words

from app.common_functions import comma_separated, add_dicts_together, remove_little_words, odds
from data.text import items, buildings, wild_mobs, names, adjectives


colorama.init()


def find_unique_adjectives(quantity, taken_names):
    free_adjectives = [x for x in adjectives if x not in taken_names]
    random.shuffle(free_adjectives)
    return free_adjectives[:quantity]


def find_unique_names(quantity, taken_names):
    free_names = [x for x in names if x not in taken_names]
    random.shuffle(free_names)
    return free_names[:quantity]


def dropper(rarity):
    results = {'super rare': 100,
               'rare': 50,
               'uncommon': 25,
               'common': 5,
               'super common': 2}
    quantity = 0
    countdown = random.randint(0, 10)
    while countdown > 0:
        if random.randint(0, results[rarity]) == 1:
            quantity += 1
        countdown -= 1
    return quantity


def drop_building(dictionary, p, limit=None):
    limit = limit or len(adjectives)
    drops_i = []

    for k, v in dictionary.items():
        quantity = dropper(v['rarity'])
        quantity = quantity if quantity < limit else limit
        limit -= quantity
        if quantity:
            if quantity > 1 and v['category'] != 'residence':
                n = random.randint(0, quantity)
                unique_names = find_unique_names(quantity - n, p.square.unique_building_names)
                p.square.unique_building_names += unique_names
                for i in range(0, quantity - n):
                    drops_i.append(Building(name=f"{unique_names[i]}'s {remove_little_words(k).capitalize()}", p=p, **v))
                unique_adjectives = find_unique_adjectives(n, p.square.unique_building_names)
                p.square.unique_building_names += unique_adjectives
                for i in range(0, n):
                    drops_i.append(Building(name=f"the {unique_adjectives[i]} {remove_little_words(k).capitalize()}", p=p, **v))

            elif quantity > 1 and v['category'] == 'residence':
                unique_house_names = find_unique_names(quantity, p.square.unique_house_names)
                p.square.unique_house_names += unique_house_names
                for i in range(0, quantity):
                    drops_i.append(Building(name=f"{unique_house_names[i]}'s {remove_little_words(k)}", p=p, **v))
            else:
                drops_i.append(Building(name=k, p=p, **v))
    return drops_i


def drop_mob(dictionary, p, limit=None, square=None):
    square = square or p.square
    limit = limit or len(names) - len(square.unique_mob_names)
    drops_i = []

    for k, v in dictionary.items():
        quantity = dropper(v['rarity'])
        quantity = quantity if quantity < limit else limit
        limit -= quantity
        if quantity:
            if quantity > 1:
                unique_names = find_unique_names(quantity, square.unique_mob_names)
                p.square.unique_mob_names += unique_names
                for i in range(0, len(unique_names)):
                    drops_i.append(Mob(name=f"{k} named {unique_names[i]}", p=p, **v))
            else:
                if k not in [n.name for n in p.square.mobs]:
                    drops_i.append(Mob(name=k, p=p, **v))
                else:
                    name = find_unique_names(1, square.unique_mob_names)[0]
                    drops_i.append(Mob(name=f"{k} named {name}", p=p, **v))
    return drops_i


def drop_item(dictionary):
    """ Randomly generates objects based on rarity """
    drops_i = []

    for k, v in dictionary.items():
        quantity = dropper(v['rarity'])
        if quantity:
            drops_i.append(Item(name=k, quantity=quantity, **v))

    return drops_i


class MapSquare:
    def __init__(self, name="", square_type=None):
        square_types = ["forest", "mountains", "desert", "city", "swamp", "ocean"]
        self.square_type = square_type or square_types[random.randint(0, len(square_types) - 1)]
        self.name = name
        self.unique_mob_names = []
        self.unique_building_names = []
        self.unique_house_names = []

    mobs = []
    items = []
    buildings = []

    def generate_items(self):
        self.items = drop_item(add_dicts_together(items["master"], items[self.square_type]))

    def generate_buildings(self, p):
        self.buildings = drop_building(add_dicts_together(buildings["master"], buildings[self.square_type]), p)

    def generate_mobs(self, p):
        self.mobs = drop_mob(add_dicts_together(wild_mobs["master"], wild_mobs[self.square_type]), p)

    def clean_up_map(self):
        """ Remove items with quantity of zero from the map inventory"""
        self.items = [i for i in self.items if i.quantity != 0]

    @staticmethod
    def map_picture(the_map, p):
        """With the player's location in the center, draw a 5 x 5 map with map square type
        and coordinates in each square"""
        xy = (p.location[0] - 2, p.location[1] + 2)
        map_coords = []
        for y in range(0, 5):
            row = [(xy[0] + x, xy[1] - y) for x in range(0, 5)]
            map_coords.append(row)

        pretty_map = []
        for r in map_coords:
            row = []
            for coordinates in r:
                if coordinates in the_map.keys():
                    if p.quest and p.job and p.quest[1] == coordinates and p.job.location == coordinates:
                        star = '*$ '
                    elif p.quest and p.quest[1] == coordinates:
                        star = ' * '
                    elif p.job and p.job.location == coordinates:
                        star = ' $ '
                    else:
                        star = '   '
                    row.append("|{!s:9}{}|".format(the_map[coordinates].square_type, star))
                else:
                    row.append("|{!s:12}|".format(' '))
            pretty_map.append(row)
        for row in pretty_map:
            print(''.join(row))


class Player:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.square = None
        self.money = 0
        self.quest = None
        self.job = None
        self.phase = "day"

    equipped_weapon = None
    major_armor = None
    minor_armor = None
    building_local = None
    inventory = []
    skills = {}
    health = 100
    greeting_count = 0
    body_count = 0
    assassination_count = 0
    hit_list = []
    death_count = 0
    food_count = 0
    run_away_count = 0
    # TODO increase insurance cost every death?
    speed_bonus = False
    game_won = False

    def game_over(self):
        if self.game_won is False:
            self.game_won = True
            print(colored("You have won the game!", "green"))
            print("You may continue playing to earn more achievements if you wish.")
            if self.run_away_count == 0:
                print("Congratulations, you have achieved the True Bravery achievement, having won the game without ever running away from a fight.")
            if self.run_away_count > 100:
                print("Congratulations, you have achieved the True Cowardice achievement, having won the game after running away from over 100 battles.")

    def clean_up_inventory(self):
        """ Remove items with quantity of zero from the map inventory"""
        self.inventory = [i for i in self.inventory if i.quantity != 0]

    def phase_change(self, the_map):
        self.phase = 'day' if self.phase == 'night' else 'night'
        for k, square in the_map.items():
            if self.location != k:
                square.generate_items()
                for b in square.buildings:
                    if b.ware_list:
                        b.wares = drop_item(b.ware_list)
                        while not b.wares:
                            b.wares = drop_item(b.ware_list)
                    jobs = {}
                    buiding_dict = add_dicts_together(buildings['master'], buildings[square.square_type])
                    for key, v in buiding_dict.items():
                        if key == b.name and v.get('jobs'):
                            for name, values in v['jobs'].items():
                                jobs[name] = values
                    b.jobs = b.drop_job(jobs)
                if self.phase == 'day':
                    self.speed_bonus = False
                    for mob in square.mobs:
                        mob.health = 100
                        mob.irritation_level = 0
                        mob.quest = None if self.quest is None else mob.quest
                    if not square.mobs:
                        square.mobs = drop_mob(add_dicts_together(wild_mobs["master"], wild_mobs[self.square.square_type]),
                                               self, limit=len(names), square=square)

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
        w = self.equipped_weapon
        major = self.major_armor.defense if self.major_armor else 0
        minor = self.minor_armor.defense if self.minor_armor else 0
        armor_defense = (major + minor) * 5

        armors = [self.major_armor.name if self.major_armor else None, self.minor_armor.name if self.minor_armor else None]

        inventory = {'inventory_items': f"You have {self.formatted_inventory()} in your inventory.",
                     'weapon': f"You are wielding {int_to_words(w.quantity)} "
                               f"{remove_little_words(w.name) if w.quantity == 1 else w.plural}." if w else None,
                     'armor': f"You are wearing {' and '.join(x for x in armors if x)}, "
                     f"giving you a {armor_defense}% reduction in incoming damage." if self.minor_armor or self.major_armor else None}
        return '\n'.join(v for v in inventory.values() if v)

    def status(self):
        skills = [f"{k} - {v}%." for k, v in self.skills.items()]

        job = f"You have a job as a {self.job.name}." if self.job else None
        quest = "You have a quest." if self.quest else None
        if job and quest:
            job_string = "\n".join([job, quest])
        elif job or quest:
            job_string = job if job else quest
        else:
            job_string = "You do not have a job, and you are not contributing to society."

        status_string = {
            'health': f'Currently, you have {self.health} health.',
            'location': f'You are located on map coordinates {self.location}, '
                        f'which is {self.square.square_type}.',
            'building_local': f'You are inside {self.building_local.name}.' if self.building_local else None,
            'skills': '\n'.join(skills) if skills else "You don't have any skills.",
            'money': f"You have ${self.money} in your wallet.",
            'job': job_string}

        return '\n'.join(v for v in status_string.values() if v)

    def statistics(self):
        print(f"You have killed {self.body_count} mobs.")
        print(f"You have ran away from {self.run_away_count} battles.")
        print(f"You have eaten {self.food_count} items.")
        print(f"You have performed {self.assassination_count} assassinations.")
        print(f"You have talked to mobs {self.greeting_count} times.")

    def view_hit_list(self):
        if self.hit_list:
            print(f"If you ever run across these shady characters, be sure to take their names off your list: {comma_separated(self.hit_list)}")
        else:
            print("Looks like you don't know of anyone who needs to be dead.")

    def increase_skill(self, skill, increase):
        try:
            self.skills[skill] += increase
        except KeyError:
            self.skills[skill] = increase
        print(f"You have increased your mastery of {skill} by {increase}% for a total of {self.skills[skill]}%.")


class Item:
    def __init__(self, name, quantity, plural, category=None, perishable=None,
                 flammable=None, rarity=None, price=None, weapon_rating=None, defense=None):
        self.name = name
        self.quantity = quantity
        self.plural = plural
        self.category = category or None
        self.perishable = perishable or None
        self.flammable = flammable or None
        self.rarity = rarity or None
        self.price = price or None
        self.weapon_rating = weapon_rating or None
        self.defense = defense or None

    def copy(self):
        return Item(name=self.name, quantity=self.quantity, plural=self.plural, category=self.category,
                    perishable=self.perishable, flammable=self.flammable, rarity=self.rarity,
                    weapon_rating=self.weapon_rating, defense=self.defense)


class Building(object):
    def __init__(self, name, p, plural, category=None, rarity=None, ware_list=None, mobs=None, jobs=None):
        self.name = name
        self.p = p
        self.quantity = 1
        self.plural = plural
        self.category = category or None
        self.rarity = rarity or None
        self.ware_list = ware_list
        self.wares = self.drop_wares()
        self.mobs = drop_mob(mobs, p) if mobs else None
        self.jobs = self.drop_job(jobs) if jobs else None

        if self.name in ('a castle', 'a volcanic base'):
            self.boss_mobs_and_jobs()

    def drop_wares(self):
        if self.ware_list:
            wares = drop_item(self.ware_list)
            while not wares:
                wares = drop_item(self.ware_list)
            return wares
        else:
            return []

    def drop_job(self, jobs):
        drops_i = []
        for k, v in jobs.items():
            if odds(2):
                drops_i.append(Job(name=k, location=self.p.location, **v))
        return drops_i

    def boss_mobs_and_jobs(self):
        boss_major_armors = [Item('a coat of impervious dragon scales', plural='coats of dragon scales', quantity=1, category='major armor', rarity='super rare', defense=5),
                             Item('an enchanted leather duster', plural='enchanted leather dusters', quantity=1, category='major armor', defense=5, rarity='super rare'),
                             Item('a coat of actual live grizzly bears', plural='coats of actual live grizzly bears', quantity=1, category='major armor', defense=5, rarity='super rare')]
        boss_minor_armors = [Item('wings of an angel', plural='wings of angels', quantity=1, rarity='super rare', category='minor armor', defense=5),
                             Item('an OSHA approved hard hat', plural='OSHA approved hard hats', quantity=1, rarity='super rare', category='minor armor', defense=5),
                             Item('a pair boots that were made for walkin', plural='pairs of boots that were made for walkin', quantity=1, rarity='super rare', category='minor armor', defense=5)]
        boss_weapons = [Item('an apache helicopter', plural='apache helicopters', rarity='super rare', weapon_rating=6, quantity=1),
                        Item('a trebuchet', plural='trebuchets', weapon_rating=6, quantity=1, rarity='super rare'),
                        Item('an army of attacking wizards', plural='armies of attacking wizards', weapon_rating=6, quantity=1, rarity='super rare')]
        boss_names = ["the Terrifying Dragon of Soul Slaying", "the Great Salamander of Darkness", "the Squirrel of Destiny", ]
        random.shuffle(boss_names)
        random.shuffle(boss_weapons)
        random.shuffle(boss_major_armors)
        random.shuffle(boss_minor_armors)

        boss = Mob(boss_names[0], self.p, plural=boss_names[0], rarity='super rare')
        boss.health = 500
        boss.equipped_weapon = boss_weapons[0]
        boss.major_armor = boss_major_armors[0]
        boss.minor_armor = boss_minor_armors[0]
        boss.irritation_level = 15
        self.mobs = [boss]
        if self.name == 'a castle':
            self.jobs = [Job('king of the realm', location=self.p.location, salary=1100)]
        if self.name == 'a volcanic base':
            self.jobs = [Job('evil overlord', location=self.p.location, salary=1100)]


class Job:
    def __init__(self, name, location, skills_needed=None, salary=0, skills_learned=None, inventory_needed=None):
        self.name = name
        self.location = location
        self.skills_needed = skills_needed or None
        self.salary = salary or 0
        self.skills_learned = skills_learned or None
        self.inventory_needed = inventory_needed or None
        self.application_attempts = 0


class Mob:
    def __init__(self, name, p, plural, rarity, inventory=None):
        self.name = name
        self.p = p
        self.plural = plural
        self.quantity = 1
        self.rarity = rarity

        self.skills = self.skills()
        self.quest = None

        self.inventory = inventory or drop_item(add_dicts_together(items['master'], items[p.square.square_type]))
        self.health = 100
        self.equipped_weapon = self.equip()
        major = [x for x in self.inventory if x.category == 'major armor']
        minor = [x for x in self.inventory if x.category == 'minor armor']
        self.major_armor = major[0] if major else None
        self.minor_armor = minor[0] if minor else None
        self.irritation_level = 0

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
        all_skills = ["strength", "patience", "cleanliness", "leadership", "communication",
                      "science", "math", "engineering", "intelligence", "driving"]

        random.shuffle(all_skills)
        return all_skills[0:2]

    def generate_quest(self):
        """
        inventory based
        bring me x of an object to learn a skill
        """

        if odds(3):

            quest_items = add_dicts_together(items["master"], items[self.p.square.square_type])
            quest_item = random.choice(list(quest_items.keys()))

            i = Item(quest_item, 0, **quest_items[quest_item])
            self.inventory.append(i)

            quantity = {'super rare': '1',
                        'rare': '2',
                        'uncommon': '3',
                        'common': '6',
                        'super common': '15'}
            q = quantity[i.rarity]

            self.quest = i, int(q), f"{self.p.name}, if you bring " \
                                    f"me {q} {i.plural if int(q) > 1 else remove_little_words(i.name)}, " \
                                    f"I will teach you a valuable skill."
            return
        elif odds(5):
            mobs = []
            for biome, building in buildings.items():
                for b, attributes in building.items():
                    if attributes.get('mobs'):
                        for k in attributes['mobs'].keys():
                            mobs.append(k)
            for biome, mob in wild_mobs.items():
                for k in mob.keys():
                    mobs.append(k)
            target = f"{mobs[random.randint(0, len(mobs)-1)]} named {names[random.randint(0, len(names)-1)]}"
            print(f"Well, we'll keep this off the record, but I can arrange for some money to find its way "
                  f"into your account if you make {colored(target, 'yellow')} disappear, if you know what I mean...")
            self.p.hit_list.append(target)
            return False

        else:
            return None
