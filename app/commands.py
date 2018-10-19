from app.main_classes import MapSquare, the_map, p
from app.common_functions import formatted_items, comma_separated, parse_inventory_action, odds, remove_little_words
import random
from reusables.string_manipulation import int_to_words

command_list = {"help": True,
                "look around": True,
                "go <southwest>": True,
                "go <sw>": True,
                "inventory": True,
                "status": True,
                "pick up <something>": False,
                "eat <something>": False,
                "visit <a building>": False,
                "buy <something>": False}


def commands_manager(words):
    """ Command handler. """
    words = words.lower().split(" ")
    if words[0] == "help":
        if the_map[p.location].items:
            command_list["pick up <something>"] = True
        else:
            command_list["pick up <something>"] = False
        for x in p.inventory:
            if x.category == "food":
                command_list["eat <something>"] = True
                break
        else:
            command_list["eat <something>"] = False

        for command, status in command_list.items():
            if status:
                print(command)

        if the_map[p.location].buildings:
            command_list["visit <a building>"] = True
        else:
            command_list["visit <a building>"] = False

    elif words[0] == "go":
        change_direction(" ".join(words[1:]))

    elif words[0] == "visit":
        interact_with_building(" ".join(words[1:]))

    elif words[0] == "leave":
        leave_building()

    elif " ".join(words) == "look around" or "look" in words:
        look_around()

    elif " ".join(words) == "inventory":
        print(f"You have {p.formatted_inventory()} in your inventory.")

    elif " ".join(words[0:2]) == "pick up":
        pick_up(" ".join(words[2:]))

    elif words[0] == "take":
        pick_up(" ". join(words[1:]))

    elif " ".join(words) == "status":
        p.status()

    elif words[0] == "eat":
        eat_food(" ".join(words[1:]))

    elif words[0] == "buy":
        buy(" ".join(words[1:]))

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
    leave_building()
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
        the_map[p.location].generate_mobs()
    print(f"You are now located on map coordinates {p.location}, which is {the_map[p.location].square_type}.")
    the_map[p.location].generate_items()


def look_around():
    if p.building_local is None:
        if the_map[p.location].items:
            print(f"You can see {comma_separated(formatted_items(the_map[p.location].items))} near you.")
        if the_map[p.location].buildings:
            print(f"The buildings here are {comma_separated(formatted_items(the_map[p.location].buildings))}.")
        if the_map[p.location].mobs:
            print(f"There {'are' if len(the_map[p.location].mobs) > 1 else 'is'} "
                  f"{comma_separated(formatted_items(the_map[p.location].mobs))} here.")
        if the_map[p.location].items == [] and the_map[p.location].buildings == [] and the_map[p.location].mobs == []:
            print("Nothing seems to be nearby.")
    # TODO generate more items to look at / find after picking up stuff?

    else:
        if p.building_local.wares:
            wares = []
            for x in p.building_local.wares:
                if x.quantity > 1:
                    wares.append(f"{int_to_words(x.quantity)} {x.plural}")
                else:
                    wares.append(x.name)
            print(f"This {p.building_local.name} has these items for sale: {comma_separated(wares)}")

        if p.building_local.mobs:
            print(f"The people here are {p.building_local.mobs}")


def pick_up(words):
    quantity, item_text = parse_inventory_action(words)

    if item_text is None:
        for i in the_map[p.location].items:
            add_item_to_inventory(i, i.quantity)
        print(f"Added {comma_separated([x.name for x in the_map[p.location].items])} to your inventory.")
        the_map[p.location].items = []

    else:
        item = None
        for i in the_map[p.location].items:
            if item_text in i.name or item_text in i.plural:
                item = i
                break
        else:
            print(f"Couldn't pick up {item_text}")

        if item:
            if quantity == "all":
                quantity = item.quantity

            if item.quantity >= quantity:
                add_item_to_inventory(item, quantity)
                item.quantity -= quantity
                if item.quantity == 0:
                    the_map[p.location].items.remove(item)
                print(f"Added {item.name if quantity == 1 else item.plural} to your inventory.")
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
            print(f"Regenerated {regenerate}% health by eating {item_eaten.name}.")

    food = [x for x in p.inventory if x.category == "food"]
    if item_text and "perishable" in item_text:
        food = [x for x in p.inventory if x.category == "food" and x.perishable]

    if item_text is None and quantity is "all":
        for i in food:
            eat(i, i.quantity)

    elif "food" in item_text:
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
                return
        else:
            print(f"Couldn't eat {item_text}")


def apply_for_job():
    if p.building_local.jobs():

        print(f"Hello! We are looking to hire {p.building_local.jobs} currently.")


def interact_with_building(words):
    for building in the_map[p.location].buildings:
        if remove_little_words(words) in remove_little_words(building.name):
            if building.category == 'building':
                if odds(8) is True:
                    print(f"Too bad, {building.name} is closed right now. Try again later.")
                else:
                    p.building_local = building
                    command_list['visit <a building>'] = False
                    command_list['leave'] = True
                    if p.building_local.wares:
                        command_list['buy <something>'] = True
                    print(f"You are now inside {building.name}.")

            else:
                if odds(10) is False:
                    print("The occupants of this residence have kicked you out.")
                else:
                    command_list['visit <a building>'] = False
                    command_list['leave'] = True
                    p.building_local = building
                    print("You are now inside a house")
            break

    else:
        print("That's not a place you can visit.")


def leave_building():
    if p.building_local is not None:
        command_list['visit <a building>'] = True
        command_list['leave'] = False
        command_list['buy <something>'] = False
        print(f"Leaving {p.building_local.name}")
        p.building_local = None


def buy(words):
    wares = []
    haggle_for = True
    quantity, item_text = parse_inventory_action(words)

    if quantity == all and item_text is None:
        wares = [x for x in p.building_local.wares]
        ware_list = [f"{ware.plural} x {ware.quantity}" for ware in p.building_local.wares]
        price_total = sum([ware.price*ware.quantity for ware in p.building_local.wares])
        print(f"For {comma_separated(ware_list)}, that comes to {price_total}.")

    else:
        for ware in p.building_local.wares:

            if remove_little_words(item_text) in ware.name or remove_little_words(item_text) in ware.plural:
                wares = [ware]
                if quantity == "all":
                    quantity = ware.quantity

                if quantity > ware.quantity:
                    print(f"Sorry, we only have {ware.quantity} for sale.")
                    haggle_for = False
                else:
                    print(f"For {ware.plural} x {ware.quantity}, that comes to ${ware.price*quantity}.")
                break
        else:
            print("I can't figure out what you want.")
            haggle_for = False

    if haggle_for is True:
        price_offered = input("Make me an offer:")
        try:
            price_offered = int(price_offered.strip(" "))
        except ValueError:
            print("I was hoping for a number, sorry.")
        haggle(wares, quantity, price_offered)


def haggle(items, quantity, price_offered):
    if price_offered > p.money:
        print("Sorry you don't have enough cash to make that offer. Try getting a job.")
        return

    price = sum([item.price for item in items]) * quantity
    if price >= price_offered and price_offered <= p.money:
        for item in items:
            item.quantity = quantity
            p.inventory.append(item)
            p.money -= price_offered
        print("Purchase complete")

    elif price > price_offered:
        if odds(price-price_offered) is True:
            print("Ok, sounds like a deal.")
            for item in items:
                item.quantity = quantity
                p.inventory.append(item)
                p.money -= price_offered
        else:
            print("Sorry, I can't sell for that price.")
