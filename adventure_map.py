"""
This is Adventure. It is a text based adventure full of adventures.
"""
import random
import re
from text import items, buildings, numbers


command_list = {"help": True,
                "look around": True,
                "go southwest": True,
                "go sw": True,
                "inventory": True,
                "status": True,
                "pick up a rock": False,
                "pick up 1 rock": False,
                "pick up all rocks": False,
                "eat a mars bar": False,
                "walk into a bar": False}


results = {'super rare': 100,
           'rare': 50,
           'uncommon': 25,
           'common': 5,
           'super common': 2}


class Item(object):
    def __init__(self, name, quantity, plural, type=None, perishable=None, flammable=None, rarity=None):
        self.name = name
        self.quantity = quantity
        self.plural = plural
        self.type = type or None
        self.perishable = perishable or None
        self.flammable = flammable or None
        self.rarity = rarity or None


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
                    formatted.append("{} dollars".format(numbers[item.quantity]))

            elif item.quantity > 1:
                formatted.append("{} {}".format(numbers[item.quantity], item.plural))
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
            print("You do not have a job.")


def add_dicts_together(dict1, dict2):
    dict3 = dict(dict1)
    dict3.update(dict2)
    return dict3


def item_drops(dictionary):
    drops_i = []
    for k, v in dictionary.items():
        quantity = 0
        countdown = random.randint(0, 10)
        while countdown > 0:
            if random.randint(0, results[v["rarity"]]) == 1:
                quantity += 1
            countdown -= 1
        if quantity:
            drops_i.append(Item(name=k, quantity=quantity, **v))

    return drops_i


def buildings_drops(location):
    dictionary = add_dicts_together(buildings["master"], buildings[the_map[location].square_type])
    drops_i = []
    for k, v in dictionary.items():
        quantity = 0
        countdown = random.randint(0, 10)
        while countdown > 0:
            if random.randint(0, results[v["rarity"]]) == 1:
                quantity += 1
            countdown -= 1
        if quantity:
            # make mobs
            # add building type items
            pass

    return drops_i


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
        self.items = item_drops(add_dicts_together(items["master"], items[self.square_type]))

    def formatted_items(self):
        formatted = []
        for item in self.items:
            if item.quantity > 1:
                formatted.append("{} {}".format(numbers[item.quantity], item.plural))
            else:
                formatted.append(item.name)
        return formatted

    def generate_buildings(self):
        self.buildings = buildings_drops(add_dicts_together(buildings["master"], buildings[self.square_type]))

        pass


the_map = {(0, 0): MapSquare(name="spawn").new()}


def change_direction(direction):
    """
           y
           |
           |
       -------- x
           |
           |

    Changes the square to be one square over in the desired direction.
    Creates a new map square if not in the map.
    """
    x = p.location[0]
    y = p.location[1]
    if direction.lower() in ("n", "ne", "nw", "north", "northeast", "northwest"):
        y += 1
    if direction.lower() in ("e", "ne", "se", "east", "northeast", "southeast"):
        x += 1
    if direction.lower() in ("s", "se", "sw", "south", "southeast", "southwest"):
        y -= 1
    if direction.lower() in ("w", "nw", "sw", "west", "northwest", "southwest"):
        x -= 1

    p.location = (x, y)
    if p.location not in the_map.keys():
        the_map[p.location] = MapSquare().new()
    print("You are now located on map coordinates {}, which is {}.".format(
        p.location, the_map[p.location].square_type))
    the_map[p.location].generate_items()


def comma_separated(words):
    if len(words) >= 3:
        commas = ", ".join(words[0:-1])
        return "{} and {}".format(commas, words[-1])
    elif len(words) == 2:
        return "{} and {}".format(words[0], words[1])
    else:
        return words[0]


def commands(words):
    """ Command handler. """
    if words.lower() == "help":
        print("Available commands are 'look around', 'go north', 'go east', 'go south', and 'go west'")

    if words.lower().startswith("go"):
        change_direction(words.strip("go "))

    if words.lower() == "look around":
        look_around()

    if words.lower() == "inventory":
        print("You have {} in your inventory.".format(comma_separated(p.formatted_inventory())))

    if words.lower().startswith("pick up"):
        pick_up(words)

    if words.lower() == "status":
        p.status()


def look_around():
    command_list["pick up a rock"] = True
    command_list["pick up 1 rock"] = True
    if the_map[p.location].items:
        print("You can see {} near you.".format(comma_separated(the_map[p.location].formatted_items())))
    else:
        print("Nothing seems to be nearby.")


def pick_up(words):
    """
    pick up 3 rocks
    pick up three rocks
    pick up a rock
    pick up 1 rock
    pick up the rocks
    pick up all rocks
    """
    item_text = None
    quantity = 0

    if re.match(r"pick up \d .", words):
        s = words.split(" ")
        quantity = int(s[2])
        item_text = " ".join(s[3:])

    elif re.match(r"pick up .", words):
        s = words.split(" ")
        if s[2] in ("a", "an", "some"):
            quantity = 1
            item_text = " ".join(s[2:])
        elif s[2] in ("the", "all"):
            quantity = "all"
            item_text = " ".join(s[2:])
        else:
            for k, v in numbers.items():
                if v == s[2]:
                    quantity = k
            item_text = " ".join(s[3:])
    else:
        print("You wanna pick up what? Try again.")

    item = None
    for i in the_map[p.location].items:
        if item_text:
            if item_text in (i.name, i.plural):
                item = i
                break
    else:
        print("Couldn't pick up {}".format(item_text))

    if item:
        if quantity == "all":
            quantity = item.quantity

        if item.quantity >= quantity:
            p.inventory.append(item)
            if quantity == 1:
                print("Added {} to your inventory.".format(item.name))
            else:
                print("Added {} {} to your inventory.".format(numbers[quantity], item.plural))
            item.quantity -= quantity
            if item.quantity == 0:
                the_map[p.location].items.remove(item)
        elif item.quantity < quantity:
            print("Can't pick up that many.")

    if the_map[p.location].items is False:
        command_list["pick up a rock"] = False
        command_list["pick up 1 rock"] = False
        command_list["pick up all rocks"] = False

    if [x for x in p.inventory if x.type == "food"]:
        command_list["eat a mars bar"] = True
    else:
        command_list["eat a mars bar"] = False


def eat_food(words):
    """
    eat a mars bar
    eat 1 mars bar
    eat three mars bars
    eat 3 mars bars
    eat all mars bars
    eat the mars bars
    eat all food
    eat the perishable food
    """
    item_text = None
    quantity = 0
    s = words.split(" ")

    if re.match(r"eat \d .", words):
        quantity = int(s[1])
        if quantity > 1:
            item_text = " ".join(s[2:])

    elif re.match(r"eat .", words) and len(words.split(" ")) >= 3:
        if s[1] in ("a", "an", "some"):
            quantity = 1
            item_text = " ".join(s[2:])
        elif s[1] in ("the", "all"):
            quantity = "all"
            item_text = " ".join(s[2:])
        else:
            for k, v in numbers.items():
                if v == s[2]:
                    quantity = k
            item_text = " ".join(s[3:])

    elif re.match(r"eat .", words) and len(words.split(" ")) == 2:
        quantity = "all"
        item_text = s[1]

    item = None

    food = [x for x in p.inventory if x.type == "food"]
    if "perishable" in item_text:
        food = [x for x in p.inventory if x.type == "food" and x.perishable]

    if quantity == "all":
        quantity = item.quantity

    if "food" in item_text:
        for item in food:
            if isinstance(quantity, int):
                if item.quantity <= quantity:
                    item.quantity = 0
                    quantity -= item.quantity
                    eat(item)
                elif quantity < item.quantity:
                    item.quantity -= quantity
                    quantity = 0
                else:
                    break
            else:
                item.quantity = 0
                eat(item)
    else:
        for item in food:
            if item_text in (item.name, item.plural):
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    if item.quantity == 0:
                        eat(item)
                else:
                    print("Couldn't eat that many.")
        else:
            print("Couldn't find {}.".format(item_text))

    if [x for x in p.inventory if x.type == "food"] is False:
        command_list["eat a mars bar"] = False


def eat(item_eaten):
    p.inventory.remove(item_eaten)
    if p.health < 100:
        regenerate = random.randint(0, 100-p.health)
        p.health += regenerate
        print("Regenerated {}% health by eating {}.".format(regenerate, item_eaten.name))

# specify which mob you killed perhaps.
# tackle next: reusable weapons. You don't want to 'throw' your really rare
# bow, for example.
# mobs cause damage - you should kill them or scare them off.
# player death - always a good goal
# ways to regen health.


if __name__ == "__main__":
    player_name = input("Welcome to the world, adventurer! What name would "
                        "you like to be known as in this land? \n")
    p = Player(player_name, (0, 0))
    the_map[p.location].generate_items()
    print("Nice to meet you, {}!".format(p.name))
    p.status()
    print("Use commands to interact with your world. At any time, type 'help' "
          "to see all available commands.")
    while p.health > 0:
        commands(input())

# have the interview process include drug testing
# interact with mobs - attack, ask for job application, trade with, do a quest
# interact with inventory - eat food, drive car, etc.
# eat food to regen health
# trade with mobs