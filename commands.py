from main_classes import MapSquare, the_map, p
from common_functions import formatted_items, comma_separated, parse_inventory_action
import random

command_list = {"help": True,
                "look around": True,
                "go southwest": True,
                "go sw": True,
                "inventory": True,
                "status": True,
                "pick up a rock": False,
                "eat a mars bar": False,
                "walk into a bar": False}


def commands_manager(words):
    """ Command handler. """
    words = words.lower().split(" ")
    if words[0] == "help":
        if the_map[p.location].items:
            command_list["pick up a rock"] = True
        else:
            command_list["pick up a rock"] = False
        for x in p.inventory:
            if x.type == "food":
                command_list["eat a mars bar"] = True
                break
        else:
            command_list["eat a mars bar"] = False

        for command, status in command_list.items():
            if status:
                print(command)

    elif words[0] == "go":
        if p.building_local is None:
            change_direction(" ".join(words[1:]))

    elif words[0] == "visit":
        interact_with_building(" ".join(words[1:]))

    elif words[0] == "leave":
        p.building_local = None

    elif " ".join(words) == "look around":
        look_around()

    elif " ".join(words) == "inventory":
        print("You have {} in your inventory.".format(comma_separated(p.formatted_inventory())))

    elif " ".join(words[0:2]) == "pick up":
        pick_up(" ".join(words[2:]))

    elif words[0] == "take":
        pick_up(" ". join(words[1:]))

    elif " ".join(words) == "status":
        p.status()

    elif words[0] == "eat":
        eat_food(" ".join(words[1:]))

    else:
        print("I don't know that command.")


def change_direction(direction):
    """
    Change direction:

    go north
    go southwest
    go n
    go sw
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
        the_map[p.location].generate_buildings()
    print("You are now located on map coordinates {}, which is {}.".format(
        p.location, the_map[p.location].square_type))
    the_map[p.location].generate_items()


def look_around():
    command_list["pick up a rock"] = True
    command_list["pick up 1 rock"] = True
    if the_map[p.location].items:
        print("You can see {} near you.".format(comma_separated(formatted_items(the_map[p.location].items))))
    if the_map[p.location].buildings:
        print("The buildings here are {}".format(comma_separated(formatted_items(the_map[p.location].buildings))))
    if the_map[p.location].items == [] and the_map[p.location].buildings == []:
        print("Nothing seems to be nearby.")


def pick_up(words):
    quantity, item_text = parse_inventory_action(words)

    if item_text is None:
        for i in the_map[p.location].items:
            add_item_to_inventory(i, i.quantity)
        the_map[p.location].items = []

    else:
        item = None
        for i in the_map[p.location].items:
            if item_text in i.name or item_text in i.plural:
                item = i
                break
        else:
            print("Couldn't pick up {}".format(item_text))

        if item:
            if quantity == "all":
                quantity = item.quantity

            if item.quantity >= quantity:
                add_item_to_inventory(item, quantity)
                item.quantity -= quantity
                if item.quantity == 0:
                    the_map[p.location].items.remove(item)
            elif item.quantity < quantity:
                print("Can't pick up that many.")


def add_item_to_inventory(item_to_add, quantity):
    if item_to_add.name in [x.name for x in p.inventory]:
        for x in p.inventory:
            if item_to_add.name == x.name:
                x.quantity += int(quantity)
    else:
        new_item = item_to_add.copy()
        new_item.quantity = quantity
        p.inventory.append(new_item)


def eat_food(words):
    """
    Eat food in your inventory:

    eat a mars bar
    eat 1 mars bar
    eat three mars bars
    eat 3 mars bars
    eat all mars bars
    eat the mars bars
    eat all food
    eat everything
    eat the food
    eat some food
    eat the perishable food
    """

    quantity, item_text = parse_inventory_action(words)

    if quantity is None and item_text is None:
        print("I can't figure out what you want to eat!")
        return

    def eat(item_eaten, q):
        if q > item_eaten.quantity:
            print("Cant eat that many")
            return

        item_eaten.quantity -= q

        if item_eaten.quantity == 0:
            p.inventory.remove(item_eaten)

        if p.health < 100:
            regenerate = random.randint(0, 100-p.health)
            p.health += regenerate
            print("Regenerated {}% health by eating {}.".format(regenerate, item_eaten.name))

    food = [x for x in p.inventory if x.type == "food"]
    if "perishable" in item_text:
        food = [x for x in p.inventory if x.type == "food" and x.perishable]

    if item_text is "all":
        for i in food:
            eat(i, i.quantity)
        else:
            print("Couldn't eat {}.".format(item_text))

    if "food" in item_text:
        for i in food:
            if isinstance(quantity, int):
                if i.quantity <= quantity:
                    i.quantity = 0
                    quantity -= i.quantity
                    eat(i, quantity)
                elif quantity < i.quantity:
                    i.quantity -= quantity
                    quantity = 0
                else:
                    break
            else:
                eat(i, i.quantity)

    else:
        for i in food:
            if item_text in i.name or item_text in i.plural:
                if quantity == "all":
                    quantity = i.quantity
                eat(i, quantity)


def purchase_items(words):
    quantity, item_text = parse_inventory_action(words)


def apply_for_job():
    if p.building_local.jobs():

        print("Hello! We are looking to hire {} currently.")


def interact_with_building(words):
    p.building_local = words

    for i in the_map[p.location].buildings.interactions:
        command_list[i] = True
